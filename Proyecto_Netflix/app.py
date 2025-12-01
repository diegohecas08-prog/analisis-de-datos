import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Netflix App", layout="wide")

# 1. CONSUMO DE DATOS (Simulación API)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/SahilChachra/Netflix-Data-Visualization/master/netflix_titles.csv"
    df = pd.read_csv(url)
    df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')
    return df

df = load_data()

# 2. SIDEBAR Y FILTROS
st.sidebar.header("Filtros")
page = st.sidebar.radio("Navegación", ["Dashboard", "Datos", "Feedback"]) # Comp 1
pais = st.sidebar.multiselect("País", df['country'].value_counts().index[:10]) # Comp 2
anio = st.sidebar.slider("Año", 2000, 2021, (2015, 2021)) # Comp 3

# Lógica de Filtrado
data = df[(df['release_year'].between(anio[0], anio[1]))]
if pais: data = data[data['country'].str.contains('|'.join(pais), na=False)]

# --- 3. ESTRUCTURA PRINCIPAL ---
if page == "Dashboard":
    st.title("Análisis de Contenido Netflix")
    
    # KPIs (Métricas clave)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Títulos", len(data)) 
    c2.metric("Películas", len(data[data['type']=='Movie'])) 
    c3.metric("Series TV", len(data[data['type']=='TV Show'])) 

    # Organización por Pestañas
    tab1, tab2 = st.tabs(["Distribución", "Detalles"]) 

    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            # Gráfico 1: Torta 
            st.plotly_chart(px.pie(
                data, 
                names='type', 
                title="Proporción Películas vs Series",
                color_discrete_sequence=px.colors.sequential.Reds_r
            ), use_container_width=True)
            st.info("La mayoría del catálogo corresponde a películas.") 
            
        with col_b:
            # Gráfico 2: Área 
            conteo = data.groupby(data['date_added'].dt.year)['show_id'].count().reset_index()
            st.plotly_chart(px.area(
                conteo, 
                x='date_added', 
                y='show_id', 
                title="Títulos agregados por año",
                color_discrete_sequence=['#E50914'] 
            ), use_container_width=True)
            st.info("Se observa un crecimiento exponencial desde 2016.") 

    with tab2:
        col_c, col_d = st.columns(2)
        with col_c:
            # Gráfico 3: Barras 
            top_ratings = data['rating'].value_counts().head(5)
            st.plotly_chart(px.bar(
                top_ratings, 
                title="Top 5 Clasificaciones",
                color_discrete_sequence=px.colors.sequential.RdBu 
            ), use_container_width=True)
            
        with col_d:
            # Gráfico 4: Histograma 
            movies = data[data['type']=='Movie']
            st.plotly_chart(px.histogram(
                movies, 
                x='duration', 
                title="Duración de Películas",
                color_discrete_sequence=['#221f1f'] 
            ), use_container_width=True)
            
        st.success("El contenido para adultos (TV-MA) domina la oferta actual.")