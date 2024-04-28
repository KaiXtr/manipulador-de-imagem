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

# A função abaixo serve para pintar as células da tabela (não está funcionando por hora)
def estilo(d):
    v = []
    txt = ""
    for x in d[1:-2]:
        if x == ' ':
            v.append(txt)
            txt = ""
        else:
            txt += x

    condicao = d
    st = f'background-color: red'
    return [st if d else st for d in condicao]

def main():

    # encontra um arquivo de imagem
    imgNome = "imagem.png"
    caminho = os.path.dirname(os.path.abspath(__file__))
    img = Image.open(caminho + '/' + imgNome).convert('RGB')

    # gerando dataframe da imagem a partir de suas dimensões
    w, h = img.size
    pixels = np.array(img.getdata())
    xlist = [i for i in range(w)]
    df = pd.DataFrame({j: xlist for j in range(h)},index=xlist,dtype=str)

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
    for x in range(w):
        row = []
        for y in range(h):
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
    for x in range(w):
        row = []
        for y in range(h):
            rgbPixel = [px for px in pixels[p]]

            # se pixel identificado é igual ao pixelPadrão, alterar
            if rgbPixel == pixelPadrao:
                row.append(pixelNovo)
            else:
                row.append(rgbPixel)
            p += 1
        df.loc[x] = [str(r) for r in row]
        novaArray.append([tuple(r) for r in row])

    # aplicando estilo (que não funciona por hora) e salvando o dataframe em uma planilha
    df.style.apply(estilo, subset=xlist)
    df.to_excel('out/planilha1.xlsx',index=False)

    # salvando array de pixels como imagem
    outImg = Image.fromarray(np.array(novaArray, dtype=np.uint8))
    outImg.save(f'out/{imgNome}')

if __name__ == "__main__":
    main()