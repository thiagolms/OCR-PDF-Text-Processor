import cv2
import pytesseract
from pdf2image import convert_from_path
import re
import os

caminho = os.getcwd()
arquivos = [arquivo for arquivo in os.listdir(caminho) if arquivo.lower().endswith('.pdf')]

for arquivo in arquivos:
    nome_arquivo = os.path.join(caminho, arquivo)
    paginas = convert_from_path(nome_arquivo)
    resultado = ""
    for pagina in paginas:
        pagina.save("img.png", "PNG")    
        img = cv2.imread("img.png")
        texto = pytesseract.image_to_string(img)
        resultado += texto
        
    def remove_quebra_linha(resultado):
        resultado = re.sub(r'(?<!\n)\n(?!\n)', ' ', resultado)
        return resultado

    resultado_formatado = remove_quebra_linha(resultado)
    nome_arquivo_txt = os.path.splitext(arquivo)[0] + ".txt"
    caminho_arquivo_txt = os.path.join(caminho, nome_arquivo_txt)
    
    with open(nome_arquivo_txt, "w") as arquivo:
        print(resultado_formatado, file = arquivo)
