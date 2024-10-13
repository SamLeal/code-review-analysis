import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import spearmanr, pearsonr

# Carregar os dados do CSV
prs_df = pd.read_csv('prs_infos_oficial.csv')

# Converter colunas para tipos numéricos (float)
cols_to_convert = ['Total de Arquivos Alterados', 'Decisão da Revisão', 
                   'Tempo de Análise (horas)', 'Total de Revisões', 'Total de Comentários']

prs_df[cols_to_convert] = prs_df[cols_to_convert].apply(pd.to_numeric, errors='coerce')

# Função para calcular correlação e exibir gráfico
def plot_and_correlate(x, y, method='spearman'):
    plt.figure(figsize=(8, 6))
    
    # Gráfico de dispersão com linha de regressão
    sns.regplot(x=x, y=y, data=prs_df, scatter_kws={'s': 10}, line_kws={"color": "red"})
    
    plt.title(f'Correlação entre {x} e {y}')
    plt.xlabel(x)
    plt.ylabel(y)
    
    # Verificação do método de correlação
    if method == 'spearman':
        corr, p_value = spearmanr(prs_df[x], prs_df[y], nan_policy='omit')
        plt.text(0.05, 0.95, f'Spearman Corr: {corr:.3f}, p-value: {p_value:.3g}', transform=plt.gca().transAxes)
    elif method == 'pearson':
        corr, p_value = pearsonr(prs_df[x], prs_df[y])
        plt.text(0.05, 0.95, f'Pearson Corr: {corr:.3f}, p-value: {p_value:.3g}', transform=plt.gca().transAxes)
    
    plt.tight_layout()
    plt.show()

# RQ05: Relação entre o tamanho dos PRs e o número de revisões
plot_and_correlate('Total de Arquivos Alterados', 'Total de Revisões', method='pearson')

# RQ06: Relação entre o tempo de análise e o número de revisões
plot_and_correlate('Tempo de Análise (horas)', 'Total de Revisões', method='pearson')

# RQ07: Qual a relação entre a descrição dos PRs e o número de revisões realizadas?
plot_and_correlate('Comprimento da Descrição', 'Total de Revisões', method='pearson')

# RQ08: Relação entre as interações e o número de revisões
plot_and_correlate('Total de Comentários', 'Total de Revisões', method='pearson')
