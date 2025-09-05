# Importação das bibliotecas necessárias
import matplotlib.pyplot as plt   # Para criação dos gráficos
import pandas as pd              # Para manipulação de dados (DataFrame)
import seaborn as sns            # Biblioteca para gráficos estatísticos
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters() # Garante compatibilidade ao trabalhar com datas no Pandas + Matplotlib

# Importa os dados do arquivo CSV
# - parse_dates: converte a coluna 'date' para tipo datetime
# - index_col: define 'date' como índice do DataFrame
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Limpeza dos dados
# Remove outliers, mantendo apenas os valores entre os percentis 2.5% e 97.5%
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    """Cria um gráfico de linha com a evolução das visualizações diárias do fórum."""

    # Cria a figura e o eixo com tamanho 15x5
    fig, ax = plt.subplots(figsize=(15,5))  

    # Plota os valores de page views ao longo do tempo
    ax.plot(df.index, df['value'], color='green', linewidth=1) 

    # Define título e rótulos dos eixos
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Salva a imagem em arquivo
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    """Cria um gráfico de barras mostrando a média mensal de visualizações por ano."""

    # Cria cópia do DataFrame e adiciona colunas de ano e mês
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # Agrupa por ano e mês e calcula a média das visualizações
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Cria a figura e eixo para o gráfico
    fig, ax = plt.subplots(figsize=(10,7))

    # Plota gráfico de barras (cada ano no eixo X e os meses como barras empilhadas lado a lado)
    df_bar.plot(kind='bar', ax=ax)

    # Ajusta rótulos e título
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')  
    ax.set_title('Views per Month')

    # Define a legenda com nomes dos meses
    ax.legend(
        title='Months', 
        labels=['January', 'February', 'March', 'April', 'May', 'June', 
                'July', 'August', 'September', 'October', 'November', 'December']
    )

    # Ajusta o layout para evitar sobreposição de textos
    plt.tight_layout()

    # Salva a imagem
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    """Cria dois gráficos de caixa (boxplot):
       1. Distribuição das visualizações por ano (tendência ao longo do tempo).
       2. Distribuição das visualizações por mês (sazonalidade).
    """

    # Prepara os dados
    df_box = df.copy()
    df_box.reset_index(inplace=True)  # Tira 'date' do índice e transforma em coluna
    df_box['year'] = [d.year for d in df_box.date]       # Extrai ano
    df_box['month'] = [d.strftime('%b') for d in df_box.date]  # Extrai mês abreviado (Jan, Feb, ...)

    # Cria figura com 2 gráficos lado a lado
    fig, axes = plt.subplots(1, 2, figsize=(15,6)) 

    # Boxplot por ano (mostra variação de page views a cada ano)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Define ordem correta dos meses para o segundo gráfico
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Boxplot por mês (mostra sazonalidade das page views ao longo do ano)
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=month_order)
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Salva a imagem
    fig.savefig('box_plot.png')
    return fig
