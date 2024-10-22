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
        feature_names=[f"feature_{i}" for i in range(X_input_flattened.shape[0])],  # Nominalmente nomeando as features
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

import torch
import matplotlib.pyplot as plt

def lrp(model, input_tensor):
    # Propagar o gradiente de saída para entrada usando autograd
    input_tensor.requires_grad_(True)
    
    output = model(input_tensor)  # Executar o modelo
    output.backward(torch.ones_like(output))  # Calcular gradiente

    relevance = input_tensor.grad * input_tensor  # Calcular relevância

    # Desanexar a relevância do gráfico de gradiente e convertê-la para NumPy
    relevance = relevance.detach().cpu().numpy()

    return relevance

### LRP ###

### DeepLIFT ###

import torch
import numpy as np
import torch.nn.functional as F

def deeplift(model, X_input):
    # Definir a entrada e a referência (baseline de zeros)
    X_input.requires_grad_()
    reference_input = torch.zeros_like(X_input)
    
    # Listas para armazenar as ativações e as ativações da referência
    activations = []
    reference_activations = []

    # Forward pass: Propagar entrada real e referência no modelo
    current_input = X_input
    current_ref_input = reference_input

    for layer in model.children():
        # Ativar a camada com a entrada e a referência
        activation = layer(current_input)
        ref_activation = layer(current_ref_input)
        
        activations.append(activation)
        reference_activations.append(ref_activation)

        current_input = activation
        current_ref_input = ref_activation

    # Lista para armazenar relevâncias
    relevances = []

    for i in range(len(activations)):
        delta_activation = activations[i] - reference_activations[i]
        
        # Gradientes das ativações em relação à entrada
        activations[i].retain_grad()
        activations[i].backward(torch.ones_like(activations[i]), retain_graph=True)
        gradient = activations[i].grad

        # Relevância para essa camada
        relevance = delta_activation * gradient

        # Ajustar dimensões se necessário para concatenar
        if relevance.ndim == 4:
            # A camada é convolucional, mantém as 4 dimensões
            relevances.append(relevance)
        elif relevance.ndim == 2:
            # A camada é totalmente conectada, expande as dimensões e interpola para ajustar
            # Expande para 4D (batch_size, saída, 1, 1)
            relevance = relevance.unsqueeze(-1).unsqueeze(-1)
            # Interpola para o tamanho da camada convolucional anterior (ex: [batch_size, saída, 8, 8])
            target_size = relevances[-1].shape[2:]  # Usa o tamanho da última camada convolucional
            relevance = F.interpolate(relevance, size=target_size, mode='bilinear', align_corners=False)
            relevances.append(relevance)

    # Concatenar relevâncias ao longo da dimensão dos canais (dimensão 1)
    deep_lift_contributions = torch.cat(relevances, dim=1)

    return deep_lift_contributions.detach().numpy()

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
