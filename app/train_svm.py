import os
import cv2
import numpy as np
import pandas as pd
from sklearn import svm, metrics
import matplotlib.pyplot as plt
import joblib
import time

def load_images_from_folder(base_folder, img_size=(64, 64)):
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
                
    return np.array(X), np.array(y), classes

def find_next_run_folder(base_path="runs/svm"):
    """Encontra o próximo número de treinamento (train, train2, train3, etc.)"""
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        return os.path.join(base_path, "train")
    
    counter = 1
    while True:
        run_name = "train" if counter == 1 else f"train{counter}"
        run_path = os.path.join(base_path, run_name)
        if not os.path.exists(run_path):
            return run_path
        counter += 1

def main():
    # ===== CRIAR ESTRUTURA DE PASTAS =====
    run_folder = find_next_run_folder()
    os.makedirs(run_folder, exist_ok=True)
    
    print(f"📁 Pasta de treinamento criada: {run_folder}/")
    print("="*60)
    
    # ===== CARREGAR DADOS =====
    print("\n⏳ Carregando imagens de treinamento...")
    X_train, y_train, classes = load_images_from_folder("dataset/train")
    
    print("⏳ Carregando imagens de validação...")
    X_val, y_val, _ = load_images_from_folder("dataset/val")

    print(f"✅ Dados carregados!")
    print(f"   Treinamento: {len(X_train)} amostras")
    print(f"   Validação: {len(X_val)} amostras")
    print(f"   Classes: {len(classes)}")
    
    # ===== TREINAR MODELO =====
    print("\n🧠 Treinando o modelo SVM (isso pode demorar)...")
    start_time = time.time()
    
    clf = svm.SVC(kernel='linear', C=1.0)
    clf.fit(X_train, y_train)
    
    training_time = time.time() - start_time
    print(f"✅ Treinamento concluído em {training_time:.2f} segundos ({training_time/60:.2f} minutos)")
    
    # ===== SALVAR MODELO =====
    model_path = os.path.join(run_folder, "modelo_svm.pkl")
    joblib.dump(clf, model_path)
    print(f"💾 Modelo salvo em: {model_path}")
    
    # ===== FAZER PREDIÇÕES =====
    print("\n📊 Avaliando o modelo...")
    y_pred = clf.predict(X_val)
    
    # ===== CALCULAR MÉTRICAS =====
    accuracy = metrics.accuracy_score(y_val, y_pred)
    report_dict = metrics.classification_report(y_val, y_pred, output_dict=True)
    
    # ===== SALVAR RESULTADOS EM CSV (similar ao YOLO) =====
    results_csv = os.path.join(run_folder, "results.csv")
    results_data = {
        'metric': [
            'accuracy',
            'macro_avg_precision',
            'macro_avg_recall',
            'macro_avg_f1',
            'weighted_avg_precision',
            'weighted_avg_recall',
            'weighted_avg_f1',
            'training_time_seconds'
        ],
        'value': [
            accuracy * 100,
            report_dict['macro avg']['precision'] * 100,
            report_dict['macro avg']['recall'] * 100,
            report_dict['macro avg']['f1-score'] * 100,
            report_dict['weighted avg']['precision'] * 100,
            report_dict['weighted avg']['recall'] * 100,
            report_dict['weighted avg']['f1-score'] * 100,
            training_time
        ]
    }
    
    df_results = pd.DataFrame(results_data)
    df_results.to_csv(results_csv, index=False)
    print(f"📄 Resultados salvos em: {results_csv}")
    
    # ===== RELATÓRIO DETALHADO =====
    print("\n" + "="*60)
    print("📊 MÉTRICAS DE DESEMPENHO - SVM")
    print("="*60)
    print(f"\n🎯 Acurácia Geral: {accuracy*100:.2f}%\n")
    
    print("📋 Relatório Detalhado por Classe:")
    print("-" * 60)
    report_text = metrics.classification_report(y_val, y_pred, digits=4)
    print(report_text)
    
    # Salvar relatório em arquivo texto
    report_path = os.path.join(run_folder, "classification_report.txt")
    with open(report_path, 'w') as f:
        f.write("RELATÓRIO DE CLASSIFICAÇÃO - SVM\n")
        f.write("="*60 + "\n\n")
        f.write(f"Acurácia Geral: {accuracy*100:.2f}%\n\n")
        f.write(report_text)
    print(f"📄 Relatório salvo em: {report_path}")
    
    print("="*60 + "\n")
    
    print("📈 MÉTRICAS AGREGADAS:")
    print("="*60)
    print(f"Accuracy: {report_dict['accuracy']*100:.2f}%")
    print(f"Macro Avg (Precision): {report_dict['macro avg']['precision']*100:.2f}%")
    print(f"Macro Avg (Recall): {report_dict['macro avg']['recall']*100:.2f}%")
    print(f"Macro Avg (F1-Score): {report_dict['macro avg']['f1-score']*100:.2f}%")
    print(f"\nWeighted Avg (Precision): {report_dict['weighted avg']['precision']*100:.2f}%")
    print(f"Weighted Avg (Recall): {report_dict['weighted avg']['recall']*100:.2f}%")
    print(f"Weighted Avg (F1-Score): {report_dict['weighted avg']['f1-score']*100:.2f}%")
    print("="*60 + "\n")
    
    # ===== MATRIZ DE CONFUSÃO =====
    print("📸 Gerando Matriz de Confusão...")
    disp = metrics.ConfusionMatrixDisplay.from_predictions(y_val, y_pred, xticks_rotation='vertical')
    disp.figure_.suptitle("Matriz de Confusão - SVM")
    plt.tight_layout()
    
    cm_path = os.path.join(run_folder, "matriz_confusao.png")
    plt.savefig(cm_path, dpi=300, bbox_inches='tight')
    print(f"✅ Matriz de confusão salva em: {cm_path}\n")
    
    # ===== RESUMO FINAL =====
    print("="*60)
    print("📦 RESUMO DA PASTA DE TREINAMENTO")
    print("="*60)
    print(f"Localização: {run_folder}/")
    print(f"\nArquivos criados:")
    print(f"  ✅ modelo_svm.pkl - Modelo treinado (reutilizável)")
    print(f"  ✅ results.csv - Resultados em formato CSV")
    print(f"  ✅ classification_report.txt - Relatório detalhado")
    print(f"  ✅ matriz_confusao.png - Gráfico da matriz de confusão")
    print(f"\nMétrica Principal: {accuracy*100:.2f}% de acurácia")
    print(f"Tempo de Treinamento: {training_time:.2f}s ({training_time/60:.2f} min)")
    print("="*60 + "\n")
    
    return accuracy

if __name__ == "__main__":
    acc_svm = main()
    print(f"✅ ACURÁCIA SVM OBTIDA: {acc_svm*100:.2f}%")
    print("Use este valor em comparacao_grafica_melhorada.py")
