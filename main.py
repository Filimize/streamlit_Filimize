import pandas as pd
import streamlit as st
from collections import Counter
from itertools import chain
import plotly.express  as px


st.set_page_config(layout="wide")

st.header("Pokedex 1-555")
st.markdown('This website got the data from [**Pokemondb**](http://pokemondb.net/pokedex/all)')

##search bar
# dont forget to change dicretory (cd)
df = pd.read_csv(r"pokedex.csv")
df['types'] = df['types'].apply(lambda x: x.replace('[','').replace(']','').replace('\'','').replace(' ','').split(","))
search_name = st.text_input(':green[Search the name of pokemon]:heavy_exclamation_mark:')
search_name_norm = search_name.capitalize()
fitered_name = df[df['name'].str.contains(search_name_norm, case=False, na=False)]

if search_name != '':
    df_name = fitered_name
else:
    df_name = df



st.sidebar.header('User Input Features')
all_types = ['Bug','Normal','Dark','Electric','Poison','Dragon','Ghost','Water','Fighting','Fire','Ground','Rock','Flying','Ice','Steel','Grass','Psychic','Fairy']
selected_type = st.sidebar.multiselect('Select the type', all_types, all_types)

## Filtering types
if set(selected_type) == set(all_types):
    df_types = df.copy()  
else:  
    df_types = df[df['types'].apply(set).apply(lambda x: x.issubset(set(selected_type)))]

## merge df1 df2
df_show = pd.merge(df_name,df_types, on='name', how='inner', suffixes=('', '_remove'))
 
# remove the duplicate columns
df_show.drop([i for i in df_show.columns if 'remove' in i], axis=1, inplace=True)


st.subheader('Table results',divider='rainbow')
st.markdown('* Result Table from filtering :blue[pokemon name] :blush:')
st.write(df_name)
st.markdown('* Result Table from filtering :blue[pokemon type(s)] :sunglasses:')
st.write(df_types)
st.markdown('* Result Table from merging two tables :blue[pokemon name & pokemon type(s)] :neutral_face:')
st.write(df_show)


st.subheader('Chart Results', divider='rainbow')

## Bar Chart
# Flatten set and count freq
counter = Counter(chain.from_iterable(df_show['types']))

# Creating df
bar_chart_df = pd.DataFrame.from_dict(counter, orient='index').reset_index()
bar_chart_df.columns = ['Item', 'Frequency']

# Use the DataFrame directly
st.markdown('* Bar chart')
st.bar_chart(bar_chart_df.set_index('Item'))

## Corr
st.markdown("* Correlation Chart")
# Extracting data get only numeric data
num_df = df_show.select_dtypes(include='number')
num_df.drop(columns='id',inplace=True)
corr = num_df.corr()
fig = px.imshow(corr, text_auto=True, aspect="auto")

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
with tab1:
    st.plotly_chart(fig, theme="streamlit")
with tab2:
    st.plotly_chart(fig, theme=None)


st.markdown("* Scatter Plot")
x = st.selectbox(
    "Please Select First attribute",
    ("total", "hp", "attack","defense","sp_attack","sp_defense","speed"))
y = st.selectbox(
    "Please Select Second attribute",
    ("total", "hp", "attack","defense","sp_attack","sp_defense","speed"))
fig = px.scatter(
    df_show,
    x=x,
    y=y
)
event = st.plotly_chart(fig, key="df_show", on_select="rerun")
event