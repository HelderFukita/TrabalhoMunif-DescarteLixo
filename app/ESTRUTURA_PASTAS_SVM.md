# 📁 Estrutura de Pastas do SVM

Agora o SVM cria uma **estrutura de pastas idêntica ao YOLO**!

## Antes vs Depois

### ❌ Antes (Salvava tudo na raiz):
```
app/
├── train_svm.py
├── matriz_confusao_svm.png
├── comparacao_modelos.png
└── outros arquivos soltos...
```

### ✅ Depois (Organizado em pastas):
```
app/
├── runs/
│   ├── svm/
│   │   ├── train/
│   │   │   ├── modelo_svm.pkl          ← Modelo treinado
│   │   │   ├── results.csv             ← Métricas em CSV
│   │   │   ├── classification_report.txt ← Relatório completo
│   │   │   └── matriz_confusao.png     ← Gráfico
│   │   ├── train2/                     ← Se rodar novamente
│   │   ├── train3/
│   │   └── ... (próximos treinamentos)
│   └── classify/
│       ├── train/                      ← Pastas do YOLO
│       ├── train3/
│       └── ...
```

## Como Funciona

### Primeira execução:
```bash
python train_svm.py
```
→ Cria: `runs/svm/train/`

### Segunda execução:
```bash
python train_svm.py
```
→ Cria: `runs/svm/train2/` (automaticamente)

### Terceira execução:
```bash
python train_svm.py
```
→ Cria: `runs/svm/train3/` (e assim por diante)

## Arquivos Salvos em Cada Pasta

| Arquivo | Função |
|---------|--------|
| **modelo_svm.pkl** | Modelo SVM treinado (pode ser reutilizado depois) |
| **results.csv** | Resumo das métricas em formato CSV (similar ao YOLO) |
| **classification_report.txt** | Relatório detalhado completo (precision, recall, F1, etc) |
| **matriz_confusao.png** | Gráfico da matriz de confusão em alta qualidade |

## Comparando com YOLO

### YOLO (`runs/classify/train/`):
```
results.csv com colunas:
- epoch
- train/loss
- val/loss
- metrics/accuracy_top1
- metrics/accuracy_top5
```

### SVM (`runs/svm/train/`):
```
results.csv com colunas:
- metric (nome da métrica)
- value (valor numérico)

Exemplos:
- accuracy: 88.76%
- macro_avg_f1: 85.34%
- training_time_seconds: 245.67
```

## Vantagens

✅ **Organização**: Cada treinamento em sua própria pasta  
✅ **Histórico**: Mantém todos os treinamentos anteriores  
✅ **Reproducibilidade**: Salva modelo para reutilização  
✅ **Consistência**: Mesma estrutura que o YOLO  
✅ **Fácil análise**: Resultados em CSV para comparação  

## Próximas Etapas

Agora você pode:

1. **Comparar históricos de treinamento:**
   ```bash
   # Verificar runs/svm/train/results.csv
   # Verificar runs/svm/train2/results.csv
   # Etc.
   ```

2. **Reutilizar o modelo treinado:**
   ```python
   import joblib
   clf = joblib.load('runs/svm/train/modelo_svm.pkl')
   predictions = clf.predict(new_data)
   ```

3. **Gerar gráficos comparativos** entre os treinamentos

---

**Agora SVM e YOLO seguem a mesma filosofia de organização! 🎉**
