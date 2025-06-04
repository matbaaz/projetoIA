import csv
import os

def extrair_features(imagem_bgr, mask, cnt):
    """
    Retorna um vetor de features (lista ou NumPy array) para o feijão definido por mask e contour.
    """
    # Converter para cinza se ainda não for
    gray = cv2.cvtColor(imagem_bgr, cv2.COLOR_BGR2GRAY)

    # 1. Cor (média e std em BGR)
    # cv2.mean retorna (b_mean, g_mean, r_mean, alpha)
    b_mean, g_mean, r_mean, _ = cv2.mean(imagem_bgr, mask=mask)
    # Para std, pegamos pixels de cada canal diretamente
    pixels_BGR = imagem_bgr[mask == 255]
    std_b, std_g, std_r = np.std(pixels_BGR, axis=0)

    # 2. Área e perímetro
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt, True)

    # 3. Circularidade
    if perimeter == 0:
        circularity = 0
    else:
        circularity = 4 * np.pi * area / (perimeter ** 2)

    # 4. Aspect ratio e bounding box
    x, y, w, h = cv2.boundingRect(cnt)
    aspect_ratio = float(w) / float(h) if h != 0 else 0

    # 5. Solidity
    hull = cv2.convexHull(cnt)
    area_hull = cv2.contourArea(hull)
    solidity = float(area) / area_hull if area_hull != 0 else 0

    # 6. Extent
    extent = float(area) / (w * h) if (w*h) != 0 else 0

    # 7. Desvio std de cinza
    pixels_gray = gray[mask == 255]
    std_gray = float(np.std(pixels_gray)) if pixels_gray.size > 0 else 0

    # 8. Entropia (usando histograma de 16 bins)
    hist, _ = np.histogram(pixels_gray, bins=16, range=(0,256), density=True)
    # Para evitar log2(0), somamos valor pequeno:
    eps = 1e-7
    entropy = -np.sum(hist * np.log2(hist + eps))

    # 9. Hu Moments (7 valores)
    moments = cv2.moments(cnt)
    hu = cv2.HuMoments(moments).flatten()
    hu = [-np.sign(h[0]) * np.log10(abs(h[0])+1e-12) if h[0] != 0 else 0 for h in hu]
    # (normalização do log para não ficarem valores muito pequenos)

    # Montar vetor final:
    features = [
        b_mean, g_mean, r_mean,
        std_b, std_g, std_r,
        area, perimeter, circularity, aspect_ratio,
        solidity, extent, std_gray, entropy
    ] + hu  # lista de 7 elementos

    return features

def montar_dataset(pasta_imagens, arquivo_csv_saida):
    """
    pasta_imagens: contém subpastas 'ruins/' e 'bons/', cada uma com imagens.
    arquivo_csv_saida: caminho do CSV final.
    """
    classes = {'ruins': 0, 'bons': 1}

    header = [
        'mean_b','mean_g','mean_r',
        'std_b','std_g','std_r',
        'area','perimeter','circularity','aspect_ratio',
        'solidity','extent','std_gray','entropy',
    ] + [f'hu{i+1}' for i in range(7)] + ['label']

    with open(arquivo_csv_saida, mode='w', newline='') as f_out:
        writer = csv.writer(f_out, delimiter=';')
        writer.writerow(header)

        for classe_str, rotulo in classes.items():
            pasta_classe = os.path.join(pasta_imagens, classe_str)
            for nome_img in os.listdir(pasta_classe):
                if not nome_img.lower().endswith(('.png','.jpg','.jpeg','.bmp')):
                    continue
                caminho = os.path.join(pasta_classe, nome_img)
                img = cv2.imread(caminho)
                if img is None:
                    continue

                máscaras, bboxes = segmentar_feijoes(img)
                # Para cada máscara (cada feijão)
                contours, _ = cv2.findContours(
                    cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) & máscaras[0], 
                    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                )
                # Mas, como segmentamos antes, basta iterar “cnts” retornados em segmentar_feijoes:
                # Na verdade, sugerimos modificar segmentar_feijoes para também retornar “contours” junto.
                # Suponhamos que “segmentar_feijoes” retorne (mascaras, bboxes, contours).

                # *** Exemplo: adaptar segmentar_feijoes para também retornar contours. ***
                # Aqui, vamos considerar que segmentar_feijoes retornou contornos na mesma ordem:
                máscaras, bboxes, contours = segmentar_feijoes_com_contours(img)

                for mask, cnt in zip(máscaras, contours):
                    feats = extrair_features(img, mask, cnt)
                    writer.writerow(feats + [rotulo])

    print(f"Dataset gerado em: {arquivo_csv_saida}")
