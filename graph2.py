# 1. Préparation des données
df = pd.read_csv('data_v3.csv')
df['total_posts'] = df['photos_posted'] + df['videos_posted']

# Calcul des totaux par genre
stats = df.groupby('gender')[['total_posts', 'likes', 'shares', 'comments_written']].sum().reindex(['H', 'F', 'AUTRE'])

# 2. Création du graphique
plt.figure(figsize=(12, 7))

# On définit les indices
indices = range(len(stats.index))
larg = 0.2  # Largeur des barres

# Calcul des positions des batons
pos1 = [x - 1.5*larg for x in indices]
pos2 = [x - 0.5*larg for x in indices]
pos3 = [x + 0.5*larg for x in indices]
pos4 = [x + 1.5*larg for x in indices]

# Tracé des barres
b1 = plt.bar(pos1, stats['total_posts'], larg, label='Total Posts', color='b')
b2 = plt.bar(pos2, stats['likes'], larg, label='Total Likes', color='r')
b3 = plt.bar(pos3, stats['shares'], larg, label='Total Partages', color='g')
b4 = plt.bar(pos4, stats['comments_written'], larg, label='Total Commentaires', color='m')

# Ajout des valeurs sur les bâtons
plt.bar_label(b1, padding=3, fontsize=9)
plt.bar_label(b2, padding=3, fontsize=9)
plt.bar_label(b3, padding=3, fontsize=9)
plt.bar_label(b4, padding=3, fontsize=9)

# Configuration
plt.xticks(indices, stats.index)
plt.ylabel('Nombre Total')
plt.title('Volume total des actions effectuées par genre')
plt.legend()
plt.grid(axis='y', linestyle='--')

# Espace pour les étiquettes
plt.ylim(0, stats['likes'].max()*1.2)

plt.show()