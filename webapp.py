__version__ = '0.1.0'
import streamlit as st
import yfinance as yf
import pandas as pd
from PIL import Image
from datetime import date
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
from plotly import graph_objs as go

#add logo dastratus
col1, col2 = st.columns([3,1])
with col1:
    st.title('Stratus')
with col2:
    image = Image.open('logo_blue.png')
    st.image(image, width=150)

#define a data de início e fim
data_inicio = '2017-01-01'
data_fim = date.today().strftime('%Y-%m-%d')

#cabeçalho

st.subheader('Análise de Ações')
st.sidebar.subheader('Escolha uma ação:')
n_dias = st.sidebar.select_slider('Quantidade de dias de previsão',options=[30, 60, 120, 240, 360])

#coleta dos dados no .csv
def pegar_dados_acoes():
    path = 'acoes.csv'
    return pd.read_csv(path, delimiter=';')

df = pegar_dados_acoes()

acao = df['snome']
nome_acao_escolhida = st.sidebar.selectbox('Escolha uma ação:' , acao)

df_acao = df[df['snome'] == nome_acao_escolhida]
acao_escolida = df_acao.iloc[0]['sigla_acao']
acao_escolida = acao_escolida + '.SA'

@st.cache
def pegar_valores_online(sigla_acao):
    df = yf.download(sigla_acao, data_inicio, data_fim)
    df.reset_index(inplace=True)
    return df

df_valores = pegar_valores_online(acao_escolida)
st.subheader('Tabela de Valores - ' + nome_acao_escolhida)
st.write(df_valores.tail(10))

#plota o gráfico de preços das açoes
st.subheader('Gráfico de Preços')
fig = go.Figure(data=[go.Candlestick(x=df_valores['Date'],open=df_valores['Open'],high=df_valores['High'],low=df_valores['Low'],close=df_valores['Close'])])
st.plotly_chart(fig)

''''#define as variáveis de treino
df_treino = df_valores[['Date','Close']]
df_treino = df_treino.rename(columns={'Date':'ds', 'Close': 'y'})

#treina o modelo
modelo = Prophet()
modelo.fit(df_treino)
futuro = modelo.make_future_dataframe(periods=n_dias, freq='B')
previsao = modelo.predict(futuro)

#plota os gráficos do treino
st.subheader('Previsão')
st.write(previsao[['ds', 'yhat','yhat_lower','yhat_upper']].tail(n_dias))

#gráfico 1
st.subheader('Gráfico de Preços')
grafico1 = plot_plotly(modelo, previsao)
st.plotly_chart(grafico1)'''
