import cv2
import pytesseract
import re
import os
from pdf2image import convert_from_path

def remove_quebra_linha(resultado):
    # REMOVE QUEBRA LINHAS E SUBSTITUI POR ESPAÇOS EM BRANCO, DESDE QUE NÃO SEJAM SEGUIDAS DE OUTRAS QUEBRAS DE LINHA
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

def remover_marca_dagua(imagem):
    # Converter para escala de cinza
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    # Definir uma intensidade mínima para considerar como preto
    intensidade_preto = 150
    # Limiarização simples para transformar pixels abaixo da intensidade mínima em preto "_" significa uma variavel nula
    _, imagem_limiarizada = cv2.threshold(imagem_cinza, intensidade_preto, 255, cv2.THRESH_BINARY)
    # Inverter os valores de preto e branco
    imagem_invertida = cv2.bitwise_not(imagem_limiarizada)
    # Ajustar a intensidade do branco
    intensidade_branco = 255
    imagem_ajustada = cv2.multiply(imagem_invertida, intensidade_branco / 255)
    # Converter de volta para BGR (se necessário)
    imagem_processada = cv2.cvtColor(imagem_ajustada, cv2.COLOR_GRAY2BGR)
    return imagem_processada

# Obtem o diretório atual
caminho = os.getcwd()
# Cria uma lista chamada arquivos que contem os nomes dos arquivos presentes no diretorio que possuem a extensão ".pdf"
arquivos = [arquivo for arquivo in os.listdir(caminho) if arquivo.endswith('.pdf')]

for arquivo in arquivos:
    # Cria o caminho completo do arquivo e concatena o diretorio atua com o nome do arquivo
    nome_arquivo = os.path.join(caminho, arquivo)
    # CONVERTE O ARQUIVO PDF EM IMAGENS DAS PAGINAS
    paginas = convert_from_path(nome_arquivo)
    resultado = ""
    for pagina in paginas:
        # SALVA A IMAGEM DA PAGINA ATUAL
        pagina.save("img.png", "PNG")   
         #LÊ A IMAGEM E SALVA
        img = cv2.imread("img.png")
        # RECEBE A IMAGEM COMO ENTRADA E RETORNA O TEXTO EXTRAIDO EM PORTUGUES
        texto = pytesseract.image_to_string(img, lang="por")
        resultado += texto
        
    # POS-PROCESSAMENTO DO TEXTO E AJUSTES FINAIS
    resultado_quebra_linha = remove_quebra_linha(resultado)
    resultado_processamento_texto = pos_processamento_texto(resultado_quebra_linha)
    #
    nome_arquivo_txt = os.path.splitext(arquivo)[0] + ".txt"
    caminho_arquivo_txt = os.path.join(caminho, nome_arquivo_txt)
    
    with open(nome_arquivo_txt, "w") as arquivo:
        print(resultado_processamento_texto, file=arquivo)
