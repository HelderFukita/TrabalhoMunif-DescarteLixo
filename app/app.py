from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image, UnidentifiedImageError
import io
import requests
import torch

# ================================
# 🔥 CONFIGURAÇÃO DE DEVICE (GPU/CPU)
# ================================
device = "cuda" if torch.cuda.is_available() else "cpu"
print("🚀 Dispositivo em uso:", device)

# ================================
# 🚀 INICIALIZAÇÃO DO APP
# ================================
app = Flask(__name__)
CORS(app)

# ================================
# 🧠 CARREGA MODELO TREINADO
# ================================
model = YOLO("runs/classify/train/weights/best.pt")
model.to(device)

# (Opcional) usar half precision se for GPU
if device == "cuda":
    model.model.half()
    print("⚡ Half precision (FP16) ativado")

# Verificação REAL do device
print("📌 Modelo está em:", next(model.model.parameters()).device)

# ================================
# ♻️ MAPEAMENTO DE DESCARTE
# ================================
lixeira = {
    "plastic": "Lixeira de Plástico ♻️",
    "glass": "Lixeira de Vidro 🍾",
    "paper": "Lixeira de Papel 📄",
    "metal": "Lixeira de Metal 🔩",
    "cardboard": "Lixeira de Papelão 📦",
    "biological": "Lixo Orgânico 🌱",
    "battery": "Descarte Especial 🔋",
    "clothes": "Doação ou Reuso 👕",
    "shoes": "Reuso ou Doação 👟",
    "trash": "Lixo Comum 🗑️"
}

class_pt = {
    "plastic": "Plástico",
    "glass": "Vidro",
    "paper": "Papel",
    "metal": "Metal",
    "cardboard": "Papelão",
    "biological": "Orgânico",
    "battery": "Bateria",
    "clothes": "Roupas",
    "shoes": "Calçados",
    "trash": "Lixo Comum"
}

# ================================
# 🔍 ENDPOINT DE DETECÇÃO
# ================================
@app.route("/detect", methods=["POST"])
def detect():
    image = None

    try:
        # Upload de imagem
        if "image" in request.files:
            file = request.files["image"]
            image = Image.open(io.BytesIO(file.read())).convert("RGB")

        # URL
        elif request.is_json:
            data = request.get_json()
            url = data.get("url")

            if not url:
                return jsonify({"error": "URL não fornecida"}), 400

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            image = Image.open(io.BytesIO(response.content)).convert("RGB")

        else:
            return jsonify({"error": "Nenhuma imagem enviada"}), 400

        # ================================
        # 🔥 INFERÊNCIA
        # ================================
        results = model(image)

        probs = results[0].probs

        class_id = probs.top1
        confidence = float(probs.top1conf)
        class_name = model.names[class_id]

        return jsonify({
            "class": class_name,
            "class_pt": class_pt.get(class_name, class_name),
            "confidence": confidence,
            "disposal": lixeira.get(class_name, "Descarte desconhecido")
        })

    except requests.exceptions.RequestException:
        return jsonify({"error": "Não foi possível acessar a URL da imagem"}), 400
    except UnidentifiedImageError:
        return jsonify({"error": "Formato de imagem inválido"}), 400
    except OSError:
        return jsonify({"error": "Formato de imagem inválido"}), 400
    except Exception as e:
        return jsonify({"error": "Falha ao processar a imagem"}), 500


# ================================
# 🚀 START DO SERVIDOR
# ================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)