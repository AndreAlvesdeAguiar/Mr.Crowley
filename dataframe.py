import easyocr
from pdf2image import convert_from_path
import pandas as pd

# Caminho para o arquivo PDF
caminho_pdf = '/home/andre/Downloads/raspagem/2023/jogo_3.pdf'

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
        # print(text)
        dados.append(text)

df = pd.DataFrame(dados)

print(df)
