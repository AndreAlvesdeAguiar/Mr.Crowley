import easyocr
from pdf2image import convert_from_path
import pandas as pd
import re
import os

def identificar_tipo_sumario(linha_base, prox_linha):
    linha_base = str(linha_base)  # Converta para string, se ainda não for
    prox_linha = str(prox_linha)  # Converta para string, se ainda não for

    # Defina padrões de expressão regular para cada tipo de sumário
    padrao_tipo1 = re.compile(r"SLOT LIVRE", re.IGNORECASE)
    padrao_tipo2 = re.compile(r"FMF", re.IGNORECASE)
    padrao_tipo3 = re.compile(r"BOLETIM\s*FINANCEIRO", re.IGNORECASE)
    padrao_tipo4 = re.compile(r"(FEDERAÇÃO\s*PARANAENSE\s*DE\s*FUTEBOL|FEDERAÇAO\s*PARANAENSE\s*DE\s*FUTEBOL)", re.IGNORECASE)
    padrao_tipo5 = re.compile(r"(FEDERAÇÃO\s*DE\s*FUTEBOL\s*DO\s*ESTADO\s*DO\s*RIO\s*DE\s*JANEIRO|FE|163|3FE3|ZFER|FB|RIO|FER|JFER|7FE|7F2|F3|FE3|F2)", re.IGNORECASE)
    # Novos tipos adicionados
    padrao_tipo6 = re.compile(r"(CLUB|FEDERACAO\s*BAHIANA\s*DE\s*FUTEBOL|U8)", re.IGNORECASE)
    padrao_tipo7 = re.compile(r"FORTALEZA", re.IGNORECASE)
    padrao_tipo8 = re.compile(r"FEDERACAO\s*MATOGROSSENSE\s*DE\s*FUTEBOL", re.IGNORECASE)
    padrao_tipo9 = re.compile(r"FGF", re.IGNORECASE)
    padrao_tipo9b_curitiba = re.compile(r"4sp", re.IGNORECASE)
    padrao_tipo9b_gaucho = re.compile(r"FEDERACAO\s*GAUCHA\s*DE\s*FUTEBOL", re.IGNORECASE)

    # Verifique se algum padrão corresponde à linha base do texto    
    if padrao_tipo1.search(linha_base):
        return "Tipo 1 - SLOT LIVRE"
    elif padrao_tipo2.search(linha_base):
        return "Tipo 2 - (FEDERACAO MINEIRA DE FUTEBOL)"
    elif padrao_tipo3.search(linha_base):
        return "Tipo 3 - (FEDERACAO PAULISTA DE FUTEBOL)"
    elif padrao_tipo4.search(linha_base):
        return "Tipo 4 - (FEDERACAO PARAENSE DE FUTEBOL)"
    elif padrao_tipo5.search(linha_base):
        return "Tipo 5 - (FEDERACAO DE FUTEBOL DO ESTADO DO RIO DE JANEIRO)"
    elif padrao_tipo6.search(linha_base):
        return "Tipo 6 - (FEDERACAO BAHIANA DE FUTEBOL)"
    elif padrao_tipo7.search(linha_base):
        return "Tipo 7 - (FEDERACAO CEARENSE DE FUTEBOL)"
    elif padrao_tipo8.search(linha_base):
        return "Tipo 8 - (FEDERACAO MATOGROSSENSE DE FUTEBOL)"
    elif padrao_tipo9.search(linha_base):
        if padrao_tipo9b_curitiba.search(prox_linha):
            return "Tipo 9 (FEDERACAO GOIANA DE FUTEBOL)"
        elif padrao_tipo9b_gaucho.search(prox_linha):
            return "Tipo 9 (FEDERACAO GAUCHA DE FUTEBOL)"
        else:
            return "Tipo 9 (TIPO NÃO MAPEADO LINHA[1])"
    else:
        return "TIPO NAO MAPEADO"

# Caminho para a pasta contendo os arquivos PDF de jogos
pasta_pdf = '/home/andre/Downloads/raspagem/sandbox'

# Inicializar EasyOCR
reader = easyocr.Reader(['pt']) # Especifique o idioma

resultados = []

# Iterar sobre todos os arquivos na pasta
for arquivo_pdf in os.listdir(pasta_pdf):
    if arquivo_pdf.endswith('.pdf'):
        caminho_pdf = os.path.join(pasta_pdf, arquivo_pdf)
        
        # Extrair texto das duas primeiras páginas do PDF
        imagens = convert_from_path(caminho_pdf, first_page=1, last_page=2)
        dados = []
        for imagem in imagens:
            imagem.save('temp.png')  # Salvar a imagem temporariamente
            resultado = reader.readtext('temp.png')  # Fornecer o caminho da imagem
            for (bbox, text, prob) in resultado:
                dados.append(text)

        # Pegar apenas a primeira e segunda linha do texto extraído
        primeira_linha = dados[0] if dados else ""
        segunda_linha = dados[1] if len(dados) > 1 else ""

        # Identificar o tipo de sumário
        tipo_sumario = identificar_tipo_sumario(primeira_linha, segunda_linha)
        
        # Adicionar resultado à lista de resultados
        # Adicionar resultado à lista de resultados
        if "Tipo 5 - (FEDERACAO DE FUTEBOL DO ESTADO DO RIO DE JANEIRO)" in tipo_sumario:
            prox_linha2 = dados[3]
            C = dados[5]
            resultados.append({'Jogo': arquivo_pdf, 'Tipo de Sumário': tipo_sumario, 'Próxima Linha': prox_linha2, 'C': C})
        elif "Tipo 6 - (FEDERACAO BAHIANA DE FUTEBOL)" in tipo_sumario:
            prox_linha2 = dados[3]  # Altere para o índice correto conforme necessário
            C = dados[5]  # Altere para o índice correto conforme necessário
            resultados.append({'Jogo': arquivo_pdf, 'Tipo de Sumário': tipo_sumario, 'Próxima Linha': prox_linha2, 'C': C})
        elif "Tipo 7 - (FEDERACAO CEARENSE DE FUTEBOL)" in tipo_sumario:
            prox_linha2 = dados[3]  # Altere para o índice correto conforme necessário
            C = dados[5]  # Altere para o índice correto conforme necessário
            resultados.append({'Jogo': arquivo_pdf, 'Tipo de Sumário': tipo_sumario, 'Próxima Linha': prox_linha2, 'C': C})
        elif "Tipo 8 - (FEDERACAO MATOGROSSENSE DE FUTEBOL)" in tipo_sumario:
            prox_linha2 = dados[3]  # Altere para o índice correto conforme necessário
            C = dados[5]  # Altere para o índice correto conforme necessário
            resultados.append({'Jogo': arquivo_pdf, 'Tipo de Sumário': tipo_sumario, 'Próxima Linha': prox_linha2, 'C': C})
        elif "Tipo 9 (FEDERACAO GOIANA DE FUTEBOL)" in tipo_sumario:
            prox_linha2 = dados[3]  # Altere para o índice correto conforme necessário
            C = dados[5]  # Altere para o índice correto conforme necessário
            resultados.append({'Jogo': arquivo_pdf, 'Tipo de Sumário': tipo_sumario, 'Próxima Linha': prox_linha2, 'C': C})
        elif "Tipo 9 (FEDERACAO GAUCHA DE FUTEBOL)" in tipo_sumario:
            prox_linha2 = dados[3]  # Altere para o índice correto conforme necessário
            C = dados[5]  # Altere para o índice correto conforme necessário
            resultados.append({'Jogo': arquivo_pdf, 'Tipo de Sumário': tipo_sumario, 'Próxima Linha': prox_linha2, 'C': C})
        elif "Tipo 4 - (FEDERACAO PARAENSE DE FUTEBOL)" in tipo_sumario:
            prox_linha2 = dados[3]  # Altere para o índice correto conforme necessário
            C = dados[5]  # Altere para o índice correto conforme necessário
            resultados.append({'Jogo': arquivo_pdf, 'Tipo de Sumário': tipo_sumario, 'Próxima Linha': prox_linha2, 'C': C})
        elif "Tipo 3 - (FEDERACAO PAULISTA DE FUTEBOL)" in tipo_sumario:
            prox_linha2 = dados[3]  # Altere para o índice correto conforme necessário
            C = dados[5]  # Altere para o índice correto conforme necessário
            resultados.append({'Jogo': arquivo_pdf, 'Tipo de Sumário': tipo_sumario, 'Próxima Linha': prox_linha2, 'C': C})
        elif "Tipo 2 - (FEDERACAO MINEIRA DE FUTEBOL)" in tipo_sumario:
            prox_linha2 = dados[3]  # Altere para o índice correto conforme necessário
            C = dados[5]  # Altere para o índice correto conforme necessário
            resultados.append({'Jogo': arquivo_pdf, 'Tipo de Sumário': tipo_sumario, 'Próxima Linha': prox_linha2, 'C': C})
        else:
            resultados.append({'Jogo': arquivo_pdf, 'Tipo de Sumário': tipo_sumario})

# Exportar lista de resultados para um arquivo Excel
nome_arquivo_excel = 'sandbox.xlsx'

df_resultados = pd.DataFrame(resultados)
df_resultados.to_excel(nome_arquivo_excel, index=False)

print(f'Resultados exportados como "{nome_arquivo_excel}"')
