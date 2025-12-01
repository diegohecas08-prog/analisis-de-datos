import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Netflix", layout="wide", page_icon="🎬")

@st.cache_data
def load():
    url = "https://raw.githubusercontent.com/SahilChachra/Netflix-Data-Visualization/master/netflix_titles.csv"
    df = pd.read_csv(url)
    df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')
    return df

try:
    df = load()
except:
    df = pd.DataFrame()

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=120)
page = st.sidebar.radio("Menú", ["Dashboard", "Datos", "Feedback"])
pais = st.sidebar.multiselect("País", df['country'].value_counts().index[:10] if not df.empty else [])
anio = st.sidebar.slider("Año", 2000, 2021, (2015, 2021))

data = df[df['release_year'].between(anio[0], anio[1])] if not df.empty else df
if pais and not data.empty: data = data[data['country'].str.contains('|'.join(pais), na=False)]

if page == "Dashboard":
    st.title("Análisis Netflix")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total", len(data)); c2.metric("Películas", len(data[data['type']=='Movie'])); c3.metric("Series", len(data[data['type']=='TV Show']))
    
    t1, t2 = st.tabs(["General", "Detalle"])
    with t1:
        ca, cb = st.columns(2)
        ca.plotly_chart(px.pie(data, names='type', title="peliculas y series", color_discrete_sequence=px.colors.sequential.Reds_r), use_container_width=True)
        cb.plotly_chart(px.area(data.groupby(data['date_added'].dt.year)['show_id'].count().reset_index(), x='date_added', y='show_id', title="Evolución", color_discrete_sequence=['#E50914']), use_container_width=True)
        st.info("Predominan películas y crecimiento reciente.")
    with t2:
        cc, cd = st.columns(2)
        cc.plotly_chart(px.bar(data['rating'].value_counts().head(), title="Ratings", color_discrete_sequence=px.colors.sequential.Reds_r), use_container_width=True)
        cd.plotly_chart(px.histogram(data[data['type']=='Movie'], x='duration', title="Duración", color_discrete_sequence=['#221f1f']), use_container_width=True)
        st.success("Contenido adulto (TV-MA) es mayoría.")

elif page == "Datos":
    st.title("Datos")
    st.dataframe(data if st.checkbox("Ver todo") else data.iloc[:, :5], use_container_width=True)
    st.download_button("Bajar CSV", data.to_csv(index=False).encode('utf-8'), "netflix.csv")

elif page == "Feedback":
    st.title("Opinión")
    with st.form("f"):
        st.text_input("Nombre"); st.slider("Nota", 1, 7)
        if st.form_submit_button("Enviar"): st.toast("¡Enviado!")









