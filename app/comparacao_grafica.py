"""
Comparação gráfica melhorada entre YOLO e SVM
Extrai métricas do YOLO (results.csv) e SVM para visualização completa
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def extract_yolo_metrics():
    """Extrai métricas finais do YOLO de results.csv"""
    csv_path = "runs/classify/train/results.csv"
    
    if not os.path.exists(csv_path):
        print(f"❌ Arquivo não encontrado: {csv_path}")
        return None
    
    df = pd.read_csv(csv_path)
    last_row = df.iloc[-1]
    
    return {
        'accuracy': last_row['metrics/accuracy_top1'],
        'loss': last_row['val/loss'],
        'epochs': int(df['epoch'].max()),
        'training_time': last_row['time']
    }

def plot_comparison():
    """Cria gráficos de comparação entre YOLO e SVM"""
    
    # Extrair métricas do YOLO
    yolo_metrics = extract_yolo_metrics()
    
    if yolo_metrics is None:
        print("Execute train.py primeiro!")
        return
    
    # IMPORTANTE: Substituir pelos valores reais do SVM
    # Execute train_svm_melhorado.py para obter esses valores
    SVM_ACCURACY = 0.2590  # ⚠️ SUBSTITUA PELO VALOR REAL!
    SVM_TRAINING_TIME = 334.61  # ⚠️ SUBSTITUA PELO VALOR REAL (em segundos)
    
    yolo_accuracy = yolo_metrics['accuracy']
    yolo_training_time = yolo_metrics['training_time']
    yolo_loss = yolo_metrics['loss']
    
    # Criar figura com múltiplos gráficos
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle('Comparação de Desempenho: YOLOv8 vs SVM', fontsize=16, fontweight='bold')
    
    # ===== GRÁFICO 1: Acurácia =====
    ax1 = axes[0]
    modelos = ['YOLOv8\n(Deep Learning)', 'SVM\n(Machine Learning)']
    acuracias = [yolo_accuracy * 100, SVM_ACCURACY * 100]
    bars1 = ax1.bar(modelos, acuracias, color=['#26C87A', '#1570EF'], width=0.6, edgecolor='black', linewidth=2)
    ax1.set_ylabel('Acurácia (%)', fontsize=12, fontweight='bold')
    ax1.set_title('🎯 Comparação de Acurácia', fontsize=13, fontweight='bold')
    ax1.set_ylim(0, 110)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
    # Adicionar valores em cima das barras
    for bar in bars1:
        height = bar.get_height()
        ax1.annotate(f'{height:.2f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # ===== GRÁFICO 2: Tempo de Treinamento =====
    ax2 = axes[1]
    tempos = [yolo_training_time, SVM_TRAINING_TIME]
    bars2 = ax2.bar(modelos, tempos, color=['#FFB52E', '#8B5CF6'], width=0.6, edgecolor='black', linewidth=2)
    ax2.set_ylabel('Tempo (segundos)', fontsize=12, fontweight='bold')
    ax2.set_title('⏱️ Tempo de Treinamento', fontsize=13, fontweight='bold')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    
    # Converter para minutos se > 60s
    for i, (bar, tempo) in enumerate(zip(bars2, tempos)):
        if tempo > 60:
            label = f'{tempo/60:.1f} min'
        else:
            label = f'{tempo:.0f}s'
        ax2.annotate(label,
                    xy=(bar.get_x() + bar.get_width() / 2, tempo),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # ===== GRÁFICO 3: Perda Final (Loss) =====
    ax3 = axes[2]
    ax3.text(0.5, 0.7, 'YOLOv8', ha='center', fontsize=14, fontweight='bold')
    ax3.text(0.5, 0.55, f'Loss Final: {yolo_loss:.4f}', ha='center', fontsize=12, 
             bbox=dict(boxstyle='round', facecolor='#26C87A', alpha=0.3))
    ax3.text(0.5, 0.35, f'Epochs: {yolo_metrics["epochs"]}', ha='center', fontsize=11)
    ax3.text(0.5, 0.15, 'Nota: SVM não usa loss similar', ha='center', fontsize=10, style='italic', color='gray')
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    ax3.axis('off')
    ax3.set_title('📊 Métricas do YOLO', fontsize=13, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('comparacao_modelos_completa.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfico de comparação salvo: 'comparacao_modelos_completa.png'")
    
    # Exibir resumo
    print("\n" + "="*60)
    print("📊 RESUMO COMPARATIVO")
    print("="*60)
    print(f"YOLOv8 - Acurácia: {yolo_accuracy*100:.2f}% | Tempo: {yolo_training_time:.1f}s")
    print(f"SVM    - Acurácia: {SVM_ACCURACY*100:.2f}% | Tempo: {SVM_TRAINING_TIME:.1f}s")
    print("="*60 + "\n")
    
    plt.show()

if __name__ == "__main__":
    print("🔄 Gerando gráfico de comparação...")
    plot_comparison()
