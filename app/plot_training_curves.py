"""
Script para visualizar as curvas de perda e acurácia do YOLO durante o treinamento
Extrai dados de runs/classify/train/results.csv e gera gráficos
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_training_curves():
    """Plota as curvas de perda (loss) e acurácia durante o treinamento do YOLO"""
    
    # Caminho do arquivo CSV com os resultados
    csv_path = "runs/classify/train/results.csv"
    
    if not os.path.exists(csv_path):
        print(f"❌ Arquivo não encontrado: {csv_path}")
        print("Execute train.py primeiro para gerar os resultados!")
        return
    
    # Carregar dados
    df = pd.read_csv(csv_path)
    
    # Criar figura com 4 subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Análise de Treinamento - YOLOv8', fontsize=16, fontweight='bold')
    
    # ===== GRÁFICO 1: Curva de Perda (Loss) =====
    ax1 = axes[0, 0]
    ax1.plot(df['epoch'], df['train/loss'], label='Train Loss', marker='o', linewidth=2, color='#1570EF')
    ax1.plot(df['epoch'], df['val/loss'], label='Val Loss', marker='s', linewidth=2, color='#FF6B6B')
    ax1.set_xlabel('Época', fontweight='bold')
    ax1.set_ylabel('Loss', fontweight='bold')
    ax1.set_title('📉 Curva de Perda (Loss)', fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # ===== GRÁFICO 2: Acurácia Top-1 =====
    ax2 = axes[0, 1]
    ax2.plot(df['epoch'], df['metrics/accuracy_top1'], label='Train Accuracy', marker='o', linewidth=2, color='#26C87A')
    ax2.set_xlabel('Época', fontweight='bold')
    ax2.set_ylabel('Acurácia (%)', fontweight='bold')
    ax2.set_title('✅ Acurácia Top-1', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim([0.7, 1.0])
    
    # ===== GRÁFICO 3: Acurácia Top-5 =====
    ax3 = axes[1, 0]
    ax3.plot(df['epoch'], df['metrics/accuracy_top5'], marker='o', linewidth=2, color='#FFB52E')
    ax3.set_xlabel('Época', fontweight='bold')
    ax3.set_ylabel('Acurácia (%)', fontweight='bold')
    ax3.set_title('⭐ Acurácia Top-5', fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim([0.95, 1.0])
    
    # ===== GRÁFICO 4: Taxa de Aprendizado =====
    ax4 = axes[1, 1]
    ax4.plot(df['epoch'], df['lr/pg0'], marker='o', linewidth=2, color='#8B5CF6')
    ax4.set_xlabel('Época', fontweight='bold')
    ax4.set_ylabel('Learning Rate', fontweight='bold')
    ax4.set_title('🎛️ Taxa de Aprendizado (Learning Rate)', fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Salvar figura
    output_path = "analise_treinamento_yolo.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico salvo: {output_path}")
    
    # Exibir estatísticas finais
    print("\n" + "="*60)
    print("📊 ESTATÍSTICAS FINAIS DE TREINAMENTO (YOLO)")
    print("="*60)
    last_row = df.iloc[-1]
    print(f"Epochs: {int(df['epoch'].max())}")
    print(f"Train Loss Final: {last_row['train/loss']:.4f}")
    print(f"Val Loss Final: {last_row['val/loss']:.4f}")
    print(f"Accuracy Top-1 Final: {last_row['metrics/accuracy_top1']*100:.2f}%")
    print(f"Accuracy Top-5 Final: {last_row['metrics/accuracy_top5']*100:.2f}%")
    print(f"Tempo Total de Treinamento: {last_row['time']:.1f} segundos ({last_row['time']/60:.1f} min)")
    print("="*60 + "\n")
    
    plt.show()

if __name__ == "__main__":
    print("🔄 Gerando gráficos de curvas de treinamento...")
    plot_training_curves()
