import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar os dados do CSV
df = pd.read_csv('./prs_infos_paginated.csv')

# Gráfico 1: Relação entre o tamanho do PR (adições + remoções) e o feedback final (MERGED ou CLOSED)
df['Total Alterações'] = df['Total de Adições'] + df['Total de Remoções']
plt.figure(figsize=(10, 6))
sns.boxplot(x='Decisão da Revisão', y='Total Alterações', data=df)
plt.title('Relação entre Tamanho do PR e Feedback Final')
plt.show()

# Gráfico 2: Relação entre o tempo de análise e o feedback final
plt.figure(figsize=(10, 6))
sns.boxplot(x='Decisão da Revisão', y='Tempo de Análise (horas)', data=df)
plt.title('Relação entre Tempo de Análise e Feedback Final')
plt.show()

# Gráfico 3: Relação entre o comprimento da descrição do PR e o feedback final
plt.figure(figsize=(10, 6))
sns.boxplot(x='Decisão da Revisão', y='Comprimento da Descrição', data=df)
plt.title('Relação entre Descrição do PR e Feedback Final')
plt.show()

# Gráfico 4: Relação entre o número de interações (comentários e participantes) e o feedback final
df['Total Interações'] = df['Total de Comentários'] + df['Total de Participantes']
plt.figure(figsize=(10, 6))
sns.boxplot(x='Decisão da Revisão', y='Total Interações', data=df)
plt.title('Relação entre Interações no PR e Feedback Final')
plt.show()
