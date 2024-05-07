from PIL import Image # a biblioteca pillow serve para manipular imagens
import numpy as np # a biblioteca numpy traz manipulação de dados
import pandas as pd # a bibilioteca pandas manipula tabelas e planilhas
import os # biblioteca para obter informações do sistema

# Esta função obtém os valores de posição de pixel do usuário e realiza a filtragem dessa entrada
def informarValor(s,l):
    v = None
    while v == None:
        try:
            v = input(f"Informe {s} (0/{l}): ")
            if v == "":
                print(f"AVISO: informado valor nulo. Definindo {s} como 0.")
                v = 0
            else:
                v = int(v)
        except:
            print(".: Valor inválido, tente novamente :.")
            v = None
    
    if v > l:
        print(f"AVISO: o valor máximo é {l}. Definindo {s} como {l}.")
        v = l
    
    return v

# Esta função converte valores RGB para valores CMYK
def to_cmyk(v):
    r,g,b = v[0],v[1],v[2]

    if (r,g,b) == (0,0,0):
        return 0,0,0,100

    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255

    min_cmy = min(c, m, y)
    c = round(((c - min_cmy) / (1 - min_cmy)) * 100,1)
    m = round(((m - min_cmy) / (1 - min_cmy)) * 100,1)
    y = round(((y - min_cmy) / (1 - min_cmy)) * 100,1)
    k = round((min_cmy) * 100,1)

    return [c,m,y,k]

# Esta função converte valores RGB em escala de cinza
def to_grayscale(v):
    r,g,b = v[0],v[1],v[2]

    l = (r * 0.2989) + (g * 0.5870) + (b * 0.1140)

    return [l,l,l]

def main():
    # encontra um arquivo de imagem
    imgNome = "balao.jpg"
    caminho = os.path.dirname(os.path.abspath(__file__))
    img = Image.open(caminho + '/' + imgNome).convert('RGB')

    # gerando dataframe da imagem a partir de suas dimensões
    w, h = img.size
    pixels = np.array(img.getdata())
    xlist = [i for i in range(h)]
    df = pd.DataFrame({j: xlist for j in range(w)},index=xlist,dtype=str)

    # obter pixel a ser alterado
    print(f'A imagem localizada em: "{caminho}/{imgNome}" possui dimensões {w}x{h}.')
    inputX = informarValor("a posição X do pixel",w - 1)
    inputY = informarValor("a posição Y do pixel",h - 1)

    pixelNovo = [255,0,0]
    inputAsk = input(f'Gostaria de informar a cor a ser substituída? (y/N): ')
    if inputAsk.lower() == "y":
        inputR = informarValor("o valor R da cor",255)
        inputG = informarValor("o valor G da cor",255)
        inputB = informarValor("o valor B da cor",255)
        pixelNovo = [inputR,inputG,inputB]

    pixelPadrao = None
    novaArray = []

    # procurando pixel informado pelo usuário
    p = 0
    for y in range(h):
        row = []
        for x in range(w):
            rgbPixel = [px for px in pixels[p]]

            # se o pixel for o informado pelo usuário, obter pixel padrão
            if x == inputX and y == inputY:
                print(f'* Pixel {inputX}x{inputY} encontrado {tuple(rgbPixel)}!')
                print(f'Todos os pixels semelhantes terão seu valor alterado para {pixelNovo}')
                pixelPadrao = rgbPixel
            else:
                print(f'Pixel {x}x{y} de {w}x{h}')
            p += 1

    # obtendo informações RGB dos pixels e os inserindo ao dataframe
    p = 0
    for y in range(h):
        row = []
        for x in range(w):
            rgbPixel = [px for px in pixels[p]]

            # se pixel identificado é igual ao pixelPadrão, alterar
            if rgbPixel == pixelPadrao:
                row.append(pixelNovo)
            else:
                row.append(rgbPixel)
            p += 1
        df.loc[y] = [str(r) for r in row]
        novaArray.append([tuple(r) for r in row])

    # salvando o dataframe em uma planilha
    planilhaNome = f"{imgNome.replace('.','_')}_rgb.xlsx"
    print(f"Gerando {planilhaNome}...")
    df.to_excel(f'out/{planilhaNome}',index=False)

    # obtendo informações CMYK dos pixels e os inserindo ao dataframe
    p = 0
    for y in range(h):
        row = []
        for x in range(w):
            rgbPixel = [px for px in pixels[p]]
            row.append(rgbPixel)
            p += 1
        df.loc[y] = [str(to_cmyk(r)) for r in row]

    # salvando o dataframe em uma planilha
    planilhaNome = f"{imgNome.replace('.','_')}_cymk.xlsx"
    print(f"Gerando {planilhaNome}...")
    df.to_excel(f'out/{planilhaNome}',index=False)

    # salvando array de pixels como imagem
    print(f"Salvando {imgNome}...")
    outImg = Image.fromarray(np.array(novaArray, dtype=np.uint8))
    outImg.save(f'out/{imgNome}')

    # gerando imagem em escala de cinza
    for y in range(len(novaArray)):
        for x in range(len(novaArray[y])):
            novaArray[y][x] = tuple(to_grayscale(novaArray[y][x]))

    # salvando array de pixels como imagem cinza
    grayscaleNome = f"greyscale_{imgNome}"
    print(f"Salvando {grayscaleNome}...")
    outImg = Image.fromarray(np.array(novaArray, dtype=np.uint8))
    outImg.save(f'out/{grayscaleNome}')

if __name__ == "__main__":
    main()