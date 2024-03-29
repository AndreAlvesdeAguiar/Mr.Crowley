import os
import requests

PDF_FOLDER_PATH = "/home/andre/Downloads/raspagem"

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
