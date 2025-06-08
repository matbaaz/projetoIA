# Diretrizes do Projeto de Processamento de Imagens de Feijões

Este documento fornece diretrizes para desenvolvimento, teste e configuração do projeto de Processamento de Imagens de Feijões.

## Instruções de Compilação/Configuração

### Configuração do Ambiente

1. **Ambiente Python**: Este projeto requer Python 3.6 ou superior.

2. **Instalação de Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

   O projeto depende dos seguintes pacotes:
   - opencv-python: Para operações de processamento de imagens
   - numpy: Para operações numéricas
   - scikit-learn: Para algoritmos de aprendizado de máquina
   - pandas: Para manipulação de dados

3. **Estrutura de Diretórios**:
   O projeto espera a seguinte estrutura de diretórios:
   ```
   raiz_do_projeto/
   ├── bons/                  # Diretório contendo imagens de feijões "bons"
   ├── ruins/                 # Diretório contendo imagens de feijões "ruins"
   ├── bons_recorte/          # Imagens recortadas de feijões bons geradas automaticamente
   ├── bons_segregado/        # Imagens segmentadas de feijões bons geradas automaticamente
   ├── ruins_recorte/         # Imagens recortadas de feijões ruins geradas automaticamente
   ├── ruins_segregado/       # Imagens segmentadas de feijões ruins geradas automaticamente
   ├── monta.py               # Script principal para geração de conjunto de dados
   ├── segmenta.py            # Módulo para segmentação de feijões
   └── requirements.txt       # Dependências do projeto
   ```

   Os diretórios `*_recorte` e `*_segregado` serão criados automaticamente se não existirem.

## Informações de Teste

### Executando Testes Existentes

1. **Teste de Segmentação**:
   ```bash
   python test_segmenta.py
   ```
   Este teste verifica a funcionalidade de segmentação de feijões:
   - Carregando uma imagem de exemplo do diretório 'ruins' ou 'bons'
   - Segmentando os feijões na imagem
   - Criando uma visualização com caixas delimitadoras e contornos
   - Salvando a visualização em 'test_segmentation_result.jpg'

2. **Teste de Geração de Conjunto de Dados**:
   ```bash
   python test_monta.py
   ```
   Este teste verifica a funcionalidade de geração de conjunto de dados:
   - Criando um diretório de teste temporário
   - Copiando uma imagem de exemplo para o diretório de teste
   - Gerando um conjunto de dados a partir da imagem de exemplo
   - Verificando se o arquivo CSV e as imagens segmentadas foram criados corretamente

### Adicionando Novos Testes

Ao adicionar novos testes ao projeto, siga estas diretrizes:

1. **Nomenclatura de Arquivos de Teste**: Nomeie os arquivos de teste com o prefixo `test_` seguido pelo nome do módulo sendo testado (ex., `test_segmenta.py`).

2. **Estrutura da Função de Teste**:
   - Cada função de teste deve focar em testar uma funcionalidade específica
   - Use nomes de funções descritivos que indiquem o que está sendo testado
   - Inclua docstrings explicando o propósito do teste
   - Retorne um booleano indicando sucesso ou falha

3. **Limpeza de Teste**: Certifique-se de que os testes limpem quaisquer arquivos ou diretórios temporários que criem.

4. **Exemplo de Estrutura de Teste**:
   ```python
   def test_alguma_funcionalidade():
       """
       Descrição do teste explicando o que está sendo testado e como.
       """
       # Configuração
       # ...
       
       # Execute a funcionalidade sendo testada
       # ...
       
       # Verifique os resultados
       # ...
       
       # Limpeza
       # ...
       
       return booleano_de_sucesso
   ```

## Diretrizes de Desenvolvimento

### Estilo de Código

1. **PEP 8**: Siga o guia de estilo [PEP 8](https://www.python.org/dev/peps/pep-0008/) para código Python.

2. **Docstrings**: Inclua docstrings para todos os módulos, classes e funções seguindo o [estilo de docstring NumPy](https://numpydoc.readthedocs.io/en/latest/format.html).

3. **Type Hints**: Considere adicionar dicas de tipo às assinaturas de funções para melhorar a legibilidade do código e permitir verificação estática de tipos.

### Fluxo de Trabalho de Processamento de Imagens

O projeto segue este fluxo de trabalho geral para processamento de imagens de feijões:

1. **Carregamento de Imagem**: Carregue imagens usando `cv2.imread()`.

2. **Pré-processamento**:
   - Converta para escala de cinza usando `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`
   - Aplique desfoque gaussiano para reduzir ruído usando `cv2.GaussianBlur()`

3. **Segmentação**:
   - Aplique limiarização binária com o método de Otsu
   - Use operações morfológicas para limpar a imagem binária
   - Encontre contornos dos feijões

4. **Extração de Características**:
   - Extraia características de cor (média e desvio padrão dos canais BGR)
   - Extraia características de forma (área, perímetro, circularidade, etc.)
   - Extraia características de textura (entropia, momentos de Hu, etc.)

5. **Geração de Conjunto de Dados**:
   - Salve características em um arquivo CSV
   - Salve imagens de feijões segmentados

### Dicas de Depuração

1. **Visualização**: Use funções de visualização do OpenCV para depurar etapas de processamento de imagens:
   ```python
   cv2.imwrite("debug_nome_etapa.jpg", imagem_debug)
   ```

2. **Filtragem de Contorno**: Ao segmentar feijões, ajuste o limiar de área em `segmentar_feijoes()` se muitos ou poucos feijões estiverem sendo detectados:
   ```python
   if area < 200:  # Ajuste este limiar conforme necessário
       continue
   ```

3. **Limiarização HSV**: Ao recortar a folha em `recortar_folha()`, ajuste os limiares HSV se a folha não estiver sendo detectada corretamente:
   ```python
   lower_white = np.array([0, 0, 200])  # Ajuste estes valores conforme necessário
   upper_white = np.array([180, 60, 255])
   ```

### Considerações de Desempenho

1. **Tamanho da Imagem**: Imagens grandes podem retardar o processamento. Considere redimensionar imagens se o desempenho for um problema.

2. **Processamento em Lote**: Ao processar múltiplas imagens, use processamento em lote para evitar carregar todas as imagens na memória de uma vez.

3. **Processamento Paralelo**: Considere usar multiprocessamento para tarefas intensivas de CPU como extração de características.