__version__ = '0.1.1'
import streamlit as st
import yfinance as yf
import pandas as pd
from PIL import Image
from datetime import date
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

#add logo dastratus
col1, col2 = st.columns([3,1])
with col1:
    st.title('Stratus v0.1.2')
with col2:
    image = Image.open('logo_blue.png')
    st.image(image, width=150)

#define a data de início e fim
data_inicio = '2017-01-01'
data_fim = date.today().strftime('%Y-%m-%d')

#cabeçalho

st.subheader('Análise e Predição de Ações')
st.sidebar.subheader('Escolha uma ação:')
n_dias = st.sidebar.select_slider('Quantidade de dias de previsão',options=[30, 60, 120, 240, 360])

#coleta dos dados no .csv
def pegar_dados_acoes():
    path = 'acoes.csv'
    return pd.read_csv(path, delimiter=';')

df = pegar_dados_acoes()

acao = df['snome']
nome_acao_escolhida = st.sidebar.selectbox('Escolha uma ação:', acao)
df_acao = df[df['snome'] == nome_acao_escolhida]
acao_escolida = df_acao.iloc[0]['sigla_acao']
acao_escolida = acao_escolida + '.SA'

#coleta os dados da acao online e formata a tabela
@st.cache
def pegar_valores_online(sigla_acao):
    df = yf.download(sigla_acao, data_inicio, data_fim)
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y').dt.date

    columns = {
        'Date': 'Data',
        'Open': 'Abertura',
        'High': 'Alta',
        'Low': 'Baixa',
        'Close': 'Fechamento'
    }
    del df ['Adj Close']
    df = df.rename(columns=columns)
    return df

df_valores = pegar_valores_online(acao_escolida)

st.subheader('Informações da ação escolhida : ')
st.subheader(nome_acao_escolhida + ' - Ultimos 8 dias')
st.write(df_valores.tail(8))

#plota o gráfico de preços das açoes
st.header('Gráfico de Preços')
fig = go.Figure(data=[go.Candlestick(
    x=df_valores['Data'], open=df_valores['Abertura'], high=df_valores['Alta'], low=df_valores['Baixa'], close=df_valores['Fechamento'])])
st.plotly_chart(fig,use_container_width=False)

#define as variáveis de treino
df_treino = df_valores[['Data', 'Fechamento']]
df_treino = df_treino.rename(columns={'Data': 'ds', 'Fechamento': 'y'})

#treina o modelo
modelo = Prophet()
modelo.fit(df_treino)
futuro = modelo.make_future_dataframe(periods=n_dias, freq='B')
previsao = modelo.predict(futuro)

#plota os gráficos do treino
st.subheader('Previsão')
previsao['ds'] = pd.to_datetime(previsao['ds']).dt.date
st.write(previsao[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(n_dias))

st.download_button(
    label='Download previsão.csv',
    data=previsao.to_csv(index=False, header=True),
    file_name='previsao' + nome_acao_escolhida + '.csv'
)

#gráfico 1
st.subheader('Gráfico de Preços')
grafico1 = plot_plotly(modelo, previsao)
st.plotly_chart(grafico1)