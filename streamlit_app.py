import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

st.title("Analiza i vizualizacija podataka o igrama")

engine = create_engine("sqlite:///C:/Users/Andro/Desktop/a/igre_baza.db")

@st.cache_data
def fetch_data():
    with engine.connect() as connection:
        query = "SELECT Name, Platform, Genre, Global_Sales FROM igre"
        df = pd.read_sql(query, connection)
    return df

data = fetch_data()

if st.checkbox("Prikaži podatke"):
    st.write(data)

#Zbrajam podatke ukupne prodaje igara za svaki platfirmu
st.subheader("Ukupna prodaja po igrama")
game_platform_sales = data.groupby(['Name', 'Platform'], as_index=False)['Global_Sales'].sum()
game_platform_sales['Name'] = game_platform_sales['Name'].str.strip().str.lower().str.title()  # Ocistit podatke o imenima
game_platform_sales = game_platform_sales.sort_values(by='Global_Sales', ascending=False)
st.write(game_platform_sales)

top_20_games = game_platform_sales.groupby('Name', as_index=False).sum().nlargest(20, 'Global_Sales')

# Uvoz neke ekstenzije kako bih si mogao prikazat platforme drukcijim bojama
st.subheader("Graf: Top 20 igara po ukupnoj prodaji s platformama")
fig = px.bar(
    game_platform_sales[game_platform_sales['Name'].isin(top_10_games['Name'])],
    x='Name',
    y='Global_Sales',
    color='Platform',
    title="Top 20 igara po ukupnoj prodaji",
    labels={'Global_Sales': 'Ukupna prodaja (milijuni)', 'Name': 'Ime igre'},
    height=600
)
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig)

st.write("""
Ovaj graf prikazuje ukupnu prodaju top 20 igara po platformama. Na X-osi nalaze se imena igara, dok Y-os prikazuje ukupnu prodaju izraženu u milijunima primjeraka. Boje u grafu predstavljaju različite platforme, omogućujući analizu popularnosti igara na specifičnim uređajima.
Dodatno, graf uključuje usporedbu između PC-a i konzola, kao i ostalih platformi, čime se jasno ističe dominacija konzola u odnosu na PC kada je riječ o ukupnoj prodaji igara. Kod konzola se posebice ističu platforme PlayStation 3 (PS3) i Xbox 360 (X360), koje su najzastupljenije među najprodavanijim igrama.
Ovaj prikaz omogućuje lako uočavanje razlika u popularnosti igara između platformi te naglašava ulogu konzola kao glavnih nositelja prodaje igara, dok je PC zastupljen u znatno manjoj mjeri. Ostale platforme, poput prijenosnih konzola, također su uključene, ali njihov doprinos prodaji je znatno manji u usporedbi s glavnim konzolama PS3 i X360.
Analiza ovih podataka pruža uvid u tržišne trendove, ukazujući na to koje platforme dominiraju tržištem i koje su igre ključne za njihov uspjeh, ali bitno je primjetiti da su ovo igrice koje su izlazile prije 10-ak godina.
""")

# 2. Graf ukupne prodaje po platformama
st.subheader("Ukupna prodaja po platformama")
platform_sales = data.groupby('Platform', as_index=False)['Global_Sales'].sum().sort_values(by='Global_Sales', ascending=False)
st.bar_chart(platform_sales.set_index('Platform')['Global_Sales'])

st.write("""
    Ovaj graf prikazuje ukupnu prodaju igara po platformama. Na X osi su prikazane platforme (npr. PS3, Xbox, PC), 
    dok Y os prikazuje ukupnu prodaju u milijunima primjeraka. Graf pomaže u razumijevanju koje platforme 
    imaju najveći udio u ukupnoj prodaji.
""")

# 3. Graf ukupne prodaje po žanrovima
st.subheader("Ukupna prodaja po žanrovima")
genre_sales = data.groupby('Genre', as_index=False)['Global_Sales'].sum().sort_values(by='Global_Sales', ascending=False)
st.bar_chart(genre_sales.set_index('Genre')['Global_Sales'])

st.write("""
    Ovaj graf prikazuje ukupnu prodaju po žanrovima igara. Na X osi su prikazani žanrovi igara (npr. Akcija, Avantura, Sport), 
    dok Y os prikazuje ukupnu prodaju u milijunima primjeraka. Ovo pomaže u razumijevanju koji žanrovi igara 
    dominiraju na tržištu prema ukupnoj prodaji.
""")

# Filtriranje podataka
st.sidebar.header("Filtriraj podatke")
filter_column = st.sidebar.selectbox("Odaberi stupac za filtriranje", data.columns)
unique_values = data[filter_column].unique()
selected_value = st.sidebar.selectbox("Odaberi vrijednost", unique_values)

filtered_data = data[data[filter_column] == selected_value]
st.write(f"Podaci filtrirani po {filter_column} = {selected_value}", filtered_data)
