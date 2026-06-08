"""
Script para visualizar a Curva de Aprendizado do SVM
Mostra como o desempenho melhora conforme aumenta a quantidade de dados
(Equivalente à curva de perda para SVM)
"""
import os
import cv2
import numpy as np
from sklearn import svm, metrics
import matplotlib.pyplot as plt

def load_images_from_folder(base_folder, img_size=(64, 64)):
    """Carrega imagens e retorna dados"""
    X = []
    y = []
    classes = os.listdir(base_folder)
    
    for class_idx, class_name in enumerate(classes):
        class_path = os.path.join(base_folder, class_name)
        if not os.path.isdir(class_path):
            continue
            
        for filename in os.listdir(class_path):
            img_path = os.path.join(class_path, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                img_resized = cv2.resize(img, img_size)
                X.append(img_resized.flatten())
                y.append(class_name)
                
    return np.array(X), np.array(y)

def plot_learning_curve():
    """Plota a curva de aprendizado do SVM"""
    
    print("⏳ Carregando dados de treinamento...")
    X_train, y_train = load_images_from_folder("dataset/train")
    
    print("⏳ Carregando dados de validação...")
    X_val, y_val = load_images_from_folder("dataset/val")
    
    print(f"✅ Dados carregados! Treino: {len(X_train)} | Validação: {len(X_val)}")
    
    # Definir porcentagens de dados a usar para treinamento
    train_sizes = np.linspace(0.1, 1.0, 10)  # De 10% até 100% dos dados
    train_scores = []
    val_scores = []
    
    print("\n🔄 Testando SVM com diferentes quantidades de dados...")
    
    for i, train_size in enumerate(train_sizes):
        # Usar apenas uma porcentagem dos dados de treino
        n_samples = int(len(X_train) * train_size)
        X_train_subset = X_train[:n_samples]
        y_train_subset = y_train[:n_samples]
        
        # Treinar o modelo
        clf = svm.SVC(kernel='linear', C=1.0)
        clf.fit(X_train_subset, y_train_subset)
        
        # Avaliar no conjunto de treinamento e validação
        train_score = clf.score(X_train_subset, y_train_subset)
        val_score = clf.score(X_val, y_val)
        
        train_scores.append(train_score)
        val_scores.append(val_score)
        
        percentage = int(train_size * 100)
        print(f"  {percentage:3d}% dados ({n_samples:4d} amostras) → "
              f"Train Acc: {train_score*100:.2f}% | Val Acc: {val_score*100:.2f}%")
    
    # Criar figura com a curva de aprendizado
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Converter para porcentagem para o eixo X
    train_sizes_percent = train_sizes * 100
    
    # Plotar as curvas
    ax.plot(train_sizes_percent, np.array(train_scores)*100, 
            'o-', label='Acurácia de Treinamento', linewidth=2.5, 
            markersize=8, color='#26C87A')
    ax.plot(train_sizes_percent, np.array(val_scores)*100, 
            's-', label='Acurácia de Validação', linewidth=2.5, 
            markersize=8, color='#1570EF')
    
    # Configurar o gráfico
    ax.set_xlabel('Percentual de Dados de Treinamento (%)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Acurácia (%)', fontsize=12, fontweight='bold')
    ax.set_title('📈 Curva de Aprendizado - SVM (Equivalente à Curva de Perda)', 
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11, loc='lower right')
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 105])
    ax.set_xlim([5, 105])
    
    # Adicionar anotação explicativa
    ax.text(0.5, 0.02, 
            'Nota: A curva de aprendizado mostra como o SVM melhora com mais dados.\n' +
            'Diferente de redes neurais, SVM não treina em épocas.',
            transform=ax.transAxes, fontsize=10, style='italic',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3),
            verticalalignment='bottom', horizontalalignment='center')
    
    plt.tight_layout()
    plt.savefig('curva_aprendizado_svm.png', dpi=300, bbox_inches='tight')
    print(f"\n✅ Curva de aprendizado salva: 'curva_aprendizado_svm.png'")
    
    # Estatísticas
    print("\n" + "="*60)
    print("📊 ANÁLISE DA CURVA DE APRENDIZADO DO SVM")
    print("="*60)
    print(f"Melhor Acurácia de Validação: {max(val_scores)*100:.2f}%")
    print(f"Acurácia Final (100% dos dados): {val_scores[-1]*100:.2f}%")
    print(f"Diferença Train-Val (overfitting): {(train_scores[-1] - val_scores[-1])*100:.2f}%")
    print("="*60 + "\n")
    
    plt.show()

if __name__ == "__main__":
    print("🔄 Gerando curva de aprendizado do SVM...")
    plot_learning_curve()
