__version__ = '0.1.0'
#importação das bibliotecas
import streamlit as st
import yfinance as yf
from datetime import date
import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
from plotly import graph_objs as go


#define a data de início e fim
DATA_INICIO = '2017-01-01'
DATA_FIM = date.today().strftime('%Y-%m-%d')

#cabeçalho
st.title('Análise de Ações')
st.sidebar.header('Escolha a ação')
n_dias = st.slider('Quantidade de dias de previsão' , 30,365)

#coleta dos dados no .csv
def pegar_dados_acoes():
    path = 'C:/Users/bruno/Downloads/acoes.csv'
    return pd.read_csv(path, delimiter=';')

df = pegar_dados_acoes()

acao = df['snome']
nome_acao_escolhida = st.sidebar.selectbox('Escolha uma ação:' , acao)

df_acao = df[df['snome'] == nome_acao_escolhida]
acao_escolida = df_acao.iloc[0]['sigla_acao']
acao_escolida = acao_escolida + '.SA'

@st.cache
def pegar_valores_online(sigla_acao):
    df = yf.download(sigla_acao, DATA_INICIO, DATA_FIM)
    df.reset_index(inplace=True)
    return df

df_valores = pegar_valores_online(acao_escolida)
st.subheader('Tabela de Valores - ' + nome_acao_escolhida)
st.write(df_valores.tail(10))

#plota o gráfico de preços das açoes
st.subheader('Gráfico de Preços')
fig = go.Figure(data=[go.Candlestick(x=df_valores['Date'],open=df_valores['Open'],high=df_valores['High'],low=df_valores['Low'],close=df_valores['Close'])])
#fig.add_trace(go.Candlestick(x=df_valores['Date'],y=df_valores['Close'],name='Preço de Fechamento',line_color='blue'))
#fig.add_trace(go.Candlestick(x=df_valores['Date'],y=df_valores['Open'],name='Preço de Abertura',line_color='red'))
st.plotly_chart(fig)

""""#define as variáveis de treino
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
st.subheader('Gráfico de Preços')

#gráfico 1
grafico1 = plot_plotly(modelo, previsao)
st.plotly_chart(grafico1)

#gráfico2
grafico2 = plot_components_plotly(modelo, previsao)
st.plotly_chart(grafico2)"""