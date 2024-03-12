#DOWNLOAD TROQUE PARA O ANO EM QUESTÃO.:.

import os
import requests

PDF_FOLDER_PATH = "/home/andre/Downloads/raspagem/2021/"

def download_pdf_file(url: str) -> bool:
    # Request URL and get response object
    response = requests.get(url, stream=True)

    # Isolate PDF filename from URL
    pdf_file_name = f"jogo_{os.path.basename(url)[3:]}".replace("b", "")

    if response.status_code == 200:
        # Save in PDF_FOLDER_PATH
        path = PDF_FOLDER_PATH
        filepath = os.path.join(path, pdf_file_name)

        with open(filepath, "wb") as pdf_object:
            pdf_object.write(response.content)
            print(f"{pdf_file_name} was successfully saved!")
            return True
    else:
        print(f"Uh oh! Could not download {pdf_file_name},")
        print(f"HTTP response status code: {response.status_code}")
        return False

def main():
    # Define o número inicial e final das partidas
    partida_inicial = 1
    partida_final = 380

    for partida in range(partida_inicial, partida_final + 1):
        URL = f"https://conteudo.cbf.com.br/sumulas/2023/142{partida}b.pdf"
        download_pdf_file(URL)

if __name__ == "__main__":
    main()

#------> https://conteudo.cbf.com.br/sumulas/2023/1421b.pdf
#                           (1..380)
#------> https://conteudo.cbf.com.br/sumulas/2023/142380b.pdf
#
#--<ref .:. https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/2023>



# EXTRAÇÃO VIA OCR


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
pasta_pdf = '/home/andre/Downloads/raspagem/2023'

# Inicializar EasyOCR
reader = easyocr.Reader(['pt']) # Especifique o idioma

resultados = []
# ref2 = ""
# ref4 = ""

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
        if "Tipo 5 - (FEDERACAO DE FUTEBOL DO ESTADO DO RIO DE JANEIRO)" in tipo_sumario:
            # prox_linha2 = dados[3]
            # C = dados[5]

            # Definir ref2 e ref4 com base nos dados extraídos
            palavra_procurada = "RECEITA"
            palavra_procurada2 = "JOGO:"
            palavra_procurada3 = "ESTÁDIO"

            for linha_numero, linha_base in enumerate(dados, start=1):
                linha_base = str(linha_base)  # Converta para string, se ainda não for
                            
                if palavra_procurada in linha_base:
                    print(f"A palavra '{palavra_procurada}' foi encontrada na linha {linha_numero}:")
                    ref4 = linha_numero + 1
                    ref6 = linha_numero - 2
                    ref8 = linha_numero - 3
                    ref10 = linha_numero - 4
                    print(linha_base)
                    ref5 = dados[ref4]
                    ref7 = dados[ref6]
                    ref9 = dados[ref8]
                    ref11 = dados[ref10]
                    print(f"UTILIZADOS: '{ref7}', DEVOLVIDOS: '{ref9}', DISPONIVEL: '{ref11}'")
                    break
                         
                if palavra_procurada2 in linha_base:
                    # print(f"A palavra '{palavra_procurada2}' foi encontrada na linha {linha_numero}:")
                    ref = linha_numero  # Convertendo linha_base para um número e adicionando 1
                    ref1 = linha_numero + 2
                    ref2 = dados[ref]
                    ref3 = dados[ref1]
        
                    print(f"Mandante'{ref2}' Visitante '{ref3}':")

                    # ref14 = linha_numero + 8
                    ref15 = dados[3]
                    print(f"DATA: '{ref15}'")


                if palavra_procurada3 in linha_base:
                    ref12 = linha_numero - 1
                    ref13 = dados[ref12]
                    print(f"ESTADIO: '{ref13}'")

                
                        
            resultados.append({'Jogo': arquivo_pdf, 'Tipo de Sumário': tipo_sumario, 'Data': ref15,
                               'Mandante': ref2, 'Visitante': ref3, 'ARRECADAÇÃO': ref5, 'UTILIZADOS': ref7, 'DEVOLVIDOS': ref9,
                               'DISPONIVEL': ref11, 'ESTADIO': ref13})

            tipo_sumario = "Tipo 5 - (FEDERACAO DE FUTEBOL DO ESTADO DO RIO DE JANEIRO)"


        elif "Tipo 6 - (FEDERACAO BAHIANA DE FUTEBOL)" in tipo_sumario:
            # prox_linha2 = dados[3]  # Altere para o índice correto conforme necessário
            # C = dados[5]  # Altere para o índice correto conforme necessário

            palavra_procurada3 = "ESTÁDIO"
            palavra_procurada2 = "TOTAL"
            
            for linha_numero, linha_base in enumerate(dados, start=1):
                linha_base = str(linha_base)  # Converta para string, se ainda não for
        
                if palavra_procurada2 in linha_base:
                    print(f"A palavra '{palavra_procurada2}' foi encontrada na linha {linha_numero}:")
                    ref6 = linha_numero
                    ref8 = linha_numero + 1
                    ref10 = linha_numero + 2
                    print(linha_base)
                    ref7 = dados[ref6]
                    ref9 = dados[ref8]
                    ref11 = dados[ref10]
                    # print(ref7)
                    print(f"DISPONIVEIS: '{ref7}', VENDIDOS: '{ref9}', DEVOLVIDOS: '0', ARRECADAÇÃO: '{ref11}'")
                    break
                
                if palavra_procurada3 in linha_base:
                    ref12 = linha_numero
                    ref13 = dados[ref12]
                    print(f"ESTADIO: '{ref13}'")
                    
                    ref14 = linha_numero + 8
                    ref15 = dados[ref14]
                    print(f"DATA: '{ref15}'")
        
                    ref16 = linha_numero + 4
                    ref17 = dados[ref16]
                    print(f"MANDANTE: '{ref17}'")
        
                    ref18 = linha_numero + 5
                    ref19 = dados[ref18]
                    print(f"VISITANTES: '{ref19}'")
                

            resultados.append({'Jogo': arquivo_pdf, 'Tipo de Sumário': tipo_sumario, 'Data': ref15,
                               'Mandante': ref17, 'Visitante': ref19, 'ARRECADAÇÃO': ref11, 'UTILIZADOS': ref9, 'DEVOLVIDOS': "0",
                               'DISPONIVEL': ref7, 'ESTADIO': ref13})

            tipo_sumario = "Tipo 6 - (FEDERACAO BAHIANA DE FUTEBOL)"


        elif "Tipo 7 - (FEDERACAO CEARENSE DE FUTEBOL)" in tipo_sumario:
            # prox_linha2 = dados[3]  # Altere para o índice correto conforme necessário
            # C = dados[5]  # Altere para o índice correto conforme necessário

            palavra_procurada3 = "ESTÁDIO"
            palavra_procurada2 = "TOTAL"
            
            for linha_numero, linha_base in enumerate(dados, start=1):
                linha_base = str(linha_base)  # Converta para string, se ainda não for
        
                if palavra_procurada2 in linha_base:
                    print(f"A palavra '{palavra_procurada2}' foi encontrada na linha {linha_numero}:")
                    ref6 = linha_numero
                    ref8 = linha_numero + 1
                    ref10 = linha_numero + 2
                    print(linha_base)
                    ref7 = dados[ref6]
                    ref9 = dados[ref8]
                    ref11 = dados[ref10]
                    # print(ref7)
                    print(f"DISPONIVEIS: '{ref7}', VENDIDOS: '{ref9}', DEVOLVIDOS: '0', ARRECADAÇÃO: '{ref11}'")
                    break
                
                if palavra_procurada3 in linha_base:
                    ref12 = linha_numero
                    ref13 = dados[ref12]
                    print(f"ESTADIO: '{ref13}'")
                    
                    ref14 = linha_numero + 7
                    ref15 = dados[ref14]
                    print(f"DATA: '{ref15}'")
    
                    ref16 = linha_numero + 3
                    ref17 = dados[ref16]
                    print(f"MANDANTE: '{ref17}'")
    
                    ref18 = linha_numero + 4
                    ref19 = dados[ref18]
                    print(f"VISITANTES: '{ref19}'")
                    

            resultados.append({'Jogo': arquivo_pdf, 'Tipo de Sumário': tipo_sumario, 'Data': ref15,
                               'Mandante': ref17, 'Visitante': ref19, 'ARRECADAÇÃO': ref11, 'UTILIZADOS': ref9, 'DEVOLVIDOS': "0",
                               'DISPONIVEL': ref7, 'ESTADIO': ref13})
            tipo_sumario = "Tipo 7 - (FEDERACAO CEARENSE DE FUTEBOL)"
            
        elif "Tipo 8 - (FEDERACAO MATOGROSSENSE DE FUTEBOL)" in tipo_sumario:
    
            palavra_procurada3 = "ESTÁDIO"
            palavra_procurada2 = "TOTAL"
        
            for linha_numero, linha_base in enumerate(dados, start=1):
                linha_base = str(linha_base)  # Converta para string, se ainda não for
    
                if palavra_procurada2 in linha_base:
                    print(f"A palavra '{palavra_procurada2}' foi encontrada na linha {linha_numero}:")
                    ref6 = linha_numero
                    ref8 = linha_numero + 1
                    ref10 = linha_numero + 2
                    print(linha_base)
                    ref7 = dados[ref6]
                    ref9 = dados[ref8]
                    ref11 = dados[ref10]
                    # print(ref7)
                    print(f"DISPONIVEIS: '{ref7}', VENDIDOS: '{ref9}', DEVOLVIDOS: '0', ARRECADAÇÃO: '{ref11}'")
                    break
                
                if palavra_procurada3 in linha_base:
                    ref12 = linha_numero
                    ref13 = dados[ref12]
                    print(f"ESTADIO: '{ref13}'")
                    
                    ref14 = linha_numero + 7
                    ref15 = dados[ref14]
                    print(f"DATA: '{ref15}'")
    
                    ref16 = linha_numero + 3
                    ref17 = dados[ref16]
                    print(f"MANDANTE: '{ref17}'")
    
                    ref18 = linha_numero + 4
                    ref19 = dados[ref18]
                    print(f"VISITANTES: '{ref19}'")
                    
            resultados.append({'Jogo': arquivo_pdf, 'Tipo de Sumário': tipo_sumario, 'Data': ref15,
                               'Mandante': ref17, 'Visitante': ref19, 'ARRECADAÇÃO': ref11, 'UTILIZADOS': ref9, 'DEVOLVIDOS': "0",
                               'DISPONIVEL': ref7, 'ESTADIO': ref13})

            tipo_sumario = "Tipo 8 - (FEDERACAO MATOGROSSENSE DE FUTEBOL)"

        elif "Tipo 9 (FEDERACAO GOIANA DE FUTEBOL)" in tipo_sumario:

            palavra_procurada3 = "ESTÁDIO"
            palavra_procurada2 = "TOTAL"
            
            for linha_numero, linha_base in enumerate(dados, start=1):
                linha_base = str(linha_base)  # Converta para string, se ainda não for
    
                if palavra_procurada2 in linha_base:
                    print(f"A palavra '{palavra_procurada2}' foi encontrada na linha {linha_numero}:")
                    ref6 = linha_numero
                    ref8 = linha_numero + 1
                    ref10 = linha_numero + 2
                    print(linha_base)
                    ref7 = dados[ref6]
                    ref9 = dados[ref8]
                    ref11 = dados[ref10]
                    # print(ref7)
                    print(f"DISPONIVEIS: '{ref7}', VENDIDOS: '{ref9}', DEVOLVIDOS: '0', ARRECADAÇÃO: '{ref11}'")
                    break
                
                if palavra_procurada3 in linha_base:
                    ref12 = linha_numero
                    ref13 = dados[ref12]
                    print(f"ESTADIO: '{ref13}'")
                    
                    ref14 = linha_numero + 8
                    ref15 = dados[ref14]
                    print(f"DATA: '{ref15}'")
    
                    ref16 = linha_numero + 4
                    ref17 = dados[ref16]
                    print(f"MANDANTE: '{ref17}'")
    
                    ref18 = linha_numero + 5
                    ref19 = dados[ref18]
                    print(f"VISITANTES: '{ref19}'")
            
            resultados.append({'Jogo': arquivo_pdf, 'Tipo de Sumário': tipo_sumario, 'Data': ref15,
                               'Mandante': ref17, 'Visitante': ref19, 'ARRECADAÇÃO': ref11, 'UTILIZADOS': ref9, 'DEVOLVIDOS': "0",
                               'DISPONIVEL': ref7, 'ESTADIO': ref13})

            tipo_sumario = "Tipo 9 (FEDERACAO GOIANA DE FUTEBOL)" 

        
        elif "Tipo 9 (FEDERACAO GAUCHA DE FUTEBOL)" in tipo_sumario:

            palavra_procurada3 = "ESTÁDIO"
            palavra_procurada2 = "TOTAL"
        
            for linha_numero, linha_base in enumerate(dados, start=1):
                linha_base = str(linha_base)  # Converta para string, se ainda não for
    
                if palavra_procurada2 in linha_base:
                    print(f"A palavra '{palavra_procurada2}' foi encontrada na linha {linha_numero}:")
                    ref6 = linha_numero
                    ref8 = linha_numero + 1
                    ref10 = linha_numero + 2
                    print(linha_base)
                    ref7 = dados[ref6]
                    ref9 = dados[ref8]
                    ref11 = dados[ref10]
                    # print(ref7)
                    print(f"DISPONIVEIS: '{ref7}', VENDIDOS: '{ref9}', DEVOLVIDOS: '0', ARRECADAÇÃO: '{ref11}'")
                    break
                
                if palavra_procurada3 in linha_base:
                    ref12 = linha_numero
                    ref13 = dados[ref12]
                    print(f"ESTADIO: '{ref13}'")
                    
                    ref14 = linha_numero + 8
                    ref15 = dados[ref14]
                    print(f"DATA: '{ref15}'")
    
                    ref16 = linha_numero + 4
                    ref17 = dados[ref16]
                    print(f"MANDANTE: '{ref17}'")
    
                    ref18 = linha_numero + 5
                    ref19 = dados[ref18]
                    print(f"VISITANTES: '{ref19}'")

            resultados.append({'Jogo': arquivo_pdf, 'Tipo de Sumário': tipo_sumario, 'Data': ref15,
                               'Mandante': ref17, 'Visitante': ref19, 'ARRECADAÇÃO': ref11, 'UTILIZADOS': ref9, 'DEVOLVIDOS': "0",
                               'DISPONIVEL': ref7, 'ESTADIO': ref13})

            tipo_sumario = "Tipo 9 (FEDERACAO GAUCHA DE FUTEBOL)" 

        
        elif "Tipo 4 - (FEDERACAO PARAENSE DE FUTEBOL)" in tipo_sumario:
            
            palavra_procurada3 = "Local:"
            palavra_procurada2 = "RECEITA BRUTA"
            
            for linha_numero, linha_base in enumerate(dados, start=1):
                linha_base = str(linha_base)  # Converta para string, se ainda não for
    
                if palavra_procurada2 in linha_base:
                    print(f"A palavra '{palavra_procurada2}' foi encontrada na linha {linha_numero}:")
                    ref6 = linha_numero - 3
                    ref8 = linha_numero - 2
                    ref10 = linha_numero
                    print(linha_base)
                    ref7 = dados[ref6]
                    ref9 = dados[ref8]
                    ref11 = dados[ref10]
                    # print(ref7)
                    print(f"DISPONIVEIS: '{ref7}', VENDIDOS: '{ref9}', DEVOLVIDOS: '0', ARRECADAÇÃO: '{ref11}'")
                    break
                
                if palavra_procurada3 in linha_base:
                    ref12 = linha_numero - 1
                    ref13 = dados[ref12]
                    print(f"ESTADIO: '{ref13}'")
                    
                    ref14 = linha_numero - 4
                    ref15 = dados[ref14]
                    print(f"DATA: '{ref15}'")
    
                    ref16 = linha_numero - 9
                    ref17 = dados[ref16]
                    print(f"MANDANTE: '{ref17}'")
    
                    ref18 = linha_numero - 7
                    ref19 = dados[ref18]
                    print(f"VISITANTES: '{ref19}'")
            
            resultados.append({'Jogo': arquivo_pdf, 'Tipo de Sumário': tipo_sumario, 'Data': ref15,
                               'Mandante': ref17, 'Visitante': ref19, 'ARRECADAÇÃO': ref11, 'UTILIZADOS': ref9, 'DEVOLVIDOS': "0",
                               'DISPONIVEL': ref7, 'ESTADIO': ref13})

            tipo_sumario = "Tipo 4 - (FEDERACAO PARAENSE DE FUTEBOL)"
            
        elif "Tipo 3 - (FEDERACAO PAULISTA DE FUTEBOL)" in tipo_sumario:
            
            palavra_procurada3 = "ESTÁDIO"
            palavra_procurada2 = "TOTAIS"
                
            for linha_numero, linha_base in enumerate(dados, start=1):
                linha_base = str(linha_base)  # Converta para string, se ainda não for
    
    
                
                if palavra_procurada3 in linha_base:
                    print(f"A palavra '{palavra_procurada3}' foi encontrada na linha {linha_numero}:")
                    ref12 = linha_numero + 1
                    ref13 = dados[ref12]
                    print(f"ESTADIO: '{ref13}'")
                    
                    ref14 = linha_numero - 2
                    ref15 = dados[ref14]
                    print(f"DATA: '{ref15}'")
    
                    ref16 = linha_numero
                    ref17 = dados[ref16]
                    print(f"MANDANTE: '{ref17}'")
    
                    ref18 = linha_numero
                    ref19 = dados[ref18]
                    print(f"VISITANTES: '{ref19}'")
                
                if palavra_procurada2 in linha_base:
                    print(f"A palavra '{palavra_procurada2}' foi encontrada na linha {linha_numero}:")
                    ref6 = linha_numero
                    ref8 = linha_numero + 1
                    ref10 = linha_numero + 3
                    print(linha_base)
                    ref7 = dados[ref6]
                    ref9 = dados[ref8]
                    ref11 = dados[ref10]
                    # print(ref7)
                    print(f"DISPONIVEIS: '{ref7}', VENDIDOS: '{ref9}', DEVOLVIDOS: '0', ARRECADAÇÃO: '{ref11}'")
                    break
                    
            tipo_sumario = "Tipo 3 - (FEDERACAO PAULISTA DE FUTEBOL)"
                    
            resultados.append({'Jogo': arquivo_pdf, 'Tipo de Sumário': tipo_sumario, 'Data': ref15,
                               'Mandante': ref17, 'Visitante': ref19, 'ARRECADAÇÃO': ref11, 'UTILIZADOS': ref9, 'DEVOLVIDOS': "0",
                               'DISPONIVEL': ref7, 'ESTADIO': ref13})

            tipo_sumario = "Tipo 3 - (FEDERACAO PAULISTA DE FUTEBOL)"
            
        elif "Tipo 2 - (FEDERACAO MINEIRA DE FUTEBOL)" in tipo_sumario:
            palavra_procurada3 = "ESTÁDIO"
            palavra_procurada2 = "TOTAL"
            
            for linha_numero, linha_base in enumerate(dados, start=1):
                linha_base = str(linha_base)  # Converta para string, se ainda não for
    
                if palavra_procurada2 in linha_base:
                    print(f"A palavra '{palavra_procurada2}' foi encontrada na linha {linha_numero}:")
                    ref6 = linha_numero
                    ref8 = linha_numero + 1
                    ref10 = linha_numero + 2
                    print(linha_base)
                    ref7 = dados[ref6]
                    ref9 = dados[ref8]
                    ref11 = dados[ref10]
                    # print(ref7)
                    print(f"DISPONIVEIS: '{ref7}', VENDIDOS: '{ref9}', DEVOLVIDOS: '0', ARRECADAÇÃO: '{ref11}'")
                    break
                
                if palavra_procurada3 in linha_base:
                    ref12 = linha_numero
                    ref13 = dados[ref12]
                    print(f"ESTADIO: '{ref13}'")
                    
                    ref14 = linha_numero + 8
                    ref15 = dados[ref14]
                    print(f"DATA: '{ref15}'")
    
                    ref16 = linha_numero + 4
                    ref17 = dados[ref16]
                    print(f"MANDANTE: '{ref17}'")
    
                    ref18 = linha_numero + 5
                    ref19 = dados[ref18]
                    print(f"VISITANTES: '{ref19}'")
                    
            resultados.append({'Jogo': arquivo_pdf, 'Tipo de Sumário': tipo_sumario, 'Data': ref15,
                               'Mandante': ref17, 'Visitante': ref19, 'ARRECADAÇÃO': ref11, 'UTILIZADOS': ref9, 'DEVOLVIDOS': "0",
                               'DISPONIVEL': ref7, 'ESTADIO': ref13})

            tipo_sumario = "Tipo 2 - (FEDERACAO MINEIRA DE FUTEBOL)"

# Exportar lista de resultados para um arquivo Excel
nome_arquivo_excel = 'sandbox14.xlsx'

df_resultados = pd.DataFrame(resultados)
df_resultados.to_excel(nome_arquivo_excel, index=False)

print(f'Resultados exportados como "{nome_arquivo_excel}"')
