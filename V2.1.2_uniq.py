import easyocr
from pdf2image import convert_from_path
import pandas as pd
import re
import os

# Caminho para o arquivo PDF
caminho_pdf = '/home/andre/Downloads/raspagem/2023/jogo_1.pdf'

# Extrair imagens das páginas do PDF
imagens = convert_from_path(caminho_pdf)

# Inicializar EasyOCR
reader = easyocr.Reader(['pt']) # Especifique o idioma

dados = []

# Processar cada imagem e extrair texto entre chaves
for imagem in imagens:
    imagem.save('temp.png')  # Salvar a imagem temporariamente
    resultado = reader.readtext('temp.png')  # Fornecer o caminho da imagem
    for (bbox, text, prob) in resultado:
        dados.append(text)

df = pd.DataFrame(dados)

linha_base = df.iloc[0]
prox_linha = df.iloc[1]

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
##---------------------------------------------------------------------------------------------------------------------------##
    if padrao_tipo1.search(linha_base):
        prox_linha2 = dados[3]
        C = dados[5]
        D = dados[6]
        tipo_sumario = "Tipo 1 - SLOT LIVRE"
##---------------------------------------------------------------------------------------------------------------------------##
    elif padrao_tipo2.search(linha_base):
        prox_linha2 = dados[3]  # Altere para o índice correto conforme necessário
        C = dados[5]  # Altere para o índice correto conforme necessário
        D = dados[6]

        palavra_procurada = "RECEITA"
        for linha_numero, linha_base in enumerate(dados, start=1):
            linha_base = str(linha_base)  # Converta para string, se ainda não for
                
            # Verifique se a palavra "RECEITA" está presente na linha
            if palavra_procurada in linha_base:
                print(f"A palavra '{palavra_procurada}' foi encontrada na linha {linha_numero}:")
                print(linha_base)
    
        tipo_sumario = "Tipo 2 - (FEDERACAO MINEIRA DE FUTEBOL)"
##---------------------------------------------------------------------------------------------------------------------------##      
    elif padrao_tipo3.search(linha_base):
        prox_linha2 = dados[3]  # Altere para o índice correto conforme necessário
        C = dados[5]  # Altere para o índice correto conforme necessário
        D = dados[6]

        palavra_procurada = "RECEITA"
        for linha_numero, linha_base in enumerate(dados, start=1):
            linha_base = str(linha_base)  # Converta para string, se ainda não for
                
            # Verifique se a palavra "RECEITA" está presente na linha
            if palavra_procurada in linha_base:
                print(f"A palavra '{palavra_procurada}' foi encontrada na linha {linha_numero}:")
                print(linha_base)
        tipo_sumario = "Tipo 3 - (FEDERACAO PAULISTA DE FUTEBOL)"
##---------------------------------------------------------------------------------------------------------------------------##
    elif padrao_tipo4.search(linha_base):
        prox_linha2 = dados[3]  # Altere para o índice correto conforme necessário
        C = dados[5]  # Altere para o índice correto conforme necessário
        D = dados[6]

        palavra_procurada = "RECEITA"
        
        for linha_numero, linha_base in enumerate(dados, start=1):
            linha_base = str(linha_base)  # Converta para string, se ainda não for
                
            # Verifique se a palavra "RECEITA" está presente na linha
            if palavra_procurada in linha_base:
                print(f"A palavra '{palavra_procurada}' foi encontrada na linha {linha_numero}:")
                print(linha_base)
        tipo_sumario = "Tipo 4 - (FEDERACAO PARAENSE DE FUTEBOL)"
##---------------------------------------------------------------------------------------------------------------------------##
    elif padrao_tipo5.search(linha_base):
        prox_linha2 = dados[3]  # Altere para o índice correto conforme necessário
        C = dados[5]  # Altere para o índice correto conforme necessário
        D = dados[6]
    
        palavra_procurada = "RECEITA"
        palavra_procurada2 = "JOGO:"
    
        for linha_numero, linha_base in enumerate(dados, start=1):
            linha_base = str(linha_base)  # Converta para string, se ainda não for
                        
            if palavra_procurada in linha_base:
                print(f"A palavra '{palavra_procurada}' foi encontrada na linha {linha_numero}:")
                ref4 = linha_numero + 1
                print(linha_base)
                ref5 = dados[ref4]
                print(ref5)
                break
                     
            if palavra_procurada2 in linha_base:
                # print(f"A palavra '{palavra_procurada2}' foi encontrada na linha {linha_numero}:")
                ref = linha_numero  # Convertendo linha_base para um número e adicionando 1
                ref1 = linha_numero + 2
                ref2 = dados[ref]
                ref3 = dados[ref1]
    
                print(f"Mandante'{ref2}' Visitante '{ref3}':")
    
        tipo_sumario = "Tipo 5 - (FEDERACAO DE FUTEBOL DO ESTADO DO RIO DE JANEIRO)"
##---------------------------------------------------------------------------------------------------------------------------##
    elif padrao_tipo6.search(linha_base):
        prox_linha2 = dados[3]  # Altere para o índice correto conforme necessário
        C = dados[5]  # Altere para o índice correto conforme necessário
        D = dados[6]

        palavra_procurada = "RECEITA"
        for linha_numero, linha_base in enumerate(dados, start=1):
            linha_base = str(linha_base)  # Converta para string, se ainda não for
                
            # Verifique se a palavra "RECEITA" está presente na linha
            if palavra_procurada in linha_base:
                print(f"A palavra '{palavra_procurada}' foi encontrada na linha {linha_numero}:")
                print(linha_base)
        tipo_sumario = "Tipo 6 - (FEDERACAO BAHIANA DE FUTEBOL)"
##---------------------------------------------------------------------------------------------------------------------------##
    elif padrao_tipo7.search(linha_base):
        prox_linha2 = dados[3]  # Altere para o índice correto conforme necessário
        C = dados[5]  # Altere para o índice correto conforme necessário
        D = dados[6]

        palavra_procurada = " RECEITA "
        for linha_numero, linha_base in enumerate(dados, start=1):
            linha_base = str(linha_base)  # Converta para string, se ainda não for
                
            # Verifique se a palavra "RECEITA" está presente na linha
            if palavra_procurada in linha_base:
                print(f"A palavra '{palavra_procurada}' foi encontrada na linha {linha_numero}:")
                print(linha_base)
        tipo_sumario = "Tipo 7 - (FEDERACAO CEARENSE DE FUTEBOL)"
##---------------------------------------------------------------------------------------------------------------------------##
    elif padrao_tipo8.search(linha_base):
        prox_linha2 = dados[3]  # Altere para o índice correto conforme necessário
        C = dados[5]  # Altere para o índice correto conforme necessário
        D = dados[6]

        palavra_procurada = "RECEITA"
        for linha_numero, linha_base in enumerate(dados, start=1):
            linha_base = str(linha_base)  # Converta para string, se ainda não for
                
            # Verifique se a palavra "RECEITA" está presente na linha
            if palavra_procurada[0] in linha_base:
                print(f"A palavra '{palavra_procurada}' foi encontrada na linha {linha_numero}:")
                print(linha_base)
        tipo_sumario = "Tipo 8 - (FEDERACAO MATOGROSSENSE DE FUTEBOL)"
##---------------------------------------------------------------------------------------------------------------------------##
    elif padrao_tipo9.search(linha_base):
        if padrao_tipo9b_curitiba.search(prox_linha):
            prox_linha2 = dados[3]  # Altere para o índice correto conforme necessário
            C = dados[5]  # Altere para o índice correto conforme necessário
            D = dados[6]


            tipo_sumario = "Tipo 9 (FEDERACAO GOIANA DE FUTEBOL)"
##---------------------------------------------------------------------------------------------------------------------------##
        elif padrao_tipo9b_gaucho.search(prox_linha):
            prox_linha2 = dados[3]  # Altere para o índice correto conforme necessário
            C = dados[5]  # Altere para o índice correto conforme necessário
            D = dados[6]
            tipo_sumario = "Tipo 9 (FEDERACAO GAUCHA DE FUTEBOL)"
        else:
            tipo_sumario = "Tipo 9 (TIPO NÃO MAPEADO LINHA[1])"
    else:
        tipo_sumario = "TIPO NAO MAPEADO"
##---------------------------------------------------------------------------------------------------------------------------##
    return tipo_sumario

tipo_sumario = identificar_tipo_sumario(linha_base, prox_linha)
print("Tipo de Sumário:", tipo_sumario)

print("Dataframe")
pd.set_option('display.max_rows', None)  # Altere o número conforme necessário
print(df)
