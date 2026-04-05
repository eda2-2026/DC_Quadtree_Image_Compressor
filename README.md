# G18_Busca_EDA2-2026.1

---

# Quadtree Image Compressor

Trabalho prático da disciplina de Estruturas de Dados 2 (EDA2 - 2026.1).
Implementacao de compressao de imagens em escala de cinza utilizando a estrutura de dados Quadtree, com busca espacial por pixel integrada para demonstrar eficiencia da arvore.

---

## Descricao

O sistema recebe uma imagem em escala de cinza e a representa como uma Quadtree, onde cada no corresponde a um bloco retangular da imagem. Blocos com baixa variancia de pixels (homogeneos) sao armazenados como folhas, guardando apenas a cor media do bloco. Blocos heterogeneos sao recursivamente divididos em quatro quadrantes ate que o criterio de homogeneidade seja satisfeito ou o tamanho minimo de bloco seja atingido.

A imagem pode ser reconstruida a partir das folhas da arvore, resultando em uma versao comprimida visualmente proxima ao original. Quanto maior o limiar de variancia aceito, maior a compressao e menor a qualidade da imagem resultante.

Alem da compressao, o sistema implementa busca espacial: dado um par de coordenadas (x, y), a arvore localiza em O(profundidade) qual folha cobre aquele pixel, demonstrando o uso da estrutura para busca eficiente.

---

## Por que Quadtree? Importancia da Estrutura de Dados

### O problema de representar imagens

Uma imagem em escala de cinza de 512x512 pixels ocupa 262.144 bytes quando armazenada de forma bruta (um byte por pixel). Para processar, buscar ou transmitir essa imagem, qualquer operacao que percorra todos os pixels tem custo **O(n)** onde `n = largura × altura`. Para imagens maiores — como fotografias de 4K (8.294.400 pixels) — esse custo se torna proibitivo.

O desafio central e: como representar e operar sobre imagens de forma que regioes homogeneas (como ceu, paredes, fundos lisos) nao exijam o mesmo custo computacional que regioes complexas (bordas, texturas, detalhes)?

### Quadtree como solucao estrutural

A **Quadtree** e uma arvore onde cada no interno possui exatamente quatro filhos, cada um correspondendo a um quadrante espacial (noroeste, nordeste, sudoeste, sudeste). Essa propriedade reflete diretamente a estrutura hierarquica de uma imagem:

- **Folhas** representam blocos homogeneos — toda uma regiao e descrita por um unico valor (a cor media), independentemente do seu tamanho em pixels.
- **Nos internos** representam regioes heterogeneas que precisam ser subdivididas para maior fidelidade.

O ganho de performance e concreto:

| Operacao | Array 2D bruto | Quadtree |
|---|---|---|
| Reconstrucao de imagem | O(largura × altura) | O(numero de folhas) |
| Busca por pixel (x, y) | O(1) com acesso direto, mas sem contexto espacial | O(log n) percorrendo a hierarquia |
| Compressao / armazenamento | O(largura × altura) por pixel | O(folhas) — regioes uniformes custam 9 bits |
| Comparacao entre imagens | O(largura × altura) | O(folhas comuns) com poda de subarvores identicas |

Em imagens com grandes areas uniformes (o caso comum em fotografias com ceu, paredes e fundos), o numero de folhas e muito menor que o total de pixels. Uma imagem 256x256 com apenas 4 regioes uniformes pode ser representada por **4 folhas** em vez de 65.536 pixels — uma reducao de mais de 16.000x.

### Busca por pixel: O(profundidade) em vez de O(n)

A busca espacial e uma das operacoes onde a Quadtree demonstra sua vantagem mais clara. Dado um par de coordenadas `(x, y)`, o algoritmo:

1. Inicia na raiz, que cobre toda a imagem.
2. Em cada no interno, determina em qual dos quatro quadrantes `(x, y)` se encontra — operacao O(1).
3. Desce recursivamente para esse quadrante.
4. Para na folha que cobre o pixel, retornando sua cor media.

O custo total e **O(profundidade da arvore)**, que e logaritmico em relacao ao tamanho da imagem. Para uma imagem 512x512 com `max_nivel=8`, o pior caso e 8 comparacoes — em vez de percorrer ate 262.144 pixels em uma busca linear.

Essa eficiencia e fundamental em aplicacoes reais como:
- **Sistemas de informacao geografica (GIS)**: localizar em qual regiao do mapa um ponto esta.
- **Motores de jogos**: detectar colisoes espaciais sem comparar todos os objetos entre si.
- **Visao computacional**: segmentar regioes de interesse sem processar cada pixel individualmente.

### Relacao entre estrutura de dados e performance

A Quadtree nao e apenas uma escolha de implementacao — e uma decisao arquitetural que muda a complexidade assintótica das operacoes fundamentais do sistema. Enquanto um array bidimensional oferece acesso O(1) por indice mas sem estrutura espacial hierarquica, a Quadtree troca esse acesso direto por uma organizacao que espelha a natureza da informacao contida na imagem.

O resultado pratico e visivel nas metricas do projeto: com limiar 20, uma fotografia tipica tem sua representacao reduzida em ~98% enquanto mantém PSNR acima de 30 dB — qualidade visual boa o suficiente para a maioria das aplicacoes, com uma fracao do custo de armazenamento e processamento.

---

## Instalacao

Requer Python 3.8 ou superior.
```bash
pip install -r requirements.txt
```

Dependencias: `Pillow`, `numpy`, `matplotlib`.

---

## Uso

**Comprimir uma imagem:**
```bash
python main.py imagens/foto.jpg saida/comprimida.png 20
```

O terceiro argumento e o limiar de variancia. Valores recomendados: entre 10 e 50.

**Benchmark de limiares:**
```bash
python main.py --benchmark imagens/foto.jpg
```

Testa limiares de 5 a 100 e plota graficos de PSNR e taxa de compressao.

---

## Parametros

| Parametro | Descricao | Padrao |
|---|---|---|
| `limiar` | Variancia maxima para considerar bloco homogeneo | 20.0 |
| `min_bloco` | Tamanho minimo de bloco em pixels | 2 |
| `max_nivel` | Profundidade maxima da arvore | 8 |

---

## Metricas

A qualidade da compressao e medida pelo **PSNR** (Peak Signal-to-Noise Ratio), expresso em dB. Valores acima de 30 dB indicam boa fidelidade visual em relacao ao original.

| Limiar | Folhas (aprox.) | Taxa de Compressao | PSNR |
|---|---|---|---|
| 5 | alta | ~93% | ~41 dB |
| 20 | media | ~98% | ~34 dB |
| 50 | baixa | ~99.6% | ~27 dB |
| 100 | muito baixa | ~99.9% | ~19 dB |

*Valores variam conforme o conteudo da imagem.*

---

## Serializacao Binaria da Arvore (Issue #9)

O projeto implementa serializacao e desserializacao compacta da QuadTree em formato binario proprio, permitindo salvar e restaurar a estrutura completa da arvore sem precisar reprocessar a imagem original.

### Como funciona

A serializacao percorre a arvore em **BFS (largura)** usando uma **fila** (`deque`), nivel por nivel. Para cada no visitado, escreve:

- `0` — no interno (os 4 filhos serao visitados em seguida na fila)
- `1` seguido de 8 bits — folha com sua cor media

A desserializacao usa a mesma fila BFS para reconstruir os nos exatamente na mesma ordem, sem necessidade de marcadores de fim ou separadores.

### Formato do arquivo `.qtb`

```
Cabecalho (13 bytes):
  'QT'        2 bytes   assinatura do formato
  versao      1 byte    uint8
  largura     2 bytes   uint16 big-endian
  altura      2 bytes   uint16 big-endian
  limiar      4 bytes   float32 big-endian
  min_bloco   1 byte    uint8
  max_nivel   1 byte    uint8

Total de bits validos  4 bytes  uint32 big-endian
Fluxo de bits BFS      ceil(bits/8) bytes
```

### Por que a fila (BFS) e essencial aqui

A BFS garante que serializar e desserializar percorram os nos **na mesma ordem**, sem precisar armazenar ponteiros ou indices de posicao no arquivo. Se a serializacao usasse DFS (pilha/recursao), a desserializacao precisaria de delimitadores para saber onde cada subarvore termina — tornando o formato mais complexo e maior. Com BFS:

1. O produtor enfileira a raiz, processa, enfileira os filhos → escreve bits em ordem.
2. O consumidor replica exatamente esse comportamento: le um bit, sabe se criara filhos ou nao, enfileira na mesma ordem.

A correspondencia 1-para-1 entre a fila do produtor e a fila do consumidor e o que torna o formato autocontido e sem overhead de metadados por no.

### Compressao real

Para imagens com regioes homogeneas, o arquivo `.qtb` pode ser drasticamente menor que a imagem bruta:

| Imagem | Pixels (bruto) | Arquivo `.qtb` | Reducao |
|--------|---------------|---------------|---------|
| 256x256 com 4 blocos uniformes | 65 536 bytes | ~22 bytes | ~2979x |
| 512x512 fotografia (limiar 20) | 262 144 bytes | variavel | depende do conteudo |

A compressao e maximizada quando os blocos da imagem sao grandes e homogeneos, pois toda uma regiao e representada por 9 bits (1 flag + 8 bits de cor) em vez de `largura × altura × 8` bits.

### API

```python
# Salvar arvore em disco
qt.salvar_arvore("saida/arvore.qtb")

# Carregar arvore do disco
qt_restaurada = QuadTree.carregar_arvore("saida/arvore.qtb")

# Reconstruir imagem normalmente
imagem = qt_restaurada.reconstruir((altura, largura))

# Ou trabalhar direto com bytes (sem arquivo)
dados: bytes = qt.serializar()
qt2 = QuadTree.deserializar(dados)
```

---

## Testes
```bash
python tests/teste_issue1.py
python tests/teste_issue2.py
python tests/teste_issue3.py
python tests/teste_issue4.py
python tests/teste_issue5.py
python tests/teste_issue6.py
python tests/teste_issue7.py
python tests/teste_issue8.py
python tests/teste_issue9.py
```

---

## Autores

Grupo 18 - EDA2 2026.1
Universidade de Brasilia
