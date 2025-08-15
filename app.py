import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    return df

df = load_data()

# Title
st.title("📊 Netflix Data Dashboard")

# Sidebar Filters
st.sidebar.header("Filter Options")

country = st.sidebar.selectbox("Select Country", options=["All"] + sorted(df['country'].dropna().unique()))
content_type = st.sidebar.multiselect("Select Type", options=df['type'].unique(), default=df['type'].unique())

# Filter Data
filtered_df = df.copy()
if country != "All":
    filtered_df = filtered_df[filtered_df['country'] == country]
if content_type:
    filtered_df = filtered_df[filtered_df['type'].isin(content_type)]

# Metrics
st.subheader("Dataset Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Titles", len(filtered_df))
col2.metric("Movies", (filtered_df['type'] == "Movie").sum())
col3.metric("TV Shows", (filtered_df['type'] == "TV Show").sum())

# Chart 1: Movies vs TV Shows
type_count = filtered_df['type'].value_counts()
fig1 = px.bar(type_count, x=type_count.index, y=type_count.values, color=type_count.index,
              title="Movies vs TV Shows")
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Content Added Over Time
df_by_year = filtered_df.groupby(filtered_df['date_added'].dt.year).size()
fig2 = px.line(df_by_year, x=df_by_year.index, y=df_by_year.values,
               title="Content Added by Year", markers=True)
st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Top Genres
df['listed_in'] = df['listed_in'].fillna("")
genre_list = []
for genres in filtered_df['listed_in']:
    for g in genres.split(","):
        genre_list.append(g.strip())

genre_df = pd.Series(genre_list).value_counts().head(10).reset_index()
genre_df.columns = ["Genre", "Count"]
fig3 = px.bar(genre_df, x="Genre", y="Count", title="Top 10 Genres")
st.plotly_chart(fig3, use_container_width=True)

# Chart 4: World Map of Netflix Content
st.subheader("🌍 Netflix Titles by Country")
country_count = df['country'].value_counts().reset_index()
country_count.columns = ['Country', 'Count']

fig4 = px.choropleth(
    country_count,
    locations="Country",
    locationmode="country names",
    color="Count",
    color_continuous_scale="Reds",
    title="Number of Netflix Titles per Country"
)
st.plotly_chart(fig4, use_container_width=True)

# Show Table
st.subheader("Filtered Dataset")
st.dataframe(filtered_df)




