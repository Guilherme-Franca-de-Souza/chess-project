import pdfplumber
import re

# Define a regex para encontrar siglas (letras maiúsculas com mais de um caractere)
sigla_regex = r'\b[A-Z]{2,}\b'

def extrair_siglas_agrupadas(pdf_path):
    siglas_agrupadas = {}

    # Abre o PDF
    with pdfplumber.open(pdf_path) as pdf:
        # Percorre cada página
        for num_pagina, pagina in enumerate(pdf.pages, start=1):
            texto = pagina.extract_text()
            if not texto:
                continue
            # Divide o texto da página em linhas
            linhas = texto.split('\n')
            for num_linha, linha in enumerate(linhas, start=1):
                # Procura siglas na linha
                siglas = re.findall(sigla_regex, linha)
                for sigla in siglas:
                    if sigla not in siglas_agrupadas:
                        siglas_agrupadas[sigla] = []
                    # Adiciona a página e linha da ocorrência
                    siglas_agrupadas[sigla].append({
                        'pagina': num_pagina,
                        'linha': num_linha,
                    })

    return siglas_agrupadas

# Caminho para o arquivo PDF
pdf_path = "monografia.pdf"

# Extrair as siglas agrupadas
resultado = extrair_siglas_agrupadas(pdf_path)

# Exibir o resultado
for sigla, ocorrencias in resultado.items():
    print(f"Sigla: {sigla}")
    for ocorrencia in ocorrencias:
        print(f"  Página: {ocorrencia['pagina']} - Linha: {ocorrencia['linha']}")