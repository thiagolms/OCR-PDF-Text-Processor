import cv2
import pytesseract
import re
import os
from pdf2image import convert_from_path

def remove_quebra_linha(resultado):
    resultado = re.sub(r"(?<!\n)\n(?!\n)", " ", resultado)
    return resultado

def pos_processamento_texto(texto):
    # FORMATANDO CABEÇALHO DO TEXTO
    # Encontrar a primeira ocorrência
    primeira_ocorrencia = texto.find("ocorrencia")
    # Verificar se encontrou a primeira ocorrência
    if primeira_ocorrencia != -1:
        # Apagar o texto acima da ocorrência
        texto = texto[primeira_ocorrencia:]
    # FORMATANDO RODAPÉ DO TEXTO
    # Encontrar a última ocorrência
    ultima_ocorrencia = max(texto.rfind("ocorrencia2"), texto.rfind("ocorrencia3"))
    # Verificar se encontrou a última ocorrência
    if ultima_ocorrencia != -1:
        # Encontrar a posição do final da ocorrência
        posicao_final_ocorrencia = texto.find("\n", ultima_ocorrencia)
        # Apagar o texto abaixo da ocorrência
        texto = texto[:posicao_final_ocorrencia + 1]
        # Adicionar as informações formatadas no final do texto
        texto += "\nrodapé\n"
        texto += "rodapé\n\n"
        texto += "rodapé\n"
        texto += "rodapé"

    return texto

caminho = os.getcwd()
arquivos = [arquivo for arquivo in os.listdir(caminho) if arquivo.endswith('.pdf')]

for arquivo in arquivos:
    nome_arquivo = os.path.join(caminho, arquivo)
    paginas = convert_from_path(nome_arquivo)
    resultado = ""
    for pagina in paginas:
        pagina.save("img.png", "PNG")    
        img = cv2.imread("img.png")
        texto = pytesseract.image_to_string(img, lang="por")
        resultado += texto
        
    resultado_quebra_linha = remove_quebra_linha(resultado)
    resultado_processamento_texto = pos_processamento_texto(resultado_quebra_linha)
    nome_arquivo_txt = os.path.splitext(arquivo)[0] + ".txt"
    caminho_arquivo_txt = os.path.join(caminho, nome_arquivo_txt)
    
    with open(nome_arquivo_txt, "w") as arquivo:
        print(resultado_processamento_texto, file=arquivo)
