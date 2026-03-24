import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout="wide")

st.title('Projet Final Jessica SOSSOU : ANALYSE ET VISUALISATION DE DONNÉES')



# Importons la donnée
@st.cache_data
def load_data():
    return pd.read_csv("Dataset.csv")

data = load_data()

st.title("Tableau de bord interactif - Analyse des Transactions")

#  Sidebar - Filtres dynamiques
st.sidebar.header("Filtres")

# Conversion Date si présente
if 'Date' in data.columns:
    data['Date'] = pd.to_datetime(data['Date'])
    date_min = data['Date'].min()
    date_max = data['Date'].max()
    date_range = st.sidebar.date_input("Filtrer par Date", [date_min, date_max])

    if len(date_range) == 2:
        data = data[(data['Date'] >= pd.to_datetime(date_range[0])) & (data['Date'] <= pd.to_datetime(date_range[1]))]

# # Filtres catégoriels multiples
colonnes_categorique = data.select_dtypes(include=['object', 'category']).columns.tolist()
for col in colonnes_categorique:
    valeurs = data[col].unique().tolist()
    selection = st.sidebar.multiselect(f"{col}", valeurs, default=valeurs)
    data = data[data[col].isin(selection)]

#  Sélection pour Graphiques
colonnes_numerique = data.select_dtypes(include=['float64', 'int64']).columns.tolist()

col_x = st.sidebar.selectbox("Variable X (catégorique)", colonnes_categorique)
col_y = st.sidebar.selectbox("Variable Y (numérique)", colonnes_numerique)
col_color = st.sidebar.selectbox("Variable couleur (optionnel)", [None] + colonnes_categorique)

# Affichage des Graphiques

# Ligne de tendance par date
if 'Date' in data.columns:
    st.subheader("Évolution temporelle")
    line_data = data.groupby('Date')[col_y].mean().reset_index()
    fig_line = px.line(line_data, x='Date', y=col_y, title=f"{col_y} moyen au fil du temps")
    st.plotly_chart(fig_line, use_container_width=True)

# Histogramme
#st.subheader("Histogramme interactif")
# fig_hist = px.histogram(data, x=col_y, color=col_color, nbins=30)
# st.plotly_chart(fig_hist, use_container_width=True)

# Barre chat dynamique
st.subheader("Diagramme en barres")

fig_bar = px.bar(
    data,
    x=col_x,
    y=col_y,
    color=col_color,
    title=f"{col_y} par {col_x}"
)

st.plotly_chart(fig_bar, use_container_width=True)

# Box plot 
st.subheader("Distribution (Boxplot)")

fig_box = px.box(
    data,
    x=col_x,
    y=col_y,
    color=col_color,
    title=f"Distribution de {col_y} par {col_x}"
)

st.plotly_chart(fig_box, use_container_width=True)

#Pie chart 
st.subheader("Répartition")

pie_data = data[col_x].value_counts().reset_index()
pie_data.columns = [col_x, 'Count']

fig_pie = px.pie(
    pie_data,
    names=col_x,
    values='Count',
    title=f"Répartition de {col_x}"
)

st.plotly_chart(fig_pie, use_container_width=True)

#Heatmap
st.subheader("Corrélation entre variables numériques")

corr = data.select_dtypes(include=['float64', 'int64']).corr()

fig_heatmap = px.imshow(
    corr,
    text_auto=True,
    title="Matrice de corrélation"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# Analyse de fraude
if 'FraudResult' in data.columns:
    st.subheader("Analyse de fraude")

    fraud_by_cat = data.groupby(col_x)['FraudResult'].mean().reset_index()

    fig_fraud = px.bar(
        fraud_by_cat,
        x=col_x,
        y='FraudResult',
        color='FraudResult',
        title=f"Taux de fraude par {col_x}"
    )

    st.plotly_chart(fig_fraud, use_container_width=True)

    # 7. Téléchargement des données filtrées
csv = data.to_csv(index=False).encode('utf-8')
st.download_button("Télécharger les données filtrées", csv, "transactions_filtrées.csv", "text/csv")