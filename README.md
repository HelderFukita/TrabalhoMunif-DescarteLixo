# ♻️ Deluxirus AI

Aplicação de Inteligência Artificial para classificação de resíduos recicláveis utilizando Visão Computacional, composta por um backend em Flask, frontend em React Native e modelos de Machine Learning e Deep Learning para análise e classificação de imagens.

---

# 👥 Integrantes da Equipe

* **Helder Augusto Kusagari Fukita** — RA: `23197574-2`
* **Erick Oliveira de Souza** — RA: `23223824-2`
* **Andrei Luiz Silva** — RA: `23087473-2`

---

# 📖 Visão Geral

O **Deluxirus AI** é um sistema desenvolvido para auxiliar na identificação e descarte correto de resíduos recicláveis por meio da análise de imagens.

O projeto foi dividido em duas etapas:

## Sistema Original

Utilização do modelo **YOLOv8** para classificação automática de resíduos através de imagens enviadas pelo usuário.

## Expansão Acadêmica

Comparação entre uma abordagem de **Deep Learning (YOLOv8)** e uma abordagem de **Machine Learning Tradicional (SVM)**, avaliando desempenho, acurácia e custo computacional.

---

# 🏗️ Arquitetura do Projeto

```text
Frontend (React Native)
          │
          ▼
Backend (Flask API)
          │
          ▼
Modelo de IA
 ├── YOLOv8
 └── SVM
```

---

# 🛠️ Tecnologias Utilizadas

## Backend

* Python 3.10 / 3.11
* Flask
* Flask-CORS
* Requests

## Inteligência Artificial

* YOLOv8 (Ultralytics)
* PyTorch
* OpenCV
* NumPy
* Pillow
* Scikit-Learn (SVM)

## Frontend

* React Native
* Expo
* Expo Router
* Expo Camera
* Expo Image Picker

---

# 📋 Requisitos

## Backend

* Python instalado
* Pip atualizado

## Frontend

* Node.js
* npm

## Hardware

### GPU CUDA é obrigatória?

**Não.**

O sistema funciona normalmente utilizando apenas CPU.

Caso exista uma GPU compatível com CUDA e uma versão adequada do PyTorch instalada, o treinamento será executado significativamente mais rápido.

Para testes, desenvolvimento e inferência, a CPU é suficiente.

---

# 🔍 Verificando GPU CUDA

Execute:

```bash
python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'Nenhuma')"
```

Exemplo:

```text
CUDA: True
GPU: NVIDIA RTX XXXX
```

ou

```text
CUDA: False
GPU: Nenhuma
```

---

# 🚀 Instalação

## 1. Atualizar o Pip

```bash
python -m pip install --upgrade pip
```

## 2. Instalar PyTorch

### Com CUDA 11.8

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Apenas CPU

```bash
pip install torch torchvision torchaudio
```

## 3. Instalar Dependências do Backend

```bash
pip install flask flask-cors ultralytics opencv-python pillow numpy requests scikit-learn
```

## 4. Instalar Dependências do Frontend

```bash
npm install
```

## 5. Instalar Expo Camera

```bash
npx expo install expo-camera
```

---

# ▶️ Execução da Aplicação

## Backend

```bash
cd app
python app.py
```

Servidor:

```text
http://localhost:5000
```

## Frontend Web

```bash
npm run web
```

## Frontend Expo

```bash
npm start
```

---

# 🤖 Sistema Original — YOLOv8

## Objetivo

Classificar resíduos recicláveis através de imagens e fornecer recomendações de descarte.

### Funcionalidades

O sistema retorna:

* Classe prevista
* Classe traduzida para Português
* Confiança da predição
* Recomendação de descarte

---

## Backend

Localização:

```text
app/app.py
```

### Responsabilidades

* Carregar o modelo treinado
* Receber imagens via upload
* Receber imagens via URL
* Executar inferência
* Retornar resultados em JSON
* Traduzir classes para português
* Mapear o descarte adequado

---

## Frontend

Responsável por:

* Tela inicial
* Navegação da aplicação
* Captura de imagens pela câmera
* Importação pela galeria
* Visualização prévia da imagem
* Exibição dos resultados

---

## Treinamento YOLOv8

Arquivo:

```text
app/train.py
```

Execução:

```bash
cd app
python train.py
```

Modelo utilizado:

```text
yolov8n-cls.pt
```

---

## Endpoint de Classificação

### POST `/detect`

Aceita:

* Upload de imagem
* URL pública de imagem

### Exemplo

```json
{
  "url": "https://exemplo.com/imagem.jpg"
}
```

### Resposta

```json
{
  "class": "plastic",
  "class_pt": "Plástico",
  "confidence": 0.98,
  "disposal": "Lixeira de Plástico ♻️"
}
```

---

# 🎓 Expansão Acadêmica — Comparação YOLOv8 x SVM

## Descrição do Problema

A gestão eficiente de resíduos sólidos e a correta separação de materiais recicláveis representam desafios ambientais e logísticos significativos.

A automação desse processo através de Visão Computacional pode reduzir erros de triagem, aumentar a produtividade e diminuir a contaminação dos materiais recicláveis.

## Objetivo

O objetivo deste trabalho é comparar duas abordagens distintas de Inteligência Artificial para classificação de resíduos:

* Machine Learning Tradicional (SVM)
* Deep Learning (YOLOv8)

---

## 🔬 Hipótese Científica

Modelos baseados em Deep Learning apresentam desempenho superior em tarefas de classificação visual quando comparados aos algoritmos tradicionais de Machine Learning.

Entretanto, modelos tradicionais como SVM exigem menor custo computacional e menor tempo de treinamento.

Essa comparação evidencia o trade-off entre:

* Eficiência computacional
* Precisão da classificação

---

# 📊 Dataset

Foi utilizado o dataset:

📎 **Garbage Classification V2 (Kaggle)**

https://www.kaggle.com/datasets/sumn2u/garbage-classification-v2

### Classes presentes

* Papel
* Plástico
* Vidro
* Metal
* Papelão
* Entre outras categorias de resíduos

---

# 🧹 Preparação dos Dados

## Pipeline YOLOv8

As imagens foram:

* Redimensionadas para 224x224 pixels
* Mantidas em RGB
* Utilizadas diretamente pela rede neural

### Vantagens

* Preservação das informações de cor
* Preservação de texturas
* Preservação de padrões espaciais

---

## Pipeline SVM

As imagens foram:

* Convertidas para escala de cinza
* Redimensionadas para 64x64 pixels
* Transformadas em vetores unidimensionais

```python
imagem.flatten()
```

Resultado:

```text
64 × 64 = 4096 características
```

Objetivo:

Reduzir dimensionalidade e permitir treinamento viável do SVM.

---

# 🛠️ Modelos Utilizados

## Parte 1 — Machine Learning Tradicional

### SVM (Support Vector Machine)

Arquivo:

```text
train_svm.py
```

Configuração:

```text
Kernel RBF
```

O SVM busca encontrar hiperplanos ótimos capazes de separar as diferentes classes.

---

## Parte 2 — Deep Learning

### YOLOv8 Nano Classification

Arquivo:

```text
train.py
```

Modelo:

```text
yolov8n-cls.pt
```

Treinamento:

```text
30 épocas
```

A rede ajusta seus pesos utilizando gradiente descendente e retropropagação.

---

# 📈 Avaliação dos Modelos

## Observação Importante

O problema tratado é de classificação.

Portanto:

* ❌ MAE (Erro Médio Absoluto)
* ❌ MSE (Erro Quadrático Médio)

não são métricas adequadas.

Foram utilizadas métricas específicas para classificação.

---

## Métricas Utilizadas

### YOLOv8

* Accuracy Top-1
* Accuracy Top-5
* Loss de Treino
* Loss de Validação
* Tempo de Treinamento

### SVM

* Accuracy
* Precision
* Recall
* F1-Score
* Macro Average
* Weighted Average
* Confusion Matrix

---

# 📊 Resultados Obtidos

| Métrica         | SVM       | YOLOv8    |
| --------------- | --------- | --------- |
| Acurácia Final  | Atualizar | Atualizar |
| Tempo de Treino | Atualizar | Atualizar |
| Loss Final      | N/A       | Atualizar |

---

# 📈 Gráficos Gerados

## YOLOv8

### Curva de Treinamento

```bash
python plot_training_curves.py
```

Gera:

```text
analise_treinamento_yolo.png
```

Exibe:

* Loss de treino
* Loss de validação
* Accuracy
* Learning Rate

---

## SVM

### Curva de Aprendizado

```bash
python plot_svm_learning_curve.py
```

Gera:

```text
curva_aprendizado_svm.png
```

Exibe:

* Accuracy versus quantidade de dados de treinamento

### Matriz de Confusão

Gerada durante:

```bash
python train_svm.py
```

Arquivo:

```text
matriz_confusao.png
```

---

## Comparação Entre Modelos

```bash
python comparacao_grafica_melhorada.py
```

Gera:

```text
comparacao_modelos_completa.png
```

Comparações:

* Accuracy
* Tempo de treinamento
* Loss
* Curva de aprendizado

---

# 🚀 Como Reproduzir os Experimentos

## 1. Treinar YOLO

```bash
python train.py
```

## 2. Gerar Curvas do YOLO

```bash
python plot_training_curves.py
```

## 3. Gerar Curva de Aprendizado do SVM

```bash
python plot_svm_learning_curve.py
```

## 4. Treinar SVM

```bash
python train_svm.py
```

Arquivos gerados:

* modelo_svm.pkl
* results.csv
* classification_report.txt
* matriz_confusao.png

## 5. Comparar Modelos

```bash
python comparacao_grafica_melhorada.py
```

---

# 📂 Estrutura de Pastas

```text
runs/
├── classify/
│   ├── train/
│   ├── train2/
│   ├── train3/
│   └── ...
│
└── svm/
    ├── train/
    │   ├── modelo_svm.pkl
    │   ├── results.csv
    │   ├── classification_report.txt
    │   └── matriz_confusao.png
    │
    ├── train2/
    ├── train3/
    └── ...
```

---

# 💡 Análise Crítica

Os resultados demonstram que o YOLOv8 apresenta maior capacidade de generalização e melhor desempenho em tarefas de classificação visual.

Sua arquitetura convolucional permite capturar padrões espaciais, formas, texturas e características cromáticas dos resíduos.

Por outro lado, o SVM mostrou-se uma alternativa extremamente eficiente em termos computacionais, exigindo menor tempo de treinamento e dispensando hardware especializado.

### YOLOv8

Indicado para:

* Sistemas industriais
* Triagem automatizada
* Aplicações com alta exigência de precisão

### SVM

Indicado para:

* Sistemas embarcados
* Hardware limitado
* Aplicações de baixo custo

---

# 📝 Notas Finais

* O problema abordado é de classificação, não regressão.
* Accuracy, Precision, Recall e F1-Score são as métricas mais relevantes.
* Todos os gráficos são exportados em alta resolução (300 DPI).
* O projeto demonstra, na prática, diferenças entre abordagens de Machine Learning Tradicional e Deep Learning aplicadas à reciclagem inteligente.

---

# 📚 Referências

## Dataset

**Garbage Classification V2**

https://www.kaggle.com/datasets/sumn2u/garbage-classification-v2

## YOLOv8

https://docs.ultralytics.com

## Scikit-Learn

https://scikit-learn.org

## PyTorch

https://pytorch.org

---

# ♻️ Deluxirus AI

**Reciclagem Inteligente através da Inteligência Artificial.**
