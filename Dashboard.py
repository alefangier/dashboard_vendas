import streamlit as st
# import requests
import pandas as pd
import plotly.express as px

def formata_numero(valor, prefixo = ''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões'

st.set_page_config(layout='wide')

st.title('DASHBOARD DE VENDAS :shopping_trolley:')

# url = 'https://labdados.com/produtos'
# response = requests.get(url)
# dados = pd.DataFrame.from_dict(response.json())
# Criando o DataFrame a partir dos dados fornecidos


data = {
    'Produto': ['Modelagem preditiva', 'Iniciando em programação', 'Pandeiro', 'Corda de pular',
                'Dinossauro Rex', 'Jogo de copos', 'Lavadora de roupas', 'Bola de vôlei',
                'Xadrez de madeira', 'Xadrez de madeira'],
    'Categoria do Produto': ['livros', 'livros', 'instrumentos musicais', 'esporte e lazer',
                             'brinquedos', 'utilidades domésticas', 'eletrodomésticos',
                             'esporte e lazer', 'brinquedos', 'brinquedos'],
    'Preço': [92.45, 43.84, 87.18, 13.65, 28.32, 54.67, 1920.01, 56.26, 25.87, 25.23],
    'Frete': [5.6097, 0, 2.2265, 1.2579, 2.0391, 9.2906, 99.8192, 0, 1.9086, 0],
    'Data da Compra': ['01/01/2020', '01/01/2020', '01/01/2020', '01/01/2020', '01/01/2020',
                       '01/01/2020', '01/01/2020', '01/01/2020', '01/01/2020', '01/01/2021'],
    'Vendedor': ['Thiago Silva', 'Mariana Ferrei', 'Thiago Silva', 'Camila Ribeiro',
                 'Juliana Costa', 'Camila Ribeiro', 'Juliana Costa', 'Mariana Ferrei',
                 'Juliana Costa', 'Thiago Silva'],
    'Local de compra': ['BA', 'SP', 'RJ', 'RJ', 'RJ', 'SP', 'ES', 'MG', 'SP', 'BA'],
    'Avaliação da compra': [1, 5, 4, 4, 1, 4, 5, 3, 5, 5],
    "Tipo de pagamento": [
        "cartao_credito", "cartao_credito", "cartao_credito", "boleto",
        "cartao_debito", "boleto", "cartao_credito", "cartao_credito",
        "boleto", "cartao_credito"],
    "Quantidade de parcelas": [3, 1, 4, 1, 1, 1, 1, 4, 1, 2],
    "lat": [-13.29, -22.19, 22.25, -22.25, -22.25, -22.19, -19.19, -18.1, -22.19, -13.29],
    "lon": [-41.71, -48.79, -42.66, -42.66, -42.66, -48.79, -40.34, -44.38, -48.79, -41.71]
}


# Mapeamento dos estados para suas respectivas regiões
state_to_region = {
    'BA': 'Nordeste',
    'SP': 'Sudeste',
    'RJ': 'Sudeste',
    'ES': 'Sudeste',
    'MG': 'Sudeste'
}

# Cria a coluna Regiao com base em 'Local de compra'
data['Regiao'] = [state_to_region.get(estado, 'Brasil') for estado in data['Local de compra']]

regioes = ['Brasil', 'Centro_Oeste', 'Nordeste', 'Norte', 'Sul', 'Sudeste']

st.sidebar.title('Filtros')
regiao = st.sidebar.selectbox('Região', regioes)
if regiao == 'Brasil':
    regiao = regioes

todos_anos = st.sidebar.checkbox('Dados de todo o período', value=True)
if todos_anos:
    ano = ''
else:
    ano = st.sidebar.slider('Ano', 2020, 2021)

query_string = {'regiao':regiao, 'ano':ano}

df = pd.DataFrame(data)
df['Data da Compra'] = pd.to_datetime(df['Data da Compra'], format='%d/%m/%Y')

# Primeiro filtro com query
df_filtrado = df.query('Regiao == @regiao or @regiao == ""')

# Depois aplica o filtro de string com .str.contains
if ano != "":
    df_filtrado = df_filtrado[df_filtrado['Data da Compra'].dt.year == int(ano)]


filtro_vendedores = st.sidebar.multiselect('Vendedores',df_filtrado['Vendedor'].unique())
if filtro_vendedores:
    df_filtrado = df_filtrado.query('Vendedor in @filtro_vendedores')


## Tabelas

### Receita
receitas_estados = df_filtrado.groupby('Local de compra')[['Preço']].sum()
receitas_estados = df_filtrado.drop_duplicates(subset=['Local de compra'])[['Local de compra', 'lat', 'lon']].merge(
    receitas_estados, left_on='Local de compra', right_index=True).sort_values('Preço', ascending=False)

receita_mensal = df_filtrado.set_index('Data da Compra').resample('M')[['Preço']].sum().reset_index()
receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
receita_mensal['Mes'] = receita_mensal['Data da Compra'].dt.month_name()

receita_categorias = df_filtrado.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço', ascending=False)

### Quantidade de vendas
vendas_estados = pd.DataFrame(df_filtrado.groupby('Local de compra')['Preço'].count())
vendas_estados = df_filtrado.drop_duplicates(subset = 'Local de compra')[['Local de compra','lat', 'lon']].merge(vendas_estados, left_on = 'Local de compra', right_index = True).sort_values('Preço', ascending = False)

vendas_mensal = pd.DataFrame(df_filtrado.set_index('Data da Compra').groupby(pd.Grouper(freq = 'M'))['Preço'].count()).reset_index()
vendas_mensal['Ano'] = vendas_mensal['Data da Compra'].dt.year
vendas_mensal['Mes'] = vendas_mensal['Data da Compra'].dt.month_name()

vendas_categorias = pd.DataFrame(df_filtrado.groupby('Categoria do Produto')['Preço'].count().sort_values(ascending = False))

### Vendedores
vendedores = pd.DataFrame(df_filtrado.groupby('Vendedor')['Preço'].agg(['sum', 'count']))


## Gráficos
### Gráficos de receita
fig_mapa_receita = px.scatter_geo(receitas_estados,
                                  lat = 'lat',
                                  lon = 'lon',
                                  scope = 'south america',
                                  size = 'Preço',
                                  template = 'seaborn',
                                  hover_name = 'Local de compra',
                                  hover_data = {'lat': False, 'lon': False},
                                  title = 'Receita por estado')

fig_receita_mensal = px.line(receita_mensal,
                             x = 'Mes',
                             y = 'Preço',
                             markers=True,
                             range_y = (0, receita_mensal['Preço'].max()),
                             color='Ano',
                             line_dash='Ano',
                                title = 'Receita mensal')

fig_receita_mensal.update_layout(yaxis_title='Receita (R$)')

fig_receita_estados = px.bar(receitas_estados.head(),
                             x = 'Local de compra',
                             y = 'Preço',
                             text_auto=True,
                             title='Top estados (receita)')

fig_receita_estados.update_layout(yaxis_title='Receita (R$)')

fig_receita_categorias = px.bar(receita_categorias.head(),
                                text_auto=True,
                                title='Receita por categoria')

fig_receita_categorias.update_layout(yaxis_title='Receita (R$)')                                


### Gráficos de quantidade de vendas
fig_mapa_vendas = px.scatter_geo(vendas_estados,
                                  lat = 'lat',
                                  lon = 'lon',
                                  scope = 'south america',
                                  size = 'Preço',
                                  template = 'seaborn',
                                  hover_name = 'Local de compra',
                                  hover_data = {'lat': False, 'lon': False},
                                  title = 'Vendas por estado')

fig_vendas_mensal = px.line(vendas_mensal,
                            x = 'Mes',
                            y = 'Preço',
                            markers=True,
                            range_y = (0, vendas_mensal.max()),
                            color='Ano',
                            line_dash='Ano',
                            title='Quantidade de vendas mensal')

fig_vendas_mensal.update_layout(yaxis_title='Quantidade de vendas')

fig_vendas_estados = px.bar(vendas_estados.head(), 
                            x = 'Local de compra',
                            y = 'Preço',
                            text_auto=True,
                            title='Top 5 estados')

fig_vendas_categorias = px.bar(vendas_categorias,
                                text_auto=True,
                                title='Vendas por categoria')

fig_vendas_categorias.update_layout(showlegend=False, yaxis_title='Quantidade de vendas')

## Visualizacao no streamlit
aba1, aba2, aba3 = st.tabs(['Receita', 'Quantidade de vendas', 'Vendedores'])


with aba1:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', formata_numero(df_filtrado['Preço'].sum(), 'R$'))
        st.plotly_chart(fig_mapa_receita, use_container_width=True)
        st.plotly_chart(fig_receita_estados, use_container_width=True)
    with coluna2:
        st.metric('Quantidade de vendas', formata_numero(df_filtrado.shape[0]))
        st.plotly_chart(fig_receita_mensal, use_container_width=True)
        st.plotly_chart(fig_receita_categorias, use_container_width=True)

with aba2:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', formata_numero(df_filtrado['Preço'].sum(), 'R$'))
        st.plotly_chart(fig_mapa_vendas, use_container_width=True)
        st.plotly_chart(fig_vendas_estados, use_container_width=True)
        
    with coluna2:
        st.metric('Quantidade de vendas', formata_numero(df_filtrado.shape[0]))
        st.plotly_chart(fig_vendas_mensal, use_container_width=True)
        st.plotly_chart(fig_vendas_categorias, use_container_width=True)
        

with aba3:
    qtd_vendedores = st.number_input('Quantidade de vendedores', min_value=2, max_value=10, value=5)
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', formata_numero(df_filtrado['Preço'].sum(), 'R$'))
        fig_receita_vendedores = px.bar(vendedores[['sum']].sort_values('sum', ascending=False).head(qtd_vendedores),
                                 x = 'sum',
                                 y = vendedores[['sum']].sort_values('sum', ascending=False).head(qtd_vendedores).index,
                                 text_auto=True,
                                 title=f'Top {qtd_vendedores} vendedores (receita)')
        st.plotly_chart(fig_receita_vendedores, use_container_width=True)
    with coluna2:
        st.metric('Quantidade de vendas', formata_numero(df_filtrado.shape[0]))
        fig_vendas_vendedores = px.bar(vendedores[['count']].sort_values('count', ascending=False).head(qtd_vendedores),
                                 x = 'count',
                                 y = vendedores[['count']].sort_values('count', ascending=False).head(qtd_vendedores).index,
                                 text_auto=True,
                                 title=f'Top {qtd_vendedores} vendedores (quantidade de vendas)')
        st.plotly_chart(fig_vendas_vendedores, use_container_width=True)
