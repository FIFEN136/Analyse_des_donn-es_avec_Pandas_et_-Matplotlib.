# Charger le fichier Excel
df = pd.read_excel('Sujet6.xlsx')

# 1) Nettoyage colonnes de données textuelles
text_columns = ['gender', 'subscription', 'region', 'device_type']
text_columns = [c for c in text_columns if c in df.columns]

for col in text_columns:
    # Normaliser en chaîne de char
    df[col] = df[col].astype(str)
    # Supprimer # et ? puis garder uniquement lettres et espaces
    df[col] = df[col].str.replace('[#?]', '', regex=True)
    df[col] = df[col].str.replace('[^A-Za-zÀ-ÖØ-öø-ÿ\\s]', '', regex=True)
    df[col] = df[col].str.strip()
    df[col] = df[col].str.replace('\\s+', ' ', regex=True)
    # Convertir en majuscule et enlever accents
    df[col] = df[col].str.normalize('NFKD').str.encode('ascii', 'ignore').str.decode('ascii')
    df[col] = df[col].str.upper()

# Supprimer lignes textuelles vides ou manquantes
if text_columns:
    df = df.dropna(subset=text_columns)
    for col in text_columns:
        df = df[df[col].str.len() > 0]

# 2) Nettoyage colonne de données numériques
decimal_columns = ['time_on_plateforme', 'avg_session_duration', 'geo_lat', 'geo_lon', 'engagement_score', 'churn_risk']
numeric_columns = [c for c in df.columns if c not in text_columns]

for col in numeric_columns:
    # Nettoyage initial des valeurs textuelles
    df[col] = df[col].astype(str).fillna('')
    df[col] = df[col].str.replace('[#?]', '', regex=True)
    # Extrait le premier nombre dans la chaîne (ex: '522abc' -> 522)
    df[col] = df[col].str.extract('(-?[0-9]+(?:\\.[0-9]+)?)', expand=False)
    # Conversion numérique
    df[col] = pd.to_numeric(df[col], errors='coerce')
    # Pas de nb négatifs
    df[col] = df[col].abs()
    # Découper en int sauf colonnes décimales autorisées
    if col not in decimal_columns:
        df[col] = df[col].apply(lambda x: int(x) if pd.notna(x) else x)

# Supprimer les lignes avec valeurs non numériques
if numeric_columns:
    df = df.dropna(subset=numeric_columns)

# 3) Nettoyage global
# Supprimer lignes complètement vides
df = df.dropna(how='all')
# Supprimer lignes avec >50% de valeurs manquantes
df = df.dropna(thresh=int(len(df.columns)*0.5))
# Supprimer doublons
df = df.drop_duplicates()

# Sauvegarder le fichier nettoyé
df.to_csv('data_v3.csv', index=False)
print("\n✓ Données nettoyées")
