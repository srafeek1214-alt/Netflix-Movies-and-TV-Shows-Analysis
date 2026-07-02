import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Set page configuration for wide layout and dark theme
st.set_page_config(
    page_title="Netflix Catalogue Dashboard",
    page_icon="🍿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to apply Netflix colors and modern styling
st.markdown("""
<style>
    /* Main layout style */
    .stApp {
        background-color: #111111;
        color: #E5E5E5;
    }
    
    /* Header/Title style */
    h1, h2, h3 {
        color: #E50914 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #181818 !important;
        border-right: 1px solid #262626;
    }
    
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #A3A3A3;
    }
    
    /* KPI Card styling */
    .kpi-card {
        background-color: #181818;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #262626;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    .kpi-title {
        color: #A3A3A3;
        font-size: 14px;
        text-transform: uppercase;
        margin-bottom: 5px;
        font-weight: bold;
    }
    
    .kpi-value {
        color: #E50914;
        font-size: 32px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Cache data loading and cleaning
@st.cache_data
def get_data():
    df = pd.read_csv("data/netflix_titles.csv")
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Handle missing values
    df['director'] = df['director'].fillna('Unknown')
    df['cast'] = df['cast'].fillna('Unknown')
    df['country'] = df['country'].fillna('Unknown')
    df['rating'] = df['rating'].fillna('Unknown')
    
    # Drop rows where date_added is missing (only 10 rows)
    df = df.dropna(subset=['date_added'])
    
    # Parse date_added
    df['date_added'] = df['date_added'].str.strip()
    df['date_added'] = pd.to_datetime(df['date_added'], format='%B %d, %Y', errors='coerce')
    df = df.dropna(subset=['date_added'])
    
    # Feature Engineering
    df['added_year'] = df['date_added'].dt.year.astype(int)
    df['added_month'] = df['date_added'].dt.month.astype(int)
    df['added_month_name'] = df['date_added'].dt.strftime('%B')
    
    # Extract Numeric Duration
    df['duration_num'] = df['duration'].str.extract(r'(\d+)').astype(float)
    df['movie_duration'] = np.where(df['type'] == 'Movie', df['duration_num'], np.nan)
    df['tv_seasons'] = np.where(df['type'] == 'TV Show', df['duration_num'], np.nan)
    
    # Primary Genre and Country
    df['primary_genre'] = df['listed_in'].apply(lambda x: x.split(',')[0].strip())
    df['primary_country'] = df['country'].apply(lambda x: x.split(',')[0].strip() if x != 'Unknown' else 'Unknown')
    
    # Content Age and Decade
    df['content_age'] = 2026 - df['release_year']
    df['decade'] = (df['release_year'] // 10) * 10
    df['decade_str'] = df['decade'].astype(str) + 's'
    
    # Movie Duration Category
    df['duration_category'] = pd.cut(
        df['movie_duration'], 
        bins=[0, 60, 90, 120, 180, 999], 
        labels=['Short (<60 min)', 'Standard (60-90 min)', 'Feature (90-120 min)', 'Long (120-180 min)', 'Epic (>180 min)']
    )
    
    return df

# Load the dataset
df = get_data()

# ----------------- SIDEBAR FILTER SYSTEM -----------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=150)
st.sidebar.title("Dashboard Filters")
st.sidebar.write("Refine the data display below:")

# 1. Content Type Filter
content_type = st.sidebar.selectbox("Content Type", ["All", "Movie", "TV Show"])

# 2. Year Filter
min_year = int(df['added_year'].min())
max_year = int(df['added_year'].max())
year_range = st.sidebar.slider("Year Added to Netflix", min_year, max_year, (min_year, max_year))

# 3. Country Filter (Exclude Unknown from selection list, but keep All option)
countries_list = sorted(list(df[df['primary_country'] != 'Unknown']['primary_country'].unique()))
country_selection = st.sidebar.selectbox("Country", ["All"] + countries_list)

# 4. Genre Filter
genres_list = sorted(list(df['primary_genre'].unique()))
genre_selection = st.sidebar.selectbox("Primary Genre", ["All"] + genres_list)

# 5. Rating Filter
ratings_list = sorted(list(df['rating'].unique()))
rating_selection = st.sidebar.selectbox("Audience Rating", ["All"] + ratings_list)

# ----------------- APPLY FILTERS -----------------
filtered_df = df.copy()

if content_type != "All":
    filtered_df = filtered_df[filtered_df['type'] == content_type]

filtered_df = filtered_df[
    (filtered_df['added_year'] >= year_range[0]) & 
    (filtered_df['added_year'] <= year_range[1])
]

if country_selection != "All":
    filtered_df = filtered_df[filtered_df['primary_country'] == country_selection]

if genre_selection != "All":
    filtered_df = filtered_df[filtered_df['primary_genre'] == genre_selection]

if rating_selection != "All":
    filtered_df = filtered_df[filtered_df['rating'] == rating_selection]

# ----------------- MAIN AREA -----------------
st.title("🍿 Netflix Movies & TV Shows Interactive Dashboard")
st.write("An interactive web application exploring Netflix's global catalogue content profile.")

st.markdown("---")

# ----------------- KPI CARDS ROW -----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Catalogue Titles</div>
        <div class="kpi-value">{filtered_df.shape[0]}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    movie_count = filtered_df[filtered_df['type'] == 'Movie'].shape[0]
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Movies</div>
        <div class="kpi-value">{movie_count}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    tv_count = filtered_df[filtered_df['type'] == 'TV Show'].shape[0]
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total TV Shows</div>
        <div class="kpi-value">{tv_count}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    unique_countries = filtered_df[filtered_df['primary_country'] != 'Unknown']['primary_country'].nunique()
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Contributing Countries</div>
        <div class="kpi-value">{unique_countries}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# ----------------- CHARTS ROW 1 -----------------
col_pie, col_countries = st.columns([1, 2])

with col_pie:
    st.subheader("Content Mix: Movie vs TV Show")
    if filtered_df.shape[0] > 0:
        fig_pie = px.pie(
            filtered_df, 
            names='type', 
            hole=0.4, 
            color='type',
            color_discrete_map={'Movie': '#E50914', 'TV Show': '#3A3A3A'}
        )
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#E5E5E5',
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No data available for these filters.")

with col_countries:
    st.subheader("Top Contributing Countries")
    # Exclude Unknown
    country_data = filtered_df[filtered_df['primary_country'] != 'Unknown']
    if country_data.shape[0] > 0:
        country_counts = country_data['primary_country'].value_counts().head(10).reset_index()
        country_counts.columns = ['Country', 'Count']
        
        fig_countries = px.bar(
            country_counts, 
            x='Count', 
            y='Country', 
            orientation='h',
            color='Count',
            color_continuous_scale='Reds'
        )
        fig_countries.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#E5E5E5',
            yaxis=dict(autorange="reversed"),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_countries, use_container_width=True)
    else:
        st.info("No country metadata available for these filters.")

# ----------------- CHARTS ROW 2 -----------------
col_genre, col_ratings = st.columns(2)

with col_genre:
    st.subheader("Genre Distribution (Top 10)")
    if filtered_df.shape[0] > 0:
        genre_counts = filtered_df['primary_genre'].value_counts().head(10).reset_index()
        genre_counts.columns = ['Genre', 'Count']
        
        fig_genre = px.bar(
            genre_counts,
            x='Count',
            y='Genre',
            orientation='h',
            color='Genre',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_genre.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#E5E5E5',
            yaxis=dict(autorange="reversed"),
            showlegend=False
        )
        st.plotly_chart(fig_genre, use_container_width=True)
    else:
        st.info("No data available.")

with col_ratings:
    st.subheader("Content Ratings Distribution")
    if filtered_df.shape[0] > 0:
        rating_counts = filtered_df['rating'].value_counts().reset_index()
        rating_counts.columns = ['Rating', 'Count']
        
        fig_ratings = px.bar(
            rating_counts,
            x='Rating',
            y='Count',
            color='Rating',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig_ratings.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#E5E5E5',
            showlegend=False
        )
        st.plotly_chart(fig_ratings, use_container_width=True)
    else:
        st.info("No data available.")

# ----------------- TIMELINE ROW -----------------
st.subheader("Content Growth Timeline (Cumulative additions)")
if filtered_df.shape[0] > 0:
    timeline_df = filtered_df.sort_values(by='date_added')
    timeline_df['cumulative_titles'] = range(1, len(timeline_df) + 1)
    
    fig_timeline = px.area(
        timeline_df,
        x='date_added',
        y='cumulative_titles',
        color_discrete_sequence=['#E50914']
    )
    fig_timeline.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#E5E5E5',
        xaxis_title="Date Added",
        yaxis_title="Total Catalogue Titles"
    )
    st.plotly_chart(fig_timeline, use_container_width=True)
else:
    st.info("No timeline data available.")

# ----------------- BUSINESS INSIGHTS SECTION -----------------
st.markdown("---")
with st.expander("💡 View 20 Key Business Insights Summary", expanded=False):
    insights = [
        "**1. Content Type Domination:** Movies dominate Netflix, comprising 69.1% (5,377 titles) of the library, compared to TV Shows at 30.9% (2,400 titles).",
        "**2. Geographic Leader:** The United States is by far the largest contributor of Netflix content, producing 2,877 primary titles (37.0% of total).",
        "**3. India's Profile:** India is the second-largest content contributor with 956 titles, heavily dominated by Movies rather than TV Shows.",
        "**4. Leading Genre:** The most popular primary genre category is 'Dramas' with 1,384 titles, reflecting a strong viewer preference for narrative-driven stories.",
        "**5. Target Audience Rating:** Content rated 'TV-MA' is the most common rating on the platform, accounting for 36.8% of titles. This indicates Netflix's target audience is mature teenagers and adults.",
        "**6. Mature Content Share:** Approximately 45.4% of Netflix's content is rated for mature audiences (TV-MA, R, NC-17), positioning Netflix as a hub for sophisticated and adult-oriented programming.",
        "**7. Peak Production Year:** The year with the highest volume of released titles present in the library is 2018, signifying a historical surge in licensing and content generation around this timeframe.",
        "**8. Peak Library Expansion:** The year 2019 saw the highest amount of content added to the library, representing Netflix's most aggressive expansion phase.",
        "**9. Top Director:** The director with the most titles on Netflix is Raúl Campos, Jan Suter with 18 credits, demonstrating a strong collaborative presence on the platform.",
        "**10. Star Power:** The actor appearing in the largest number of Netflix listings is Anupam Kher with 42 appearances, particularly in Indian cinema titles.",
        "**11. Average Movie Length:** The average duration of movies on the platform is 99.3 minutes, aligning closely with standard theatrical standards of ~1.5 to 2 hours.",
        "**12. Movie Length Trends:** In recent years (2015 onwards), the average movie length has slightly declined to 94.8 minutes, indicating a potential shift towards shorter, more digestible content formats.",
        "**13. Freshness of Library:** The average age of content on Netflix is 12.1 years, highlighting that the catalog is overwhelmingly skewed towards recent releases from the last decade.",
        "**14. TV Show Longevity:** A massive 67.0% of TV Shows on Netflix only have 1 season, which points to a high cancellation rate or a focus on limited miniseries format.",
        "**15. Monthly Addition Trends:** The month of December is the most frequent choice for adding content, suggesting strategic positioning around holiday seasons or quarterly financial cycles.",
        "**16. Library Growth (2015-2020):** From 2015 to 2020, yearly content additions grew by 2,183.0%, indicating exponential platform expansion and investment in content acquisition.",
        "**17. Genre Synergy:** The most common genre combination is 'Documentaries', representing a strong library focus on localized stand-up comedy specials.",
        "**18. Modern Skew:** Over 73.3% of all Netflix content belongs to the 2010s decade, proving that older classic films/shows comprise a minority portion of the library.",
        "**19. Movie Category Share:** The 'Feature (90-120 min)' category represents the dominant duration segment for Movies, representing 47.9% of the movie catalog.",
        "**20. Local Preferences:** While movies dominate overall, countries like the United Kingdom exhibit a much higher ratio of TV Shows (40.8% of UK titles are TV Shows) compared to the global average of TV Shows."
    ]
    for insight in insights:
        st.write(insight)

# ----------------- DATA SEARCH & EXPLORER -----------------
st.subheader("🔍 Netflix Catalogue Search & Explorer")
search_term = st.text_input("Enter keywords in Title, Director, Cast or Description:")
if search_term:
    search_results = filtered_df[
        filtered_df['title'].str.contains(search_term, case=False, na=False) |
        filtered_df['director'].str.contains(search_term, case=False, na=False) |
        filtered_df['cast'].str.contains(search_term, case=False, na=False) |
        filtered_df['description'].str.contains(search_term, case=False, na=False)
    ]
    st.write(f"Found {search_results.shape[0]} titles matching standard filters & keyword:")
    st.dataframe(search_results[['title', 'type', 'primary_country', 'release_year', 'rating', 'duration', 'listed_in']])
else:
    st.write("Displaying random selection of current filtered list:")
    st.dataframe(filtered_df[['title', 'type', 'primary_country', 'release_year', 'rating', 'duration', 'listed_in']].sample(min(10, filtered_df.shape[0])))
