# ♻️ Classificação de Resíduos para Reciclagem: Aplicando o modelo SVM do projeto DeluxiriusIA com uso do YOLOV8

## 👥 Integrantes da Equipe
* **Helder Augusto Kusagari Fukita** - RA: `23197574-2`
* **Erick Oliveira de Souza** - RA: `23223824-2`
* **Andrei Luiz Silva** - RA: `23087473-2`

---

## 📝 1. Descrição do Problema e Contextualização
A gestão eficiente de resíduos sólidos e a triagem correta de materiais recicláveis representam um dos maiores desafios ecológicos e logísticos da atualidade. A automação desse processo por meio de visão computacional pode acelerar as esteiras de reciclagem e reduzir a contaminação de lotes de materiais.

O objetivo deste projeto é desenvolver e comparar duas abordagens de Inteligência Artificial para classificar imagens de diferentes tipos de resíduos em suas respectivas categorias.

### 🔬 Hipótese Científica
* **Hipótese:** Modelos baseados em Deep Learning (Redes Neurais Convolucionais profundas) apresentarão uma acurácia significativamente superior em comparação aos métodos de Machine Learning tradicional. Isso ocorre porque redes convolucionais capturam padrões espaciais, texturas e contextos complexos diretamente dos pixels. Em contrapartida, os métodos tradicionais, por necessitarem de severa redução de dimensionalidade e perda de informação de cor para viabilidade computacional, apresentarão menor acurácia, contudo com um custo de tempo de treinamento drasticamente inferior (*trade-off* de eficiência vs eficácia).

---

## 📊 2. Dataset e Preparação dos Dados
A base de dados utilizada consiste em imagens de resíduos divididas em classes organizadas de forma categórica (ex: plástico, vidro, papel, metal, etc.).

Como os dois algoritmos escolhidos possuem naturezas matemáticas distintas, o pipeline de preparação de dados foi bifurcado:

1. **Pipeline para YOLOv8 (Deep Learning):** As imagens são alimentadas com dimensões de $224 \times 224$ pixels mantendo seus 3 canais de cor originais (RGB), permitindo que a rede extraia características cromáticas cruciais para a identificação dos materiais.
2. **Pipeline para SVM (Machine Learning Tradicional):** O SVM sofre com a "Maldição da Dimensionalidade" ao processar matrizes brutas grandes. Portanto, as imagens foram convertidas para **Escala de Cinza** (eliminando variações irrelevantes de iluminação e reduzindo canais de 3 para 1) e redimensionadas para $64 \times 64$ pixels. Por fim, a matriz foi "achatada" (`.flatten()`) em um vetor unidimensional de $4096$ características antes de alimentar o classificador.

Pegamos o banco de dados para treinar no Kaggle: 
  https://www.kaggle.com/datasets/sumn2u/garbage-classification-v2/?select=original

---

## 🛠️ 3. Modelos e Métodos Utilizados

O projeto foi rigorosamente estruturado atendendo às duas frentes exigidas pelo requisitos:

### ⚙️ Parte 1: Machine Learning Tradicional (SVM)
* **Algoritmo:** Support Vector Machine (Classifier) com kernel RBF.
* **Script:** `train_svm.py`
* **Abordagem por trás dos panos:** Tenta traçar hiperplanos ótimos de separação em um espaço multidimensional para segregar as classes de resíduos. Diferente de redes neurais, o SVM resolve uma otimização matemática direta e não utiliza o conceito de épocas interativas de retropropagação.

### 🧠 Parte 2: Deep Learning & Redes Neurais (YOLOv8)
* **Algoritmo:** YOLOv8 Nano para Classificação (`yolov8n-cls.pt`).
* **Script:** `train.py`
* **Abordagem por trás dos panos:** Uma rede neural convolucional profunda de última geração. O modelo foi treinado ao longo de **30 épocas**, refinando seus pesos sinápticos através de gradiente descendente a cada passagem completa pelo dataset de treino.

---

## 📈 4. Avaliação e Comparação dos Resultados

*(Nota Científica: Como o problema abordado é de **Classificação**, métricas de Regressão como Erro Médio Absoluto (MAE) ou Erro Quadrático Médio (MSE) listadas no edital não são aplicáveis. Foram utilizadas as métricas estatísticas adequadas de classificação: Acurácia, Precisão, Recall e F1-Score).*

### 📊 Resultados Obtidos (Resumo)

| Métrica | SVM (Parte 1) | YOLOv8 (Parte 2) | 
| :--- | :---: | :---: |
| **Acurácia Final** | *[Ex: 72.00%]* | *[Ex: 94.50%]* |
| **Tempo de Treino** | *[Ex: 12 seg]* | *[Ex: 15 min]* |
| **Loss (Perda Final)** | N/A | *[Ex: 0.182]* |

### 🖼️ Gráficos e Análises Geradas
O projeto gera automaticamente uma estrutura padronizada de relatórios visuais salvos na pasta `/runs`:
* **`analise_treinamento_yolo.png`:** Curvas de perda (*Loss Train/Val*) e evolução da acurácia ao longo das 30 épocas da rede profunda. (Gerado por `plot_training_curves.py`).
* **`curva_aprendizado_svm.png`:** Avaliação do SVM variando o volume de dados de treinamento (de 10% a 100%) para simular a curva de aprendizado do modelo tradicional. (Gerado por `plot_svm_learning_curve.py`).
* **`matriz_confusao.png` (na pasta do SVM):** Mapeamento detalhado de erros e acertos cruzados por classe do classificador estatístico.
* **`comparacao_modelos_completa.png`:** Infográfico final que coloca lado a lado o desempenho em acurácia e tempo de ambos os modelos. (Gerado por `comparacao_grafica.py`).

---

## 💡 5. Análise Crítica e Conclusão
Os testes práticos confirmaram a hipótese inicial. O **YOLOv8** demonstrou superioridade robusta em cenários práticos de classificação visual devido à sua arquitetura convolucional profunda capaz de compreender nuances geométricas dos resíduos, tornando-o ideal para aplicação em sistemas de triagem automatizada em tempo real que demandam altíssima confiabilidade.

Por outro lado, o **SVM** provou-se uma alternativa extremamente barata computacionalmente. Treinado em uma fração ínfima de tempo e sem a necessidade de hardware especializado (GPU), ele se destaca como uma excelente solução de baixo custo para dispositivos embarcados limitados, desde que o ambiente de captura de imagem seja controlado.

---

## 🚀 6. Como Executar o Projeto

### Pré-requisitos
bash
pip install -r requirements.txt

---

# 📊 Guia Completo de Métricas - DeluxirusIA

## ✅ Métricas Obrigatórias do Edital

### 1. **Erro Médio Absoluto (MAE) ou Erro Quadrático Médio (MSE)**
**Status:** ✅ Sua tarefa é de CLASSIFICAÇÃO (não regressão), então não precisa.
- Problema: Classificação de resíduos (10 classes)
- Métricas apropriadas: Accuracy, Precision, Recall, F1-Score

### 2. **Curva de Perda Durante o Treinamento** 
**Status:** ✅ **DISPONÍVEL - Execute:**
```bash
python plot_training_curves.py
```
**Onde encontrar:**
- Arquivo: `runs/classify/train/results.csv`
- Colunas relevantes:
  - `train/loss` - Perda do treinamento
  - `val/loss` - Perda da validação
  - `metrics/accuracy_top1` - Acurácia top-1

### 3. **Comparação Gráfica Entre Modelos**
**Status:** ✅ **DISPONÍVEL - Execute:**
```bash
python comparacao_grafica_melhorada.py
```
**Gera:**
- Gráfico comparativo YOLOv8 vs SVM
- Compara: Acurácia, Tempo de Treinamento, Loss

### 4. **Indicadores Adequados ao Problema (Classificação)**
**Status:** ✅ **TODOS JÁ EXISTEM - Execute:**
```bash
python train_svm_melhorado.py
```
**Métricas por classe:**
- ✅ Precision (Precisão)
- ✅ Recall (Revocação)
- ✅ F1-Score
- ✅ Support (Número de amostras)

**Métricas Agregadas:**
- ✅ **Accuracy** - Acurácia geral
- ✅ **Macro Avg** - Média não ponderada entre classes
- ✅ **Weighted Avg** - Média ponderada por suporte
- ✅ **Confusion Matrix** - Matriz de confusão

---

## 🚀 Como Usar

### Passo 1: Treinar o YOLO (se ainda não fez)
```bash
python train.py
```
Gera: `runs/classify/train/results.csv` com todas as curvas de perda

### Passo 2: Visualizar Curvas de Perda do YOLO
```bash
python plot_training_curves.py
```
**Saída:**
- Gráfico: `analise_treinamento_yolo.png`
- Mostra: Loss, Accuracy, Learning Rate ao longo dos épocas

### Passo 3A: Gerar Curva de Aprendizado do SVM ⭐ NOVO
```bash
python plot_svm_learning_curve.py
```
**Por que SVM é diferente?**
- YOLO treina em **épocas** → gera curva de perda ao longo do tempo
- SVM treina **uma única vez** → não tem "épocas"
- Solução: Usar **curva de aprendizado** (acurácia vs % de dados)

**Saída:**
- Gráfico: `curva_aprendizado_svm.png`
- Mostra: Como SVM melhora conforme recebe mais dados de treinamento

### Passo 3B: Treinar e Avaliar o SVM Completo
```bash
python train_svm.py
```
**Saída:**
- Pasta criada: `runs/svm/train/` (ou `train2`, `train3` se já existir)
- No console: Relatório completo com todas as métricas
- Arquivos salvos:
  - `modelo_svm.pkl` - Modelo treinado (reutilizável)
  - `results.csv` - Métricas em CSV (similar ao YOLO!)
  - `classification_report.txt` - Relatório detalhado
  - `matriz_confusao.png` - Gráfico da matriz
- Valores: Accuracy, Precision, Recall, F1-Score, Macro Avg, Weighted Avg

### Passo 4: Comparar Modelos Graficamente
```bash
python comparacao_grafica_melhorada.py
```
**Saída:**
- Gráfico: `comparacao_modelos_completa.png`
- Compara os dois modelos lado a lado

---

## 📋 Localização de Cada Métrica

| Métrica | Onde Encontrar | Arquivo |
|---------|---|---|
| **Curva de Loss (Perda) - YOLO** | `runs/classify/train/results.csv` | `results.csv` |
| **Curva de Aprendizado - SVM** ⭐ | `plot_svm_learning_curve.py` | `curva_aprendizado_svm.png` |
| **Acurácia YOLO** | `runs/classify/train/results.csv` | `results.csv` (coluna: `metrics/accuracy_top1`) |
| **Acurácia SVM** | `runs/svm/train/results.csv` | `results.csv` (métrica: `accuracy`) |
| **Precision/Recall/F1-Score (SVM)** | `runs/svm/train/classification_report.txt` | `classification_report.txt` + console |
| **Accuracy SVM** | `runs/svm/train/results.csv` | `results.csv` |
| **Macro Avg (SVM)** | `runs/svm/train/results.csv` | `results.csv` |
| **Weighted Avg (SVM)** | `runs/svm/train/results.csv` | `results.csv` |
| **Matriz de Confusão (SVM)** | `runs/svm/train/` | `matriz_confusao.png` |
| **Comparação Modelos** | `comparacao_grafica_melhorada.py` | `comparacao_modelos_completa.png` |

---

## 🎯 Resumo das Métricas Geradas

### YOLO (Deep Learning)
- ✅ Loss (Treino e Validação)
- ✅ Accuracy Top-1 e Top-5
- ✅ Learning Rate por época
- ✅ Tempo de treinamento

### SVM (Machine Learning)
- ✅ **Curva de Aprendizado** ⭐ (novo!)
- ✅ Precision por classe
- ✅ Recall por classe
- ✅ F1-Score por classe
- ✅ Accuracy geral
- ✅ Macro Average
- ✅ Weighted Average
- ✅ Confusion Matrix

### Comparação
- ✅ Gráfico: Acurácia YOLO vs SVM
- ✅ Gráfico: Tempo de treinamento
- ✅ Gráfico: Loss do YOLO
- ✅ Gráfico: Curva de Aprendizado do SVM

---

## ⚡ Diferença Entre YOLO e SVM: Curvas

### YOLO (Rede Neural - Deep Learning)
```
Treina em ÉPOCAS
📉 Epoch 1: Loss = 1.35 → Accuracy = 85%
📉 Epoch 2: Loss = 0.61 → Accuracy = 89%
📉 Epoch 3: Loss = 0.49 → Accuracy = 90%
...
📉 Epoch 30: Loss = 0.08 → Accuracy = 94%

Resultado: CURVA DE PERDA (Loss diminui ao longo do tempo)
```

### SVM (Machine Learning)
```
Treina UMA ÚNICA VEZ (sem épocas)
✅ Treina com 10% dos dados → Accuracy = 60%
✅ Treina com 30% dos dados → Accuracy = 70%
✅ Treina com 60% dos dados → Accuracy = 80%
✅ Treina com 100% dos dados → Accuracy = 88%

Resultado: CURVA DE APRENDIZADO (Accuracy melhora com mais dados)
```

**Conclusão:** Ambas mostram o desempenho do modelo! 
- YOLO: Performance melhora **ao longo do treinamento**
- SVM: Performance melhora **conforme recebe mais dados**

---

Alguns valores precisam ser atualizados manualmente em `comparacao_grafica_melhorada.py`:

```python
# Linha ~28-29
SVM_ACCURACY = 0.72  # ⚠️ SUBSTITUA PELO VALOR REAL (obtido de train_svm_melhorado.py)
SVM_TRAINING_TIME = 300  # ⚠️ SUBSTITUA PELO VALOR REAL (em segundos)
```

Após executar `train_svm_melhorado.py`, atualize esses valores com os resultados obtidos.

---

## � Nova Estrutura de Pastas (SVM igual YOLO!)

O SVM agora cria uma **estrutura de pastas organizada** como o YOLO:

```
runs/
├── classify/              ← YOLO
│   ├── train/
│   ├── train3/
│   └── ...
└── svm/                   ← SVM (NOVO!)
    ├── train/
    │   ├── modelo_svm.pkl
    │   ├── results.csv
    │   ├── classification_report.txt
    │   └── matriz_confusao.png
    ├── train2/
    ├── train3/
    └── ...
```

**Benefícios:**
- ✅ Organização clara dos treinamentos
- ✅ Histórico completo (train, train2, train3...)
- ✅ Modelo salvo para reutilização
- ✅ Resultados em CSV para análise
- ✅ Mesma estrutura que YOLO!

Para mais detalhes, veja [ESTRUTURA_PASTAS_SVM.md](ESTRUTURA_PASTAS_SVM.md)

---

## �📝 Notas Finais

- Seu problema é de **CLASSIFICAÇÃO**, não regressão → MAE/MSE não são aplicáveis
- As métricas mais importantes: **Accuracy, Precision, Recall, F1-Score**
- Você tem **dois modelos** para comparar (YOLO e SVM) ✅
- Todos os gráficos serão salvos em PNG em alta resolução (300 DPI)

**Tudo que o edital pede já está implementado! 🎉**
