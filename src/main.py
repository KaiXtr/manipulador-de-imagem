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
def to_grayscale(v,tp):
    r,g,b = v[0],v[1],v[2]

    l = 0

    if tp == 0:
        l = (r * 0.2989) + (g * 0.5870) + (b * 0.1140)
    elif tp == 1:
        l = (r + g + b)/3
    elif tp == 2:
        l = (min(r,g,b) + max(r,g,b))/2
    elif tp == 3:
        l = min(r,g,b)
    elif tp == 4:
        l = max(r,g,b)

    return [l,l,l]

# Esta função altera o brilho da imagem ao somar valores absolutos
def brilho_soma(v,b):
    for vv in range(len(v)):
        v[vv] += b

        if (v[vv] > 255): v[vv] = 255
        if (v[vv] < 0): v[vv] = 0

    return v

# Esta função altera o brilho da imagem ao multiplicar valores proporcionais
def brilho_fator(v,b):
    for vv in range(len(v)):
        if b >= 0: v[vv] *= b
        else: v[vv] = int(v[vv]/(-1 * b))

        if (v[vv] > 255): v[vv] = 255
        if (v[vv] < 0): v[vv] = 0

    return v

# Esta função altera o contraste da imagem
def contraste(v,b):
    f = (259.0 * (b + 255.0)) / (255.0 * (259.0 - b))

    for vv in range(len(v)):
        v[vv] = round(f * (v[vv] - 128) + 128)

        if (v[vv] > 255): v[vv] = 255
        if (v[vv] < 0): v[vv] = 0

    return v

def main():
    # encontra um arquivo de imagem
    imgNome = "imagem.png"
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

    # criando pasta
    folderNome = imgNome.replace('.','_')
    os.makedirs(f"./out/{folderNome}",exist_ok=True)

    # salvando o dataframe em uma planilha
    planilhaNome = f"{imgNome.replace('.','_')}_rgb.xlsx"
    print(f"Gerando {planilhaNome}...")
    df.to_excel(f'out/{folderNome}/{planilhaNome}',index=False)

    # obtendo informações CMYK dos pixels e os inserindo ao dataframe
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
        df.loc[y] = [str(to_cmyk(r)) for r in row]

    # salvando o dataframe em uma planilha
    planilhaNome = f"{imgNome.replace('.','_')}_cymk.xlsx"
    print(f"Gerando {planilhaNome}...")
    df.to_excel(f'out/{folderNome}/{planilhaNome}',index=False)

    # salvando array de pixels como imagem
    print(f"Salvando {imgNome}...")
    outImg = Image.fromarray(np.array(novaArray, dtype=np.uint8))
    outImg.save(f'out/{folderNome}/{imgNome}')

    # gerando 5 tipos de imagens em escala de cinza
    for t in range(5):
        grayscaleArray = np.array(novaArray).view()

        # gerando imagem em escala de cinza
        for y in range(len(grayscaleArray)):
            for x in range(len(grayscaleArray[y])):
                vv = to_grayscale(grayscaleArray[y][x],t)
                grayscaleArray[y][x] = tuple(vv)

        # salvando array de pixels como imagem cinza
        grayscaleNome = f"greyscale_{t + 1}_{imgNome}"
        print(f"Salvando {grayscaleNome}...")
        outImg = Image.fromarray(np.array(grayscaleArray, dtype=np.uint8))
        outImg.save(f'out/{folderNome}/{grayscaleNome}')

    # gerando 3 tipos de imagens de brilhos
    for t in range(3):
        brilhoArray = np.array(novaArray).view()

        # gerando imagem em escala de cinza
        for y in range(len(brilhoArray)):
            for x in range(len(brilhoArray[y])):
                if t == 0: vv = brilho_soma(brilhoArray[y][x],-128)
                if t == 1: vv = brilho_soma(brilhoArray[y][x],128)
                if t == 2: vv = brilho_soma(brilhoArray[y][x],200)
                brilhoArray[y][x] = tuple(vv)

        # salvando array de pixels como imagem cinza
        brilhoNome = f"brilho_soma_{t + 1}_{imgNome}"
        print(f"Salvando {brilhoNome}...")
        outImg = Image.fromarray(np.array(brilhoArray, dtype=np.uint8))
        outImg.save(f'out/{folderNome}/{brilhoNome}')
    
    # gerando 3 tipos de imagens de brilhos
    for t in range(3):
        brilhoArray = np.array(novaArray).view()

        # gerando imagem em escala de cinza
        for y in range(len(brilhoArray)):
            for x in range(len(brilhoArray[y])):
                if t == 0: vv = brilho_fator(brilhoArray[y][x],-2)
                if t == 1: vv = brilho_fator(brilhoArray[y][x],2)
                if t == 2: vv = brilho_fator(brilhoArray[y][x],3)
                brilhoArray[y][x] = tuple(vv)

        # salvando array de pixels como imagem cinza
        brilhoNome = f"brilho_fator_{t + 1}_{imgNome}"
        print(f"Salvando {brilhoNome}...")
        outImg = Image.fromarray(np.array(brilhoArray, dtype=np.uint8))
        outImg.save(f'out/{folderNome}/{brilhoNome}')
    
    # gerando 3 tipos de imagens de contrates
    for t in range(3):
        contrasteArray = np.array(novaArray).view()

        # gerando imagem em escala de cinza
        for y in range(len(contrasteArray)):
            for x in range(len(contrasteArray[y])):
                if t == 0: vv = contraste(contrasteArray[y][x],-100)
                if t == 1: vv = contraste(contrasteArray[y][x],100)
                if t == 2: vv = contraste(contrasteArray[y][x],200)
                contrasteArray[y][x] = tuple(vv)

        # salvando array de pixels como imagem cinza
        contrasteNome = f"contraste_{t + 1}_{imgNome}"
        print(f"Salvando {contrasteNome}...")
        outImg = Image.fromarray(np.array(contrasteArray, dtype=np.uint8))
        outImg.save(f'out/{folderNome}/{contrasteNome}')

if __name__ == "__main__":
    main()