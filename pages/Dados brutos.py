import streamlit as st
# import requests
import pandas as pd
import time

@st.cache_data
def converte_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def mensagem_sucesso():
    sucesso = st.success('Download realizado com sucesso!', icon="✅")
    time.sleep(5)
    sucesso.empty()

st.title('DADOS BRUTOS')

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

df = pd.DataFrame(data)
df['Data da Compra'] = pd.to_datetime(df['Data da Compra'], format='%d/%m/%Y')


with st.expander("Colunas", expanded=True):
    colunas = st.multiselect('Selecione as colunas', df.columns.tolist(), default=df.columns.tolist())

with st.sidebar.expander('Nome do produto'):
    produtos = st.multiselect('Selecione os produtos', df['Produto'].unique(), df['Produto'].unique())
with st.sidebar.expander('Categoria do produto'):
    categoria = st.multiselect('Selecione as categorias', df['Categoria do Produto'].unique(), df['Categoria do Produto'].unique())
with st.sidebar.expander('Preço do produto'):
    preco = st.slider('Selecione o preço', 0, 5000, (0,5000))
with st.sidebar.expander('Frete da venda'):
    frete = st.slider('Frete', 0,250, (0,250))
with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Selecione a data', (df['Data da Compra'].min(), df['Data da Compra'].max()))
with st.sidebar.expander('Vendedor'):
    vendedores = st.multiselect('Selecione os vendedores', df['Vendedor'].unique(), df['Vendedor'].unique())
with st.sidebar.expander('Local de compra'):
    local_compra = st.multiselect('Selecione o local de compra', df['Local de compra'].unique(), df['Local de compra'].unique())
with st.sidebar.expander('Avaliação da compra'):
    avaliacao = st.slider('Selecione a avaliação da compra',1,5, value = (1,5))
with st.sidebar.expander('Tipo de pagamento'):
    tipo_pagamento = st.multiselect('Selecione o tipo de pagamento',df['Tipo de pagamento'].unique(), df['Tipo de pagamento'].unique())
with st.sidebar.expander('Quantidade de parcelas'):
    qtd_parcelas = st.slider('Selecione a quantidade de parcelas', 1, 24, (1,24))


query = '''
Produto in @produtos and \
@preco[0] <= Preço <= @preco[1] and \
@data_compra[0] <= `Data da Compra` <= @data_compra[1]
'''

df_filtrado = df.query(query)
df_filtrado = df_filtrado[colunas]

st.dataframe(df_filtrado, use_container_width=True)

st.markdown(f'A tabela possui :blue[{df_filtrado.shape[0]}] linhas e :blue[{df_filtrado.shape[1]}] colunas.')

st.markdown('Escreva um nome para o arquivo')
coluna1, coluna2 = st.columns(2)
with coluna1:
    nome_arquivo = st.text_input('', label_visibility = 'collapsed', value='dados')
    nome_arquivo += '.csv'
with coluna2:
    st.download_button('Fazer o download da tabela em csv', 
                       data = converte_csv(df_filtrado), 
                       file_name=nome_arquivo, 
                       mime='text/csv', on_click=mensagem_sucesso)
