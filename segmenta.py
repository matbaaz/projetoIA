
import cv2
import numpy as np

def segmentar_feijoes(imagem_bgr):
    """
    Recebe uma imagem BGR (NumPy array) e retorna uma lista de máscaras binárias,
    uma para cada feijão detectado, além das bounding boxes correspondentes.
    """

    # 1. Converter para escala de cinza
    gray = cv2.cvtColor(imagem_bgr, cv2.COLOR_BGR2GRAY)

    # 2. (Opcional) Reduzir ruído
    blur = cv2.GaussianBlur(gray, ksize=(5,5), sigmaX=0)

    # 3. Limiarização binária invertida (branco→0, feijão (escuro)→255)
    #    Usamos Otsu para escolher limiar automaticamente
    _, bin_inv = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # Agora bin_inv == 255 onde estava feijão, e 0 onde era fundo branco

    # 4. Morfologia: erode → dilate para remover ruídos pequenos
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    opening = cv2.morphologyEx(bin_inv, cv2.MORPH_OPEN, kernel, iterations=1)

    # 5. Encontrar contornos
    contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mascaras = []
    bboxes = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 200:  # filtrar regiões muito pequenas (ajustar conforme escala da imagem)
            continue

        # 6. Criar máscara do contorno
        mask = np.zeros_like(gray)
        cv2.drawContours(mask, [cnt], -1, color=255, thickness=-1)  # preenchido

        # 7. Bounding box
        x, y, w, h = cv2.boundingRect(cnt)
        mascaras.append(mask)
        bboxes.append((x, y, w, h))

    return mascaras, bboxes
