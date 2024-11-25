# EXPLAINABILITY FUNCTIONS

###  SmoothGrad ###

import torch
import numpy as np

def smoothgrad(model, input_tensor, stdev_spread=0.15, nsamples=50):
    mean = 0
    stdev = stdev_spread * (input_tensor.max() - input_tensor.min())
    total_gradients = torch.zeros_like(input_tensor)

    for i in range(nsamples):
        noise = torch.randn_like(input_tensor) * stdev
        noisy_input = input_tensor + noise
        noisy_input.requires_grad_()

        output = model(noisy_input)
        output.backward()
        gradients = noisy_input.grad
        total_gradients += gradients

    avg_gradients = total_gradients / nsamples
    return avg_gradients.cpu().numpy()

###  SmoothGrad ###

###  LIME ###

import torch
import numpy as np
import lime
from lime import lime_tabular

def feature_to_channel_position(index, channels, height, width):
    """
    Converte um índice de feature achatado para canal e posição original na matriz 13x8x8.
    :param index: Índice linear (achado).
    :param channels: Número de canais (13).
    :param height: Altura da matriz (8).
    :param width: Largura da matriz (8).
    :return: (canal, x, y)
    """
    channel = index // (height * width)
    remaining = index % (height * width)
    x = remaining // width
    y = remaining % width
    return channel, x, y

def model_predict(X_input, model):
    with torch.no_grad():
        model.eval()
        X_input_tensor = torch.tensor(X_input, dtype=torch.float32)
        output = model(X_input_tensor)
    return output.cpu().numpy()

def lime_explain(model, X_input, board_to_matrix):
    # Flatten a matriz 13x8x8 para ser compatível com LIME (1D)
    X_input_flattened = X_input.flatten().cpu().numpy()

    # Ajustar o número de features baseado na entrada achatada
    explainer = lime_tabular.LimeTabularExplainer(
        training_data=np.random.random((1000, X_input_flattened.shape[0])),  # Geração de dados de exemplo
        feature_names=[
            f"channel_{channel} (x={x}, y={y})"
            for i in range(X_input_flattened.shape[0])
            for channel, x, y in [feature_to_channel_position(i, 13, 8, 8)]
        ],  # Nomes descritivos com canal e posição
        mode='regression'  # Modo de regressão, já que estamos prevendo um valor escalar
    )

    # Explicação para uma única instância
    explanation = explainer.explain_instance(
        X_input_flattened,  # Convertido para uma entrada 1D
        lambda x: model_predict(x.reshape(-1, 13, 8, 8), model),  # Redimensionar para (N, 13, 8, 8) para N amostras
        num_features=10  # Número de features a serem explicadas
    )
    
    return explanation

###  LIME ###


### GradCam ###

import torch
import torch.nn.functional as F

def gradcam(model, input_tensor, target_layer_name="conv2"):
    conv_output = None
    gradients = None

    def forward_hook(module, input, output):
        nonlocal conv_output
        conv_output = output

    def backward_hook(module, grad_input, grad_output):
        nonlocal gradients
        gradients = grad_output[0]

    target_layer = dict(model.named_modules())[target_layer_name]
    target_layer.register_forward_hook(forward_hook)
    target_layer.register_backward_hook(backward_hook)

    output = model(input_tensor)
    output.backward()

    pooled_gradients = torch.mean(gradients, dim=[0, 2, 3])
    for i in range(conv_output.shape[1]):
        conv_output[:, i, :, :] *= pooled_gradients[i]

    heatmap = torch.mean(conv_output, dim=1).squeeze().cpu().detach().numpy()
    heatmap = np.maximum(heatmap, 0)
    heatmap /= np.max(heatmap)
    return heatmap


### GradCam ###


### LRP ###

def lrp(model, input_tensor):
    # Propagar o gradiente de saída para entrada usando autograd
    input_tensor.requires_grad_(True)

    output = model(input_tensor)  # Forward pass
    relevance = output.clone()  # Inicializar a relevância como a saída

    #print(f"Initial Output Shape: {output.shape}")
    #print(f"Initial Relevance Shape: {relevance.shape}")

    # Propagar relevância camada a camada
    for idx, layer in enumerate(reversed(list(model.children()))):
        #print(f"Processing Layer: {layer.__class__.__name__}, Current Relevance Shape: {relevance.shape}")
        
        if isinstance(layer, torch.nn.Linear):  # Propagação em camadas densas
            #print(f"Layer {idx}: Linear, Weight Shape: {layer.weight.shape}, Bias Shape: {layer.bias.shape}")
            #print(f"Relevance Before Linear: {relevance.shape}")
            
            # Redistribuir relevância proporcionalmente aos pesos da camada
            relevance = distribute_relevance_to_previous_layer(layer, relevance)
            #print(f"Relevance After Linear: {relevance.shape}")
        
        elif isinstance(layer, torch.nn.Conv2d):  # Propagação em camadas convolucionais
            #print(f"Layer {idx}: Conv2D, Weight Shape: {layer.weight.shape}, Bias Shape: {layer.bias.shape}")
            #print(f"Input Tensor Shape (Conv2D): {input_tensor.shape}")
            relevance = lrp_conv2d(layer, relevance, input_tensor, eps=1e-6)
            #print(f"Relevance After Conv2D: {relevance.shape}")
        
        elif isinstance(layer, torch.nn.ReLU):  # Propagação em ReLU
            #print(f"Layer {idx}: ReLU")
            relevance = F.relu(relevance)  # Garantir que relevância permaneça positiva
            #print(f"Relevance After ReLU: {relevance.shape}")
        elif isinstance(layer, torch.nn.Flatten):  # Ajustar formato para camadas convolucionais
            #print(f"Layer {idx}: Flatten")
            
            # Verificar se o número de elementos é compatível
            expected_size = input_tensor.size(0) * 128 * 8 * 8  # Total de elementos esperado
            actual_size = relevance.numel()  # Total de elementos atual no tensor de relevância

            if actual_size != expected_size:
                #print(f"Current Relevance Shape: {relevance.shape}, Total Elements: {actual_size}")
                
                # Expandir ou redistribuir relevância para atingir o número correto de elementos
                relevance = relevance.expand(-1, expected_size // actual_size).contiguous().view(
                    input_tensor.size(0), 128, 8, 8
                )
            else:
                # Redimensionar para o formato correto se os tamanhos forem compatíveis
                relevance = relevance.view(input_tensor.size(0), 128, 8, 8)
            
            #print(f"Relevance After Flatten: {relevance.shape}")


    # Converter relevância para NumPy e desanexar do gráfico computacional
    relevance = relevance.detach().cpu().numpy()
    #print("Final Relevance Shape:", relevance.shape)
    return relevance

def distribute_relevance_to_previous_layer(layer, relevance):
    """
    Redistribui a relevância da camada superior para as entradas da camada anterior.
    """
    #print(f"Distributing Relevance: Current Relevance Shape {relevance.shape}")
    weights = layer.weight.data
    #print(f"Layer Weights Shape: {weights.shape}")

    # Expandir relevância proporcionalmente aos pesos
    relevance = torch.matmul(relevance, weights.abs())  # Propagar proporcionalmente aos pesos
    #print(f"Distributed Relevance Shape: {relevance.shape}")

    return relevance


def lrp_linear(layer, relevance_output, eps=1e-6):
    """
    Propaga a relevância em camadas lineares.
    """
    #print(f"Entering lrp_linear with Relevance Shape: {relevance_output.shape}")
    
    weights = layer.weight.data
    biases = layer.bias.data if layer.bias is not None else 0

    #print(f"Linear Layer Weights Shape: {weights.shape}, Bias Shape: {biases.shape if biases is not None else 'None'}")
    #print(f"Relevance Output Shape: {relevance_output.shape}")

    # Calcular a relevância proporcional
    z = torch.matmul(relevance_output, weights.T) + biases + eps
    relevance_input = torch.matmul((relevance_output / z), weights)
    #print(f"Relevance Input Shape After Linear: {relevance_input.shape}")
    return relevance_input

def lrp_conv2d(layer, relevance_output, input_tensor, eps=1e-6):
    """
    Propaga a relevância em camadas convolucionais.
    """
    #print(f"Entering lrp_conv2d with Relevance Shape: {relevance_output.shape}")
    #print(f"Conv2D Layer Weight Shape: {layer.weight.shape}, Bias Shape: {layer.bias.shape if layer.bias is not None else 'None'}")
    #print(f"Input Tensor Shape: {input_tensor.shape}")

    weights = layer.weight.data
    bias = layer.bias.data if layer.bias is not None else 0

    # Ajustar canais de relevância para corresponder ao número de canais internos
    if relevance_output.shape[1] != weights.shape[1]:  # Se os canais não coincidirem
        #print("Adjusting relevance channels to match input channels...")
        weight_mapping = weights.sum(dim=(2, 3)).abs()  # Soma sobre kernel (reduzir para [128, 64])
        relevance_output = torch.einsum('bchw,oi->bohw', relevance_output, weight_mapping.T)
        #print(f"Adjusted Relevance Shape (Internal Mapping): {relevance_output.shape}")

    # Mapear relevância para o número de canais da entrada original
    if relevance_output.shape[1] != input_tensor.shape[1]:  # Ajustar para 13 canais
        #print("Mapping relevance channels to match original input channels...")
        relevance_output = relevance_output[:, :input_tensor.shape[1], :, :]  # Ajuste direto para 13 canais
        #print(f"Adjusted Relevance Shape (Input Mapping): {relevance_output.shape}")

    # Reajustar relevância para corresponder aos pesos (64 canais)
    if relevance_output.shape[1] != weights.shape[1]:
        #print("Re-adjusting relevance to match convolution weights...")
        relevance_output = torch.cat([
            relevance_output,
            torch.zeros((relevance_output.size(0), weights.shape[1] - relevance_output.shape[1], *relevance_output.shape[2:]), device=relevance_output.device)
        ], dim=1)
        #print(f"Relevance Shape After Re-adjustment: {relevance_output.shape}")

    # Ajustar o input_tensor para corresponder aos pesos (64 canais)
    if input_tensor.shape[1] != weights.shape[1]:  # Se o input_tensor não tem 64 canais
        #print("Adjusting input_tensor channels to match convolution weights...")
        input_tensor = torch.cat([
            input_tensor,
            torch.zeros((input_tensor.size(0), weights.shape[1] - input_tensor.shape[1], *input_tensor.shape[2:]), device=input_tensor.device)
        ], dim=1)
        #print(f"Input Tensor Shape After Adjustment: {input_tensor.shape}")

    try:
        # Propagação inversa da relevância
        z = F.conv2d(input_tensor, weights, bias=bias, stride=layer.stride, padding=layer.padding) + eps
    except RuntimeError as e:
        #print(f"Error in lrp_conv2d forward convolution: {e}")
        #print(f"Input Tensor Shape: {input_tensor.shape}")
        #print(f"Weight Shape: {weights.shape}")
        raise

    # Ajustar relevância para corresponder aos canais de saída da convolução transposta
    if relevance_output.shape[1] != weights.shape[0]:  # Se não tem 128 canais
        #print("Adjusting relevance for transpose convolution...")
        relevance_output = torch.cat([
            relevance_output,
            torch.zeros((relevance_output.size(0), weights.shape[0] - relevance_output.shape[1], *relevance_output.shape[2:]), device=relevance_output.device)
        ], dim=1)
        #print(f"Relevance Shape After Adjustment for Transpose: {relevance_output.shape}")

    try:
        # Redistribuir relevância proporcional
        relevance_input = F.conv_transpose2d(
            (relevance_output / z), weights, stride=layer.stride, padding=layer.padding
        )
    except RuntimeError as e:
        #print(f"Error in lrp_conv2d transpose convolution: {e}")
        #print(f"Relevance Output Shape: {relevance_output.shape}")
        #print(f"Weight Shape: {weights.shape}")
        raise

    #print(f"Relevance Input Shape After Conv2D: {relevance_input.shape}")
    return relevance_input * input_tensor



### LRP ###

### DeepLIFT ###

import torch
from captum.attr import DeepLift

def deeplift(model, input_tensor):
    model.eval()  # Certifique-se de que o modelo está em modo de avaliação
    deeplift = DeepLift(model)  # Inicializa o objeto DeepLIFT

    # Gera a atribuição DeepLIFT em relação à entrada de referência (matriz de zeros)
    attribution = deeplift.attribute(input_tensor, target=0, baselines=torch.zeros_like(input_tensor))

    return attribution.cpu().detach().numpy()

### DeepLIFT ###


### Saliency MAPS ###

import torch

def saliency_map(model, input_tensor):
    # Configurar o tensor de entrada para permitir o cálculo de gradientes
    input_tensor.requires_grad_()

    # Fazer a previsão do modelo
    output = model(input_tensor)

    # Assumimos que estamos interessados na primeira saída, então faremos backward na primeira saída
    output.backward(torch.ones_like(output))

    # O mapa de saliência é o valor absoluto dos gradientes da entrada
    saliency = input_tensor.grad.abs()

    # Converter para numpy e retornar
    return saliency.detach().cpu().numpy()

### Saliency MAPS ###
