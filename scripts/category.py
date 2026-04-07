import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
from sklearn.metrics import confusion_matrix, classification_report 

df_raw = pd.read_csv('data/raw_2026_03_16_2026_03_22.csv',sep=";")
df_GT = pd.read_csv('data/Groud_Truth_16_03_2026_22_03_2026.csv',sep=";")

y_raw = df_raw["Catégorie d'invités"]
y_true = df_GT["Catégorie d'invités"]

labels = sorted(y_true.unique())
cm = confusion_matrix(y_true, y_raw)

plt.figure(figsize=(10, 7))
sns.heatmap(cm, annot=True, fmt='d', xticklabels=labels, yticklabels=labels, cmap='Blues')
plt.xlabel('Prédiction du modèle')
plt.ylabel('Réalité de terrain')
plt.title('Matrice de Confusion')
plt.savefig('matrice_confusion_whisper.png', dpi=300, bbox_inches='tight')

# 5. Afficher les métriques détaillées (Précision, Rappel, F1-score)
print(classification_report(y_true, y_raw))
