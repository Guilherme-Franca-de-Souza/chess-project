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


###  SHAP ###


import shap

def shap_explain(model, input_tensor):
    explainer = shap.GradientExplainer(model, input_tensor)
    shap_values = explainer.shap_values(input_tensor)
    
    return shap_values


###  SHAP ###


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