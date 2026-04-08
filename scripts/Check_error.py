import pandas as pd 
df=pd.read_csv('data/export_01-03-2026_au_31-03-2026.csv',sep=";")
radios = {"France Inter", "franceinfo", "France Culture"}

def main():
    df_verif = df['Historique des modifications']
    df_verif = df_verif.dropna()
    count_NameError =  df_verif.str.contains(r"\[AD\] Nom de l'invité").sum()
    count_CategoryError = df_verif.str.contains(r"\[AD\] Catégorie").sum()
    print(f" Taille du DataFrame :  {len(df)}")
    print("-"*40)
    print(f" Nombre total d'erreurs corrigés : {len(df_verif)}")
    print(f" Nombre d'erreurs nom des invité.e.s : {count_NameError}")
    print(f" Nombre d'erreurs dans les catégories des invité.e.s : {count_CategoryError}")

def unique():
    df_unique = df.drop_duplicates(subset="Invités")
    counts_NameErrorUnique = df_unique['Historique des modifications'].str.contains(r"\[AD\] Nom de l'invité",na=False).sum()
    counts_CategoryErrorUnique = df_unique['Historique des modifications'].str.contains(r"\[AD\] Catégorie", na=False).sum()
    print(f" Nombre d'erreurs dans les  nom des invité.e.s unique : {counts_NameErrorUnique}")
    print(f" Nombre d'erreurs dans les catégories des invité.e.s unique : {counts_CategoryErrorUnique}")

def Radios ():
    for radio in radios :
        df_radio = df[df['Station'] == radio] 
        nb_invité = len(df_radio['Invités'])
        radio_error = df_radio['Historique des modifications'].notna().sum()
        count_NameError_radio = df_radio['Historique des modifications'].str.contains(r"\[AD\] Nom de l'invité", na=False).sum()
        count_categoryError_radio = df_radio['Historique des modifications'].str.contains(r"\[AD\] Catégorie", na=False).sum()
        print(f" Radio : {radio}")
        print(f" Nombre d'invité.e.s : {nb_invité}")
        print(f" Nombre d'erreur corrigé : {radio_error}")
        print(f" Nombre d'erreurs dans les noms des invité.e.s : {count_NameError_radio}")
        print(f" Nombre d'erreurs catégorie des invité.e.s  : {count_categoryError_radio}")
        print("-"*40)
if __name__ == "__main__":
    main()
    print("-"*40)
    unique()
    print("-"*40)
    Radios()
