import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados
data = pd.read_csv('vgchartz-2024.csv')

# Verificar se a coluna release_date existe e converter para datetime
if 'release_date' in data.columns:
    data['release_date'] = pd.to_datetime(data['release_date'], format='%Y-%m-%d', errors='coerce')
    if data['release_date'].isnull().any():
        st.warning("Algumas datas no dataset são inválidas e foram ignoradas.")
else:
    st.error("A coluna 'release_date' não foi encontrada no dataset.")

# Funções auxiliares
def generos_mais_vendidos(data):
    vendas_por_genero = data.groupby('genre')['total_sales'].sum()
    vendas_por_genero = vendas_por_genero[vendas_por_genero >= 10].sort_values(ascending=False)
    return vendas_por_genero
    

def consoles_mais_vendidos(data):
    vendas_por_console = data.groupby('console')['total_sales'].sum()
    vendas_por_console = vendas_por_console[vendas_por_console >= 10].sort_values(ascending=False)
    return vendas_por_console


def media_notas_por_genero(data):
    media_notas = data.groupby('genre')['critic_score'].mean()
    media_notas = media_notas[data.groupby('genre')['total_sales'].sum() >= 10].sort_values(ascending=False)
    return media_notas

def generos_mais_vendidos_por_pais(data):
    paises = {
        'na_sales': 'América do Norte',
        'jp_sales': 'Japão',
        'pal_sales': 'Europa',
        'other_sales': 'Outras Regiões'
    }
    vendas_por_genero_pais = {
        pais: data.groupby('genre')[col].sum().sort_values(ascending=False)
        for col, pais in paises.items()
    }
    vendas_por_genero_pais = {
        pais: vendas[vendas >= 50] for pais, vendas in vendas_por_genero_pais.items()
    }
    return vendas_por_genero_pais

def media_notas_por_ano(data):
    if 'release_date' in data.columns and not data['release_date'].isnull().all():
        data['year'] = data['release_date'].dt.year
        media_notas_ano = data.groupby('year')['critic_score'].mean()
        media_notas_ano = media_notas_ano[data.groupby('year')['total_sales'].sum() >= 50]
        return media_notas_ano
    else:
        st.error("Não é possível calcular a média de notas por ano, pois 'release_date' está ausente ou inválida.")
        return pd.Series()

# Configuração do Streamlit
st.title("Análise de Vendas de Jogos")
st.sidebar.header("Configurações")

# Número de jogos vendidos ao longo dos anos (até 2015)
if 'release_date' in data.columns and not data['release_date'].isnull().all():
    data['year'] = data['release_date'].dt.year
    vendas_por_ano = data.groupby('year')['total_sales'].sum()

    # Filtrar para anos até 2015
    vendas_por_ano = vendas_por_ano[vendas_por_ano.index <= 2015]

    st.subheader("Número de Jogos Vendidos ao Longo dos Anos (Até 2015)")
    fig, ax = plt.subplots()
    vendas_por_ano.plot(kind='line', ax=ax, marker='o', color='blue')
    plt.title("Número de Jogos Vendidos ao Longo dos Anos (Até 2015)")
    plt.xlabel("Ano")
    plt.ylabel("Vendas Totais (em milhões)")
    st.pyplot(fig)
    st.write(
        "O gráfico acima mostra a evolução das vendas de jogos até 2015, destacando como tendências de mercado e novos lançamentos influenciaram o número de jogos vendidos ao longo do tempo."
    )
else:
    st.error("Não foi possível gerar o gráfico, pois os dados de 'release_date' estão ausentes ou inválidos.")



# Gêneros mais vendidos
genero_vendas = generos_mais_vendidos(data)
st.subheader("Gêneros Mais Vendidos")
fig, ax = plt.subplots()
genero_vendas.plot(kind='bar', ax=ax, color='skyblue')
plt.title("Gêneros Mais Vendidos")
plt.xlabel("Gênero")
plt.ylabel("Vendas Totais")
st.pyplot(fig)
st.write("É possível perceber que os gêneros de jogos mais vendidos ao redor do mundo são os de esportes, ação e tiro. ")

# Consoles mais vendidos
console_vendas = consoles_mais_vendidos(data)
st.subheader("Consoles Mais Vendidos")
fig, ax = plt.subplots()
console_vendas.plot(kind='bar', ax=ax, color='orange')
plt.title("Consoles Mais Vendidos")
plt.xlabel("Console")
plt.ylabel("Vendas Totais")
st.pyplot(fig)
st.write("Mesmo com o aumento do numero de vendas ao longo dos anos, é possível ver que os consoles mais antigos ainda são os mais vendidos.")

# Média de notas por gênero
media_genero = media_notas_por_genero(data)
st.subheader("Média de Notas por Gênero")
fig, ax = plt.subplots()
media_genero.plot(kind='bar', ax=ax, color='green')
plt.title("Média de Notas por Gênero")
plt.xlabel("Gênero")
plt.ylabel("Média de Notas")
st.pyplot(fig)
st.write("Aqui vemos a média das notas dadas pelos críticos, agrupadas por gênero.")

# Gêneros mais vendidos por país

vendas_por_pais = generos_mais_vendidos_por_pais(data)
st.subheader("Gêneros Mais Vendidos por País")
for pais, vendas in vendas_por_pais.items():
    st.write(f"Vendas em {pais}")
    fig, ax = plt.subplots()
    vendas.plot(kind='bar', ax=ax, color='purple')
    plt.title(f"Gêneros Mais Vendidos em {pais}")
    plt.xlabel("Gênero")
    plt.ylabel("Vendas Totais")
    st.pyplot(fig)

st.write(
    "Com este gráfico é possível perceber alguns dos diferentes gostos dentro de cada região do planeta. "
    "Nos países do ocidente há uma preferência por jogos de esportes e ação, enquanto que no representante do oriente, o Japão, "
    "existe uma preferência por jogos de RPG."
)

# Média de notas por ano
media_ano = media_notas_por_ano(data)
if not media_ano.empty:
    st.subheader("Média de Notas por Ano")
    fig, ax = plt.subplots()
    media_ano.plot(kind='line', ax=ax, marker='o', color='red')
    plt.title("Média de Notas por Ano")
    plt.xlabel("Ano")
    plt.ylabel("Média de Notas")
    st.pyplot(fig)
    st.write("Muito embora o mercado de games tenha crescido ao longo dos anos, é possível perceber que isso não reflete necessariamente nas notas, muito embora elas tenham aumentado em média, não existe uma grande variação ao longo dos anos. ")

# Correlação entre vendas e notas
st.subheader("Correlação entre Vendas e Notas")
fig, ax = plt.subplots()
data.plot.scatter(x='critic_score', y='total_sales', ax=ax, color='darkorange', alpha=0.6)
plt.title("Correlação entre Notas e Vendas")
plt.xlabel("Notas dos Críticos")
plt.ylabel("Vendas Totais")
st.pyplot(fig)
st.write("É Possível observar através desse gráfico que jogos com notas medianas a altas tendem a vender mais do que os jogos com notas baixas ou muito baixas")


st.title("Conclusão")
st.write("Com essa breve análise foi possível observar algumas tendências de mercado e de indústria dentro do universo dos jogos. Por um lado, podemos perceber alguns costumes de consumo de certos mercados dentro de diferentes países e como as vendas dos jogos variam ao longo do tempo. Por outro lado, temos uma visão geral de como a indústria foi se adaptando para criar jogos que atendessem as demandas dos jogadores.")
