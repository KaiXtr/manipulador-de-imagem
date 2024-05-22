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

# Esta função inverte as cores da imagem
def inverter(v,b):
    for vv in range(len(v)):
        v[vv] = 255 - v[vv]

    return v

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

# Esta função separa os canais RGB
def to_channel(v,b):
    n = [0,0,0]

    if b[0]: n[0] = v[0]
    if b[1]: n[1] = v[1]
    if b[2]: n[2] = v[2]

    return n

# Esta função adiciona borrão
def blur(v,x,y,b):
    nPixels = 0

    n = [0,0,0]
    for yy in range(-b, b + 1):
        if (y + yy < 0): continue
        if (y + yy > len(v) - 1): continue

        for xx in range(-b, b + 1):
            if (x + xx < 0): continue
            if (x + xx > len(v[y + yy]) - 1): continue

            n[0] += v[y + yy][x + xx][0]
            n[1] += v[y + yy][x + xx][1]
            n[2] += v[y + yy][x + xx][2]
            nPixels += 1
    
    return [int(n[0]/nPixels),int(n[1]/nPixels),int(n[2]/nPixels)]

# Esta função aplica o filtro de detecção de borda
def sobel(v,x,y,b):
    n = list(v[y][x])
    for yy in range(-1, 2):
        if (y + yy < 0): continue
        if (y + yy > len(v) - 1): continue

        for xx in range(-1, 2):
            if (x + xx < 0): continue
            if (x + xx > len(v[y + yy]) - 1): continue

            if yy == -1:
                if xx == -1:
                    n[0] += (v[y + yy][x + xx][0] * -1) + (v[y + yy][x + xx][0] * 1)
                    n[1] += (v[y + yy][x + xx][1] * -1) + (v[y + yy][x + xx][0] * 1)
                    n[2] += (v[y + yy][x + xx][2] * -1) + (v[y + yy][x + xx][0] * 1)
                if xx == 0:
                    n[0] += (v[y + yy][x + xx][0] * 2)
                    n[1] += (v[y + yy][x + xx][0] * 2)
                    n[2] += (v[y + yy][x + xx][0] * 2)
                if xx == 1:
                    n[0] += (v[y + yy][x + xx][0] * 1) + (v[y + yy][x + xx][0] * 1)
                    n[1] += (v[y + yy][x + xx][1] * 1) + (v[y + yy][x + xx][0] * 1)
                    n[2] += (v[y + yy][x + xx][2] * 1) + (v[y + yy][x + xx][0] * 1)
            if yy == 0:
                if xx == -1:
                    n[0] += (v[y + yy][x + xx][0] * -2)
                    n[1] += (v[y + yy][x + xx][1] * -2)
                    n[2] += (v[y + yy][x + xx][2] * -2)
                if xx == 1:
                    n[0] += (v[y + yy][x + xx][0] * 2)
                    n[1] += (v[y + yy][x + xx][1] * 2)
                    n[2] += (v[y + yy][x + xx][2] * 2)
            if yy == 1:
                if xx == -1:
                    n[0] += (v[y + yy][x + xx][0] * -1) + (v[y + yy][x + xx][0] * -1)
                    n[1] += (v[y + yy][x + xx][1] * -1) + (v[y + yy][x + xx][0] * -1)
                    n[2] += (v[y + yy][x + xx][2] * -1) + (v[y + yy][x + xx][0] * -1)
                if xx == 0:
                    n[0] += (v[y + yy][x + xx][0] * -2)
                    n[1] += (v[y + yy][x + xx][0] * -2)
                    n[2] += (v[y + yy][x + xx][0] * -2)
                if xx == 1:
                    n[0] += (v[y + yy][x + xx][0] * 1) + (v[y + yy][x + xx][0] * -1)
                    n[1] += (v[y + yy][x + xx][1] * 1) + (v[y + yy][x + xx][0] * -1)
                    n[2] += (v[y + yy][x + xx][2] * 1) + (v[y + yy][x + xx][0] * -1)
    
    return n

def alterarImg(pArray,func,valor,svImg=None):
    novaArray = np.array(pArray).view()
    maxLd = len(pArray) * len(pArray[0])

    # fazendo alteração nos pixels da imagem
    if (func != None):
        for y in range(len(pArray)):
            for x in range(len(pArray[y])):
                if func.__name__ in ('blur','sobel'):
                    vv = func(list(pArray),x,y,valor)
                else:
                    vv = func(list(pArray[y][x]),valor)
                
                prg = 100 * ((x + (y * len(pArray)))/maxLd)
                print(f"Aplicando alterações... ({int(prg) + 1}/100)")
                novaArray[y][x] = tuple(vv)
    
    if (svImg != None):
        salvarImg(svImg,novaArray)
    
    return novaArray

def salvarImg(imgPath,pArray):
    print(f"Salvando {imgPath}...")
    outImg = Image.fromarray(np.array(pArray, dtype=np.uint8))
    outImg.save(imgPath)

def salvarPlanilha(arqPath,dataFrame):
    print(f"Gerando {arqPath}...")
    dataFrame.to_excel(arqPath,index=False)

def carregarImg(imgNome,prompt=False):
    # encontra um arquivo de imagem
    folderNome = imgNome.replace('.','_')
    img = Image.open(imgNome).convert('RGB')

    # gerando dataframe da imagem a partir de suas dimensões
    w, h = img.size
    pixels = np.array(img.getdata())
    xlist = [i for i in range(h)]
    df = pd.DataFrame({j: xlist for j in range(w)},index=xlist,dtype=str)

    # obter pixel a ser alterado
    print(f'A imagem localizada em: "{imgNome}" possui dimensões {w}x{h}.')
    inputX = informarValor("a posição X do pixel",w - 1) if prompt else 0
    inputY = informarValor("a posição Y do pixel",h - 1) if prompt else 0

    pixelNovo = [255,0,0]
    inputAsk = input(f'Gostaria de informar a cor a ser substituída? (y/N): ') if prompt else 'N'
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
        #df.loc[y] = [str(r) for r in row]
        novaArray.append([tuple(r) for r in row])

    # salvando o dataframe em uma planilha
    #salvarPlanilha(f"{imgNome}_rgb.xlsx",df)

    # obtendo informações CMYK dos pixels e os inserindo ao dataframe
    '''p = 0
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
    salvarPlanilha(f"{imgNome}_cymk.xlsx",df)'''
    
    return novaArray

def main():
    imgNome = "imagem.png"
    imgNome = "balao.jpg"

    # criando pasta
    folderNome = f"./out/{imgNome.replace('.','_')}"
    os.makedirs(folderNome,exist_ok=True)

    # carregando imagem e pixels
    novaArray = carregarImg(imgNome)

    # salvando array de pixels como imagem
    alterarImg(novaArray,None,None,f"{folderNome}/{imgNome}")

    # gerando 5 tipos de imagens em escala de cinza
    for t in range(5):
        alterarImg(novaArray,to_grayscale,t,f"{folderNome}/grayscale_{t + 1}_{imgNome}")

    # gerando 3 tipos de imagens de brilhos e 3 tipos de imagens de contraste
    for t in range(3):
        if t == 0:
            alterarImg(novaArray,inverter,1,f"{folderNome}/inverter_{imgNome}")
            alterarImg(novaArray,brilho_soma,-128,f"{folderNome}/brilho_soma_{t + 1}_{imgNome}")
            alterarImg(novaArray,brilho_fator,-2,f"{folderNome}/brilho_fator_{t + 1}_{imgNome}")
            alterarImg(novaArray,contraste,-100,f"{folderNome}/contraste_{t + 1}_{imgNome}")
            alterarImg(novaArray,blur,1,f"{folderNome}/borrar_{t + 1}_{imgNome}")
            alterarImg(novaArray,sobel,1,f"{folderNome}/sobel_{imgNome}")
            alterarImg(novaArray,to_channel,[1,1,0],f"{folderNome}/rgb_{t + 1}_{imgNome}")
        if t == 1:
            alterarImg(novaArray,brilho_soma,128,f"{folderNome}/brilho_soma_{t + 1}_{imgNome}")
            alterarImg(novaArray,brilho_fator,2,f"{folderNome}/brilho_fator_{t + 1}_{imgNome}")
            alterarImg(novaArray,contraste,100,f"{folderNome}/contraste_{t + 1}_{imgNome}")
            alterarImg(novaArray,blur,3,f"{folderNome}/borrar_{t + 1}_{imgNome}")
            alterarImg(novaArray,to_channel,[0,1,0],f"{folderNome}/rgb_{t + 1}_{imgNome}")
        if t == 2:
            alterarImg(novaArray,brilho_soma,200,f"{folderNome}/brilho_soma_{t + 1}_{imgNome}")
            alterarImg(novaArray,brilho_fator,3,f"{folderNome}/brilho_fator_{t + 1}_{imgNome}")
            alterarImg(novaArray,contraste,200,f"{folderNome}/contraste_{t + 1}_{imgNome}")
            alterarImg(novaArray,blur,5,f"{folderNome}/borrar_{t + 1}_{imgNome}")
            alterarImg(novaArray,to_channel,[0,1,1],f"{folderNome}/rgb_{t + 1}_{imgNome}")

if __name__ == "__main__":
    main()