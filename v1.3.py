import easyocr
from pdf2image import convert_from_path
import pandas as pd
import re
import os

def identificar_tipo_sumario(linha_base):
    linha_base = str(linha_base)  # Converta para string, se ainda não for

    # Defina padrões de expressão regular para cada tipo de sumário
    padrao_tipo1 = re.compile(r"FEDERAÇÃO\s*PARANAENSE\s*DE\s*FUTEBOL", re.IGNORECASE)
    padrao_tipo2 = re.compile(r"FMF", re.IGNORECASE)
    padrao_tipo3 = re.compile(r"BOLETIM\s*FINANCEIRO", re.IGNORECASE)
    padrao_tipo4 = re.compile(r"FEDERAÇÃO\s*PARANAENSE\s*DE\s*FUTEBOL", re.IGNORECASE)
    padrao_tipo5 = re.compile(r"FEDERAÇÃO\s*DE\s*FUTEBOL\s*DO\s*ESTADO\s*DO\s*RIO\s*DE\s*JANEIRO", re.IGNORECASE)

    # Verifique se algum padrão corresponde à linha base do texto    
    if padrao_tipo1.search(linha_base):
        return "Tipo 1"
    elif padrao_tipo2.search(linha_base):
        return "Tipo 2"
    elif padrao_tipo3.search(linha_base):
        return "Tipo 3"
    elif padrao_tipo4.search(linha_base):
        return "Tipo 4"
    elif padrao_tipo5.search(linha_base):
        return "Tipo 5"
    else:
        return "TIPO NAO MAPEADO"

# Caminho para a pasta contendo os arquivos PDF de jogos
pasta_pdf = '/home/andre/Downloads/raspagem/2023/'

# Inicializar EasyOCR
reader = easyocr.Reader(['pt']) # Especifique o idioma

resultados = []

# Iterar sobre todos os arquivos na pasta
for arquivo_pdf in os.listdir(pasta_pdf):
    if arquivo_pdf.endswith('.pdf'):
        caminho_pdf = os.path.join(pasta_pdf, arquivo_pdf)
        
        # Extrair texto da primeira página do PDF
        imagens = convert_from_path(caminho_pdf, first_page=1, last_page=1)
        dados = []
        for imagem in imagens:
            imagem.save('temp.png')  # Salvar a imagem temporariamente
            resultado = reader.readtext('temp.png')  # Fornecer o caminho da imagem
            if resultado:
                bbox, text, prob = resultado[0]  # Pegar apenas a primeira linha
                dados.append(text)

        # Pegar apenas a primeira linha do texto extraído
        primeira_linha = dados[0] if dados else ""
        
        # Identificar o tipo de sumário
        tipo_sumario = identificar_tipo_sumario(primeira_linha)
        
        # Adicionar resultado à lista de resultados
        resultados.append({'Jogo': arquivo_pdf, 'Tipo de Sumário': tipo_sumario})

# Exportar lista de resultados para um arquivo Excel
nome_arquivo_excel = 'resultados_excel.xlsx'

df_resultados = pd.DataFrame(resultados)
df_resultados.to_excel(nome_arquivo_excel, index=False)

print(f'Resultados exportados como "{nome_arquivo_excel}"')
