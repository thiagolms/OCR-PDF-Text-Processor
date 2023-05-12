import cv2
import pytesseract
from pdf2image import convert_from_path
import re
paginas = convert_from_path("portaria.pdf")

resultado = ""
for pagina in paginas:
    pagina.save("img.png", "PNG")    
    img = cv2.imread("img.png")
    texto = pytesseract.image_to_string(img)
    resultado += texto
    
#paragrafos = resultado.split("\n")
#paragrafo_sem_quebra = [paragrafo.strip() for paragrafo in paragrafos]
#resultado = "\n".join(paragrafo_sem_quebra)
#def remove_line_breaks(text):
#    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
#    return text
#resultado_formatado = remove_line_breaks(resultado)
with open("texto.txt", "w") as arquivo:
    print(resultado, file = arquivo)
