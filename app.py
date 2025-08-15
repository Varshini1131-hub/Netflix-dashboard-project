import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------
# Title and Description
# -------------------
st.set_page_config(page_title="Netflix Data Dashboard", layout="wide")
st.title("🎬 Netflix Data Analysis Dashboard")
st.markdown("Explore trends and patterns in Netflix movies and TV shows.")

# -------------------
# Load Data
# -------------------
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df['date_added'] = pd.to_datetime(df['date_added'],errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month
    return df

df = load_data()

# -------------------
# Sidebar Filters
# -------------------
st.sidebar.header("Filter Options")
type_filter = st.sidebar.multiselect("Select Type", options=df['type'].unique(), default=df['type'].unique())
country_filter = st.sidebar.multiselect("Select Country", options=df['country'].dropna().unique(), default=["United States"])
year_filter = st.sidebar.slider("Select Release Year", int(df['release_year'].min()), int(df['release_year'].max()), (2010, 2020))

# Apply filters
filtered_df = df[
    (df['type'].isin(type_filter)) &
    (df['country'].isin(country_filter)) &
    (df['release_year'] >= year_filter[0]) &
    (df['release_year'] <= year_filter[1])
]

# -------------------
# KPIs
# -------------------
total_titles = len(filtered_df)
movies_count = len(filtered_df[filtered_df['type'] == 'Movie'])
shows_count = len(filtered_df[filtered_df['type'] == 'TV Show'])

col1, col2, col3 = st.columns(3)
col1.metric("Total Titles", total_titles)
col2.metric("Movies", movies_count)
col3.metric("TV Shows", shows_count)

# -------------------
# Charts
# -------------------
st.subheader("Number of Titles Over the Years")
titles_by_year = filtered_df.groupby('release_year').size().reset_index(name='count')
fig_year = px.line(titles_by_year, x='release_year', y='count', markers=True, title="Titles Added Over the Years")
st.plotly_chart(fig_year, use_container_width=True)

st.subheader("Top 10 Countries by Titles")
top_countries = filtered_df['country'].value_counts().head(10).reset_index()
top_countries.columns = ['country', 'count']
fig_country = px.bar(top_countries, x='country', y='count', title="Top Countries by Number of Titles", text='count')
st.plotly_chart(fig_country, use_container_width=True)

st.subheader("Distribution by Rating")
fig_rating = px.histogram(filtered_df, x="rating", title="Ratings Distribution")
st.plotly_chart(fig_rating, use_container_width=True)

st.subheader("Movies vs TV Shows")
fig_type = px.pie(filtered_df, names="type", title="Content Type Distribution")
st.plotly_chart(fig_type, use_container_width=True)

# -------------------
# Show Data Table
# -------------------
st.subheader("Filtered Data Table")
st.dataframe(filtered_df)

st.markdown("📌 **Dashboard created with Streamlit**")


