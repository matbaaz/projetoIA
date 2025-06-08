
import os
import cv2
import csv
import numpy as np

#Recorta a imagem  excluindo a parte marrom e mantendo apenas a parte branca da folha
def recortar_folha(imagem_bgr):
    hsv = cv2.cvtColor(imagem_bgr, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 60, 255])
    mask = cv2.inRange(hsv, lower_white, upper_white)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return imagem_bgr
    maior_contorno = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(maior_contorno)
    recorte = imagem_bgr[y:y+h, x:x+w]
    return recorte

def segmentar_feijoes_com_contours(imagem_bgr):
    gray = cv2.cvtColor(imagem_bgr, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, bin_inv = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    opening = cv2.morphologyEx(bin_inv, cv2.MORPH_OPEN, kernel, iterations=1)
    contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mascaras = []
    bboxes = []
    valid_contours = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 200:
            continue
        mask = np.zeros_like(gray)
        cv2.drawContours(mask, [cnt], -1, color=255, thickness=-1)
        x, y, w, h = cv2.boundingRect(cnt)
        mascaras.append(mask)
        bboxes.append((x, y, w, h))
        valid_contours.append(cnt)
    return mascaras, bboxes, valid_contours

def extrair_features(imagem_bgr, mask, cnt):
    gray = cv2.cvtColor(imagem_bgr, cv2.COLOR_BGR2GRAY)
    b_mean, g_mean, r_mean, _ = cv2.mean(imagem_bgr, mask=mask)
    pixels_BGR = imagem_bgr[mask == 255]
    std_b, std_g, std_r = np.std(pixels_BGR, axis=0) if pixels_BGR.size > 0 else (0,0,0)
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt, True)
    circularity = 4 * np.pi * area / (perimeter ** 2) if perimeter != 0 else 0
    x, y, w, h = cv2.boundingRect(cnt)
    aspect_ratio = float(w)/h if h != 0 else 0
    hull = cv2.convexHull(cnt)
    area_hull = cv2.contourArea(hull)
    solidity = float(area)/area_hull if area_hull != 0 else 0
    extent = float(area)/(w*h) if (w*h) != 0 else 0
    pixels_gray = gray[mask == 255]
    std_gray = float(np.std(pixels_gray)) if pixels_gray.size > 0 else 0
    hist, _ = np.histogram(pixels_gray, bins=16, range=(0,256), density=True)
    eps = 1e-7
    entropy = -np.sum(hist * np.log2(hist + eps))
    moments = cv2.moments(cnt)
    hu = cv2.HuMoments(moments).flatten()
    hu_log = [-np.sign(h) * np.log10(abs(h) + 1e-12) if h != 0 else 0 for h in hu]
    features = [
        b_mean, g_mean, r_mean,
        std_b, std_g, std_r,
        area, perimeter, circularity, aspect_ratio,
        solidity, extent, std_gray, entropy
    ] + hu_log
    return features

def processar_feijao(img_crop, mask, cnt, writer, rotulo, nome_base, pasta_segregado, indice):
    """
    Processa um feijão individual, extraindo suas características, salvando no CSV e gerando uma imagem isolada.

    Args:
        img_crop: Imagem recortada contendo o feijão
        mask: Máscara binária do feijão
        cnt: Contorno do feijão
        writer: Objeto CSV writer para salvar as características
        rotulo: Rótulo da classe (0 para ruins, 1 para bons)
        nome_base: Nome base para o arquivo de saída
        pasta_segregado: Diretório para salvar as imagens segmentadas
        indice: Índice do feijão na imagem atual

    Returns:
        None
    """
    # Extrai características e salva no CSV
    feats = extrair_features(img_crop, mask, cnt)
    writer.writerow(feats + [rotulo])

    # Recorta o feijão e sua máscara
    x, y, w, h = cv2.boundingRect(cnt)
    feijao_crop = img_crop[y:y+h, x:x+w]
    mask_crop = mask[y:y+h, x:x+w]

    # Cria fundo branco e aplica a máscara
    fundo_branco = np.ones_like(feijao_crop, dtype=np.uint8) * 255
    feijao_masked = np.where(mask_crop[..., None] == 255, feijao_crop, fundo_branco)

    # Salva a imagem do feijão isolado
    nome_feijao = f"{nome_base}_feijao_{indice+1:03d}.jpg"
    caminho_feijao = os.path.join(pasta_segregado, nome_feijao)
    cv2.imwrite(caminho_feijao, feijao_masked)

def montar_dataset(pasta_imagens, arquivo_csv_saida):
    classes = {'ruins_recorte': 0, 'bons_recorte': 1}
    header = [
        'mean_b','mean_g','mean_r',
        'std_b','std_g','std_r',
        'area','perimeter','circularity','aspect_ratio',
        'solidity','extent','std_gray','entropy',
    ] + [f'hu{i+1}' for i in range(7)] + ['label']

    with open(arquivo_csv_saida, mode='w', newline='') as f_out:
        writer = csv.writer(f_out, delimiter=';')
        writer.writerow(header)
        #Itera sobre as classes ruins e bons
        for classe_str, rotulo in classes.items():
            pasta_classe = os.path.join(pasta_imagens, classe_str)
            #pasta_recorte = os.path.join(pasta_imagens, f"{classe_str}_recorte")
            pasta_segregado = os.path.join(pasta_imagens, f"{classe_str}_segregado")
            os.makedirs(pasta_classe, exist_ok=True)
            os.makedirs(pasta_segregado, exist_ok=True)

            for nome_img in os.listdir(pasta_classe):
                if not nome_img.lower().endswith(('.png','.jpg','.jpeg','.bmp')):
                    continue
                caminho = os.path.join(pasta_classe, nome_img)
                img = cv2.imread(caminho)
                if img is None:
                    continue

                nome_base = os.path.splitext(nome_img)[0]
                #img_crop = recortar_folha(img)
                #caminho_recorte = os.path.join(pasta_classe, nome_img)
                #cv2.imwrite(caminho_recorte, img_crop)

                mascaras, bboxes, contours = segmentar_feijoes_com_contours(img)

                for i, (mask, cnt) in enumerate(zip(mascaras, contours)):
                    processar_feijao(img, mask, cnt, writer, rotulo, nome_base, pasta_segregado, i)

    print(f"Dataset gerado em: {arquivo_csv_saida}")

if __name__ == "__main__":
    pasta = os.getcwd()
    montar_dataset(pasta, "feijoes_dataset.csv")
