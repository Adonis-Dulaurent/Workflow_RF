import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
from jiwer import process_words
import re 

def clean_text(text) :
    """
    Nettoie le texte pour éviter les erreurs de ponctuation ou de case. 
    comportement : 
        - Supprime la ponctuation
        - remet les lettres en majuscules en minuscules 
    retour : 
        texte nettoyé 
    Dépendances: 
        - re 
    """
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

errors = []

df_raw = pd.read_csv('data/raw_2026_03_16_2026_03_22.csv', sep=";")
df_true = pd.read_csv('data/Groud_Truth_16_03_2026_22_03_2026.csv', sep=";")

col_raw='Invités'
col_true='Invités'

for v, w in zip(df_true[col_true], df_raw[col_raw]):
    v_clean = clean_text(v)
    w_clean = clean_text(w)

    if v_clean and w_clean:
        res = process_words(v_clean, w_clean)
        ref_sentence = res.references[0]
        hyp_sentence = res.hypotheses[0]
        
        for alignment in res.alignments[0]:
            if alignment.type == "substitute":
                ref_word = ref_sentence[alignment.ref_start_idx]
                hyp_word = hyp_sentence[alignment.hyp_start_idx]
                errors.append((ref_word, hyp_word))

df_errors = pd.DataFrame(errors, columns=['Vérité','IA'])

top_errors = df_errors.value_counts().nlargest(20).reset_index(name='frequence')
matrix_data = top_errors.pivot(index='Vérité', columns='IA', values='frequence').fillna(0)

plt.figure(figsize=(14, 10))
sns.heatmap(matrix_data, annot=True, fmt='g', cmap="YlOrRd", cbar=True)
plt.title("Matrice de Confusion : Mots substitués par Whisper (Top 20)")
plt.xlabel("Ce que Whisper a écrit")
plt.ylabel("Ce qui était vraiment dit")
plt.xticks(rotation=45)
plt.savefig('matrice_confusion_nom.png', dpi=300, bbox_inches='tight')
