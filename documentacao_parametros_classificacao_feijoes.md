# Documentação dos Parâmetros para Classificação de Feijões

Este documento explica cada parâmetro considerado para a identificação de feijões bons e ruins no sistema de processamento de imagens.

## Visão Geral

O sistema utiliza técnicas de processamento de imagens e visão computacional para extrair características (features) de imagens de feijões. Estas características são utilizadas para treinar um modelo de aprendizado de máquina que classifica os feijões como "bons" ou "ruins". Os parâmetros são divididos em três categorias principais:

1. **Características de Cor**
2. **Características de Forma**
3. **Características de Textura**

## Características de Cor

As características de cor capturam informações sobre a distribuição de cores nos feijões, o que pode indicar maturidade, doenças ou defeitos.

### Valores Médios dos Canais de Cor (BGR)

| Parâmetro | Descrição | Relevância para Classificação |
|-----------|-----------|-------------------------------|
| `mean_b` | Valor médio do canal Azul (Blue) | Feijões ruins podem apresentar coloração azulada devido a fungos ou mofo |
| `mean_g` | Valor médio do canal Verde (Green) | Feijões imaturos podem ter tonalidade esverdeada |
| `mean_r` | Valor médio do canal Vermelho (Red) | Feijões maduros e saudáveis geralmente têm tons mais avermelhados |

### Desvio Padrão dos Canais de Cor (BGR)

| Parâmetro | Descrição | Relevância para Classificação |
|-----------|-----------|-------------------------------|
| `std_b` | Desvio padrão do canal Azul | Indica variabilidade na coloração azul; maior variabilidade pode indicar manchas ou defeitos |
| `std_g` | Desvio padrão do canal Verde | Indica variabilidade na coloração verde; pode revelar áreas com diferentes níveis de maturação |
| `std_r` | Desvio padrão do canal Vermelho | Indica variabilidade na coloração vermelha; pode revelar manchas ou descoloração |

## Características de Forma

As características de forma descrevem a geometria e morfologia dos feijões, o que pode indicar desenvolvimento adequado ou deformidades.

| Parâmetro | Descrição | Relevância para Classificação |
|-----------|-----------|-------------------------------|
| `area` | Área total do feijão em pixels | Feijões muito pequenos ou muito grandes podem indicar desenvolvimento anormal |
| `perimeter` | Perímetro do contorno do feijão | Relacionado ao tamanho e forma do feijão |
| `circularity` | Medida de quão circular é o feijão (4π × área / perímetro²) | Feijões saudáveis tendem a ter formas mais regulares; valores próximos a 1 indicam forma circular |
| `aspect_ratio` | Razão entre largura e altura (w/h) | Indica o alongamento do feijão; feijões deformados podem ter valores atípicos |
| `solidity` | Razão entre a área do feijão e a área do seu casco convexo | Indica a presença de concavidades; feijões danificados podem ter valores menores |
| `extent` | Razão entre a área do feijão e a área do retângulo delimitador | Indica quão compacto é o feijão dentro de sua bounding box |

## Características de Textura

As características de textura capturam padrões na superfície dos feijões, o que pode indicar rugosidade, rachaduras ou outros defeitos superficiais.

| Parâmetro | Descrição | Relevância para Classificação |
|-----------|-----------|-------------------------------|
| `std_gray` | Desvio padrão dos valores de pixel em escala de cinza | Indica variabilidade na textura; valores altos podem indicar superfície irregular |
| `entropy` | Medida da aleatoriedade na distribuição de intensidades | Superfícies com rachaduras ou manchas tendem a ter maior entropia |
| `hu1` a `hu7` | Momentos invariantes de Hu | Descritores de forma invariantes a rotação, escala e translação; úteis para detectar deformidades sutis |

## Processo de Segmentação

Antes da extração de características, o sistema realiza um processo de segmentação para isolar cada feijão:

1. **Conversão para escala de cinza**: Simplifica a imagem para processamento
2. **Aplicação de desfoque gaussiano**: Reduz ruído na imagem
3. **Limiarização binária com método de Otsu**: Separa os feijões do fundo
4. **Operações morfológicas**: Limpa a imagem binária, removendo pequenos ruídos
5. **Detecção de contornos**: Identifica o contorno de cada feijão
6. **Filtragem por área**: Remove objetos muito pequenos (área < 200 pixels) que provavelmente são ruídos

## Conclusão

A combinação destes parâmetros permite uma análise abrangente dos feijões, considerando suas propriedades visuais em múltiplas dimensões. O sistema utiliza estas características para treinar um modelo de classificação que pode distinguir feijões bons de ruins com alta precisão.

Os parâmetros mais determinantes para a classificação geralmente são:
- Características de cor: para detectar descoloração e manchas
- Circularidade e solidity: para detectar deformidades e danos físicos
- Entropia e momentos de Hu: para detectar irregularidades na textura e forma

Esta abordagem multidimensional permite uma avaliação robusta da qualidade dos feijões, mesmo quando alguns defeitos são sutis ou difíceis de detectar com inspeção visual humana.