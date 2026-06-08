# Deluxirus AI

Aplicação de inteligência artificial para classificação de resíduos com YOLOv8, backend em Flask e frontend mobile/web em React Native.

## Visão Geral

Este projeto identifica o tipo de resíduo em uma imagem e retorna:

- a classe prevista pelo modelo
- a confiança da predição
- a recomendação de descarte

## O que cada parte faz

### Backend

O backend fica em `app/app.py` e é responsável por:

- carregar o modelo treinado
- receber imagens por upload ou URL
- executar a inferência com YOLOv8
- devolver o resultado em JSON
- traduzir a classe para pt-BR e mapear o descarte

### Frontend

O frontend em React Native fica na pasta `app/` do projeto Expo e é responsável por:

- exibir a tela de introdução
- permitir acesso à funcionalidade principal
- capturar imagem pela câmera
- importar imagem da galeria no mobile e no web
- mostrar a prévia da imagem importada
- exibir o resultado da classificação

### Treinamento

O script `app/train.py` é usado para treinar o modelo com o dataset local.

## Tecnologias Utilizadas

- Python 3.10 / 3.11
- YOLOv8 (Ultralytics)
- PyTorch
- Flask
- Flask-CORS
- React Native
- Expo Router
- Expo Camera
- Expo Image Picker

## Requisitos

- Python instalado
- Node.js e npm instalados
- Dependências Python instaladas
- Dependências do frontend instaladas com npm

### GPU CUDA é obrigatória?

Não. O projeto funciona sem placa de vídeo com CUDA.

- Com GPU CUDA e PyTorch compatível, o treinamento fica mais rápido.
- Sem GPU, o treino roda normalmente na CPU, apenas com desempenho menor.
- Para testes, desenvolvimento e inferência, CPU é suficiente.

### Como verificar se a GPU está ativa

Antes de iniciar o treinamento, você pode confirmar se o PyTorch está enxergando a GPU com este comando:

```bash
python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'Nenhuma')"
```

Se a GPU estiver ativa, a saída deve indicar `CUDA: True` e mostrar o nome da placa. Se aparecer `CUDA: False`, o treino vai continuar funcionando na CPU.

## Instalação

### 1. Atualizar o pip

```bash
python -m pip install --upgrade pip
```

### 2. Instalar PyTorch

#### Com GPU CUDA 11.8

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### Somente CPU

```bash
pip install torch torchvision torchaudio
```

### 3. Instalar dependências do backend

```bash
pip install flask flask-cors ultralytics opencv-python pillow numpy requests
```

### 4. Instalar dependências do frontend

Na raiz do projeto:

```bash
npm install
```

### 5. Instalar Expo Camera, se necessário

```bash
npx expo install expo-camera
```

## Execução

### Backend

```bash
cd app
python app.py
```

Servidor disponível em:

```bash
http://localhost:5000
```

### Frontend

Na raiz do projeto:

```bash
npm run web
```

Ou, para abrir em outras plataformas do Expo:

```bash
npm start
```

## Treinamento do Modelo

```bash
cd app
python train.py
```

Se estiver usando CPU, o treinamento continua funcionando. Apenas espere mais tempo para concluir.

## EndPoint de Classificação

### POST `/detect`

Aceita imagem por upload ou URL pública.

#### Exemplo com URL

```json
{
  "url": "https://exemplo.com/imagem.jpg"
}
```

#### Resposta

```json
{
  "class": "plastic",
  "class_pt": "Plástico",
  "confidence": 0.98,
  "disposal": "Lixeira de Plástico ♻️"
}
```

## Estrutura Principal

```text
app/
├── app.py
├── train.py
├── HomeScreen.tsx
├── scan.tsx
├── index.tsx
└── dataset/
```

## Observações

- O modelo utilizado é um classificador YOLOv8 (`yolov8n-cls`).
- A interface foi pensada para mobile como prioridade, mas também funciona no web.
- A classe exibida na tela é traduzida para pt-BR.
