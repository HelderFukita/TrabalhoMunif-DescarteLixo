import os
import shutil
import random

# Caminhos
train_dir = "dataset/train"
val_dir = "dataset/val"

# Porcentagem para validação
split_ratio = 0.2

# Cria pasta val se não existir
os.makedirs(val_dir, exist_ok=True)

for class_name in os.listdir(train_dir):
    class_train_path = os.path.join(train_dir, class_name)

    # Ignora se não for pasta
    if not os.path.isdir(class_train_path):
        continue

    images = os.listdir(class_train_path)

    # Remove arquivos inválidos (segurança)
    images = [img for img in images if img.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if len(images) == 0:
        print(f"⚠️ Classe vazia ignorada: {class_name}")
        continue

    # Embaralha
    random.shuffle(images)

    # Define quantas imagens vão para validação
    num_val = int(len(images) * split_ratio)

    val_images = images[:num_val]

    # Cria pasta da classe no val
    class_val_path = os.path.join(val_dir, class_name)
    os.makedirs(class_val_path, exist_ok=True)

    # Move imagens
    for img in val_images:
        src = os.path.join(class_train_path, img)
        dst = os.path.join(class_val_path, img)

        shutil.move(src, dst)

    print(f"✅ {class_name}: {num_val} imagens movidas para validação")

print("\n🚀 Dataset dividido com sucesso!")