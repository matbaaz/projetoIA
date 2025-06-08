# Explicação das Variáveis de Segmentação de Feijões

Este documento explica o significado e o propósito das variáveis `mascaras`, `bboxes` e `contours` retornadas pela função `segmentar_feijoes_com_contours(img_crop)` no sistema de processamento de imagens de feijões.

## Visão Geral do Processo de Segmentação

A função `segmentar_feijoes_com_contours()` é responsável por identificar e isolar cada feijão individual em uma imagem. Ela implementa os seguintes passos:

1. Conversão da imagem para escala de cinza
2. Aplicação de desfoque gaussiano para reduzir ruído
3. Limiarização binária com método de Otsu para separar os feijões do fundo
4. Operações morfológicas para limpar a imagem binária
5. Detecção de contornos para identificar cada feijão
6. Filtragem por área para remover objetos muito pequenos

Após este processamento, a função retorna três variáveis importantes: `mascaras`, `bboxes` e `contours`.

## Explicação das Variáveis

### 1. `mascaras` (Máscaras)

**O que são**: Uma lista de imagens binárias (matrizes NumPy), uma para cada feijão detectado na imagem.

**Características**:
- Cada máscara tem o mesmo tamanho da imagem original
- Pixels com valor 255 (branco) representam o feijão
- Pixels com valor 0 (preto) representam o fundo

**Propósito**:
- Isolar cada feijão do fundo e de outros feijões
- Permitir a extração de características apenas dos pixels que pertencem ao feijão
- Facilitar a criação de imagens segmentadas de cada feijão individual

**Como são usadas no código**:
- Para extrair características de cor, forma e textura de cada feijão
- Para criar imagens isoladas de cada feijão com fundo branco

### 2. `bboxes` (Bounding Boxes)

**O que são**: Uma lista de tuplas, cada uma contendo as coordenadas do retângulo delimitador de um feijão.

**Formato**: Cada tupla contém quatro valores `(x, y, w, h)`:
- `x`: Coordenada x do canto superior esquerdo do retângulo
- `y`: Coordenada y do canto superior esquerdo do retângulo
- `w`: Largura do retângulo
- `h`: Altura do retângulo

**Propósito**:
- Definir a região da imagem que contém cada feijão
- Permitir o recorte de cada feijão para processamento individual
- Calcular características como aspect_ratio e extent

**Como são usadas no código**:
- Embora armazenadas, as bounding boxes são recalculadas a partir dos contornos quando necessário

### 3. `contours` (Contornos)

**O que são**: Uma lista de arrays NumPy, cada um contendo os pontos que formam o contorno de um feijão.

**Características**:
- Cada contorno é uma sequência de pontos (x,y) que definem o perímetro do feijão
- Os contornos capturam a forma exata do feijão, não apenas um retângulo aproximado

**Propósito**:
- Permitir cálculos precisos de características de forma como área, perímetro e circularidade
- Possibilitar a visualização do contorno do feijão
- Servir como base para cálculos de momentos e outras características avançadas

**Como são usados no código**:
- Para extrair características geométricas dos feijões
- Para calcular momentos de Hu, que são descritores de forma invariantes
- Para determinar as bounding boxes para recorte dos feijões

## Fluxo de Processamento

Após a segmentação, estas três variáveis são utilizadas em conjunto para:

1. Extrair características de cada feijão usando a função `extrair_features()`
2. Recortar cada feijão individual da imagem original
3. Criar imagens isoladas de cada feijão com fundo branco
4. Salvar as imagens segmentadas e as características extraídas

Este processo permite a análise detalhada de cada feijão individualmente, possibilitando a classificação precisa entre feijões bons e ruins com base em suas características visuais.