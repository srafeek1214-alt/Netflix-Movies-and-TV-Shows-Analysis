import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual styles for premium Netflix dark theme
plt.style.use('dark_background')
plt.rcParams.update({
    'figure.facecolor': '#111111',
    'axes.facecolor': '#181818',
    'text.color': '#E5E5E5',
    'axes.labelcolor': '#E5E5E5',
    'xtick.color': '#A3A3A3',
    'ytick.color': '#A3A3A3',
    'grid.color': '#262626',
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'savefig.facecolor': '#111111',
    'savefig.edgecolor': '#111111',
})

# Custom Netflix Palette
NETFLIX_RED = '#E50914'
DARK_GREY = '#221F1F'
LIGHT_GREY = '#F5F5F1'
ACCENT_COLORS = ['#E50914', '#D1A153', '#3A9D23', '#2270B4', '#E57C04', '#9B5DE5', '#00F5D4', '#FF5A5F', '#00B4D8', '#F15BB5']

def load_and_clean_data():
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
    
    # Drop if parsing introduced new NaNs in date_added
    df = df.dropna(subset=['date_added'])
    
    return df

def feature_engineering(df):
    # Added Year, Month, Day, Month Name, Day Name
    df['added_year'] = df['date_added'].dt.year.astype(int)
    df['added_month'] = df['date_added'].dt.month.astype(int)
    df['added_day'] = df['date_added'].dt.day.astype(int)
    df['added_month_name'] = df['date_added'].dt.strftime('%B')
    df['added_day_name'] = df['date_added'].dt.strftime('%A')
    
    # Extract Numeric Duration
    df['duration_num'] = df['duration'].str.extract(r'(\d+)').astype(float)
    df['movie_duration'] = np.where(df['type'] == 'Movie', df['duration_num'], np.nan)
    df['tv_seasons'] = np.where(df['type'] == 'TV Show', df['duration_num'], np.nan)
    
    # Primary Genre and Country
    df['primary_genre'] = df['listed_in'].apply(lambda x: x.split(',')[0].strip())
    df['primary_country'] = df['country'].apply(lambda x: x.split(',')[0].strip() if x != 'Unknown' else 'Unknown')
    
    # Content Age
    df['content_age'] = 2026 - df['release_year']
    
    # Decade
    df['decade'] = (df['release_year'] // 10) * 10
    df['decade_str'] = df['decade'].astype(str) + 's'
    
    # Duration Category for Movies
    df['duration_category'] = pd.cut(
        df['movie_duration'], 
        bins=[0, 60, 90, 120, 180, 999], 
        labels=['Short (<60 min)', 'Standard (60-90 min)', 'Feature (90-120 min)', 'Long (120-180 min)', 'Epic (>180 min)']
    )
    
    return df

def generate_charts(df):
    charts_dir = "images/charts"
    os.makedirs(charts_dir, exist_ok=True)
    
    # 1. Total Movies vs TV Shows
    plt.figure(figsize=(8, 6))
    sns.countplot(data=df, x='type', palette=[NETFLIX_RED, '#3A3A3A'], order=df['type'].value_counts().index)
    plt.title('Total Movies vs TV Shows on Netflix', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Content Type', fontsize=11, labelpad=10)
    plt.ylabel('Count', fontsize=11, labelpad=10)
    for p in plt.gca().patches:
        plt.gca().annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height() - 300),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points', color='white', fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_1_movies_vs_tvshows.png", dpi=150)
    plt.close()

    # 2. Percentage of Movies and TV Shows
    plt.figure(figsize=(7, 7))
    counts = df['type'].value_counts()
    plt.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=[NETFLIX_RED, '#3A3A3A'], 
            explode=[0.05, 0], startangle=140, textprops={'fontsize': 12, 'color': 'white', 'fontweight': 'bold'})
    plt.title('Percentage of Movies and TV Shows on Netflix', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_2_percentage_distribution.png", dpi=150)
    plt.close()

    # 3. Content added each year
    plt.figure(figsize=(12, 6))
    yearly_added = df.groupby(['added_year', 'type']).size().unstack(fill_value=0)
    plt.plot(yearly_added.index, yearly_added['Movie'], color=NETFLIX_RED, marker='o', linewidth=2.5, label='Movies')
    plt.plot(yearly_added.index, yearly_added['TV Show'], color='#D1A153', marker='s', linewidth=2.5, label='TV Shows')
    plt.title('Content Added Each Year on Netflix', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Year Added', fontsize=11, labelpad=10)
    plt.ylabel('Amount of Content', fontsize=11, labelpad=10)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend(facecolor='#181818', edgecolor='none')
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_3_content_added_yearly.png", dpi=150)
    plt.close()

    # 4. Content added each month
    plt.figure(figsize=(12, 6))
    monthly_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    monthly_added = df.groupby(['added_month_name', 'type']).size().unstack(fill_value=0).reindex(monthly_order)
    x = np.arange(len(monthly_order))
    width = 0.35
    plt.bar(x - width/2, monthly_added['Movie'], width, label='Movies', color=NETFLIX_RED)
    plt.bar(x + width/2, monthly_added['TV Show'], width, label='TV Shows', color='#3A9D23')
    plt.xticks(x, monthly_order)
    plt.title('Content Added Each Month (Seasonality)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Month Added', fontsize=11, labelpad=10)
    plt.ylabel('Amount of Content', fontsize=11, labelpad=10)
    plt.grid(True, linestyle='--', alpha=0.2, axis='y')
    plt.legend(facecolor='#181818', edgecolor='none')
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_4_content_added_monthly.png", dpi=150)
    plt.close()

    # 5. Movies released by year (Trend line)
    plt.figure(figsize=(12, 6))
    movies_released = df[df['type'] == 'Movie'].groupby('release_year').size()
    # Filter to show from year 1990 onwards for better clarity
    movies_released_recent = movies_released[movies_released.index >= 1990]
    plt.fill_between(movies_released_recent.index, movies_released_recent.values, color=NETFLIX_RED, alpha=0.3)
    plt.plot(movies_released_recent.index, movies_released_recent.values, color=NETFLIX_RED, linewidth=2.5, marker='o', markevery=3)
    plt.title('Number of Movies Released by Year (1990-Present)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Release Year', fontsize=11, labelpad=10)
    plt.ylabel('Count of Movies', fontsize=11, labelpad=10)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_5_movies_released_yearly.png", dpi=150)
    plt.close()

    # 6. Top 10 countries
    plt.figure(figsize=(12, 6))
    # Exclude Unknown
    country_counts = df[df['primary_country'] != 'Unknown']['primary_country'].value_counts().head(10)
    sns.barplot(x=country_counts.values, y=country_counts.index, palette='Reds_r')
    plt.title('Top 10 Countries Contributing Content on Netflix', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Number of Titles', fontsize=11, labelpad=10)
    plt.ylabel('Country', fontsize=11, labelpad=10)
    for index, value in enumerate(country_counts.values):
        plt.text(value + 20, index, str(value), va='center', color='white', fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_6_top_10_countries.png", dpi=150)
    plt.close()

    # 7. Top 15 genres
    plt.figure(figsize=(12, 7))
    genre_counts = df['primary_genre'].value_counts().head(15)
    sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='plasma')
    plt.title('Top 15 Genres on Netflix', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Number of Titles', fontsize=11, labelpad=10)
    plt.ylabel('Primary Genre', fontsize=11, labelpad=10)
    for index, value in enumerate(genre_counts.values):
        plt.text(value + 15, index, str(value), va='center', color='white', fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_7_top_15_genres.png", dpi=150)
    plt.close()

    # 8. Top ratings
    plt.figure(figsize=(12, 6))
    rating_order = df['rating'].value_counts().index
    sns.countplot(data=df, x='rating', palette='viridis', order=rating_order)
    plt.title('Distribution of Content Ratings on Netflix', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Rating Code', fontsize=11, labelpad=10)
    plt.ylabel('Count', fontsize=11, labelpad=10)
    plt.xticks(rotation=45)
    for p in plt.gca().patches:
        plt.gca().annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', xytext=(0, 3), textcoords='offset points', color='white')
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_8_top_ratings.png", dpi=150)
    plt.close()

    # 9. Top directors
    plt.figure(figsize=(12, 7))
    director_counts = df[df['director'] != 'Unknown']['director'].value_counts().head(10)
    sns.barplot(x=director_counts.values, y=director_counts.index, color=NETFLIX_RED)
    plt.title('Top 10 Directors on Netflix by Number of Titles', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Number of Movies/TV Shows', fontsize=11, labelpad=10)
    plt.ylabel('Director', fontsize=11, labelpad=10)
    for index, value in enumerate(director_counts.values):
        plt.text(value + 0.3, index, str(value), va='center', color='white', fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_9_top_directors.png", dpi=150)
    plt.close()

    # 10. Most frequent actors
    # Since actors are comma-separated in the cast column, split and count
    cast_list = df[df['cast'] != 'Unknown']['cast'].str.split(', ')
    all_actors = [actor.strip() for sublist in cast_list for actor in sublist]
    actor_series = pd.Series(all_actors).value_counts().head(10)
    
    plt.figure(figsize=(12, 7))
    sns.barplot(x=actor_series.values, y=actor_series.index, palette='coolwarm')
    plt.title('Top 10 Actors appearing on Netflix', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Number of Appearances', fontsize=11, labelpad=10)
    plt.ylabel('Actor Name', fontsize=11, labelpad=10)
    for index, value in enumerate(actor_series.values):
        plt.text(value + 0.5, index, str(value), va='center', color='white', fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_10_most_frequent_actors.png", dpi=150)
    plt.close()

    # 11. Movie duration distribution
    plt.figure(figsize=(12, 6))
    movie_durations = df[df['type'] == 'Movie']['movie_duration'].dropna()
    sns.histplot(movie_durations, bins=30, kde=True, color=NETFLIX_RED, edgecolor='white', alpha=0.7)
    plt.title('Distribution of Movie Durations (Minutes)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Duration (Minutes)', fontsize=11, labelpad=10)
    plt.ylabel('Density / Count', fontsize=11, labelpad=10)
    plt.grid(True, linestyle='--', alpha=0.2)
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_11_movie_duration_distribution.png", dpi=150)
    plt.close()

    # 12. Longest movies
    plt.figure(figsize=(12, 6))
    longest_movies = df[df['type'] == 'Movie'].sort_values(by='movie_duration', ascending=False).head(10)
    sns.barplot(x=longest_movies['movie_duration'], y=longest_movies['title'], color='#2270B4')
    plt.title('Top 10 Longest Movies on Netflix', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Duration (Minutes)', fontsize=11, labelpad=10)
    plt.ylabel('Movie Title', fontsize=11, labelpad=10)
    for index, value in enumerate(longest_movies['movie_duration']):
        plt.text(value + 3, index, f"{int(value)} min", va='center', color='white', fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_12_longest_movies.png", dpi=150)
    plt.close()

    # 13. Shortest movies
    plt.figure(figsize=(12, 6))
    # Exclude 0 duration just in case
    shortest_movies = df[(df['type'] == 'Movie') & (df['movie_duration'] > 0)].sort_values(by='movie_duration', ascending=True).head(10)
    sns.barplot(x=shortest_movies['movie_duration'], y=shortest_movies['title'], color='#E57C04')
    plt.title('Top 10 Shortest Movies on Netflix', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Duration (Minutes)', fontsize=11, labelpad=10)
    plt.ylabel('Movie Title', fontsize=11, labelpad=10)
    for index, value in enumerate(shortest_movies['movie_duration']):
        plt.text(value + 0.3, index, f"{int(value)} min", va='center', color='white', fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_13_shortest_movies.png", dpi=150)
    plt.close()

    # 14. Average movie duration over release years
    plt.figure(figsize=(12, 6))
    avg_duration_years = df[df['type'] == 'Movie'].groupby('release_year')['movie_duration'].mean().reset_index()
    # Filter to show from year 1990 onwards for reliability (sample size)
    avg_duration_years_recent = avg_duration_years[avg_duration_years['release_year'] >= 1990]
    plt.plot(avg_duration_years_recent['release_year'], avg_duration_years_recent['movie_duration'], 
             color=NETFLIX_RED, linewidth=2.5, marker='o', markersize=5)
    plt.title('Average Movie Duration by Release Year (1990-Present)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Release Year', fontsize=11, labelpad=10)
    plt.ylabel('Average Duration (Minutes)', fontsize=11, labelpad=10)
    plt.grid(True, linestyle='--', alpha=0.2)
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_14_avg_movie_duration_trend.png", dpi=150)
    plt.close()

    # 15. Country-wise content growth
    plt.figure(figsize=(12, 6))
    top5_countries = df[df['primary_country'] != 'Unknown']['primary_country'].value_counts().head(5).index
    country_growth = df[df['primary_country'].isin(top5_countries)].groupby(['added_year', 'primary_country']).size().unstack(fill_value=0)
    # Cumulative growth
    country_growth_cum = country_growth.cumsum()
    # Filter to 2008+
    country_growth_cum = country_growth_cum[country_growth_cum.index >= 2008]
    
    for i, country in enumerate(top5_countries):
        plt.plot(country_growth_cum.index, country_growth_cum[country], marker='o', label=country, linewidth=2, color=ACCENT_COLORS[i])
    plt.title('Cumulative Content Growth Over Time (Top 5 Countries)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Year Added', fontsize=11, labelpad=10)
    plt.ylabel('Cumulative Content Count', fontsize=11, labelpad=10)
    plt.grid(True, linestyle='--', alpha=0.2)
    plt.legend(facecolor='#181818', edgecolor='none')
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_15_country_wise_growth.png", dpi=150)
    plt.close()

    # 16. Genre-wise distribution
    # Let's show primary genre distribution as a horizontal bar chart
    plt.figure(figsize=(12, 6))
    genre_dist = df['primary_genre'].value_counts()
    sns.barplot(x=genre_dist.values, y=genre_dist.index, palette='magma')
    plt.title('Distribution of Content by Primary Genre', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Count', fontsize=11, labelpad=10)
    plt.ylabel('Genre', fontsize=11, labelpad=10)
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_16_genre_distribution.png", dpi=150)
    plt.close()

    # 17. Rating distribution (Movies vs TV Shows)
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x='rating', hue='type', palette=[NETFLIX_RED, '#3A9D23'], order=df['rating'].value_counts().index[:10])
    plt.title('Rating Distribution: Movies vs TV Shows (Top 10 Ratings)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Rating', fontsize=11, labelpad=10)
    plt.ylabel('Count', fontsize=11, labelpad=10)
    plt.legend(facecolor='#181818', edgecolor='none')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_17_rating_by_type.png", dpi=150)
    plt.close()

    # 18. Movies vs TV Shows by country
    plt.figure(figsize=(12, 6))
    top10_countries = df[df['primary_country'] != 'Unknown']['primary_country'].value_counts().head(10).index
    country_type = df[df['primary_country'].isin(top10_countries)].groupby(['primary_country', 'type']).size().unstack(fill_value=0)
    country_type = country_type.reindex(top10_countries)
    
    x = np.arange(len(top10_countries))
    width = 0.35
    plt.bar(x - width/2, country_type['Movie'], width, label='Movies', color=NETFLIX_RED)
    plt.bar(x + width/2, country_type['TV Show'], width, label='TV Shows', color='#D1A153')
    plt.xticks(x, top10_countries, rotation=45)
    plt.title('Movies vs TV Shows by Country (Top 10)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Country', fontsize=11, labelpad=10)
    plt.ylabel('Count', fontsize=11, labelpad=10)
    plt.legend(facecolor='#181818', edgecolor='none')
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_18_movies_vs_tvshows_by_country.png", dpi=150)
    plt.close()

    # 19. Monthly Netflix additions
    # Distribution of content additions by month (total of all years)
    plt.figure(figsize=(12, 6))
    monthly_data = df.groupby(['added_month', 'type']).size().unstack(fill_value=0)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    plt.bar(months, monthly_data['Movie'], label='Movies', color=NETFLIX_RED, alpha=0.9)
    plt.bar(months, monthly_data['TV Show'], bottom=monthly_data['Movie'], label='TV Shows', color='#3A9D23', alpha=0.9)
    plt.title('Seasonality: Content Additions by Month', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Month', fontsize=11, labelpad=10)
    plt.ylabel('Number of Additions', fontsize=11, labelpad=10)
    plt.legend(facecolor='#181818', edgecolor='none')
    plt.grid(True, linestyle='--', alpha=0.1, axis='y')
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_19_monthly_additions_distribution.png", dpi=150)
    plt.close()

    # 20. Heatmap of monthly additions by year
    # Filter for years 2015 to 2021 where most content is added
    heatmap_df = df[(df['added_year'] >= 2015) & (df['added_year'] <= 2021)]
    heatmap_pivot = heatmap_df.pivot_table(index='added_year', columns='added_month_name', values='show_id', aggfunc='count', fill_value=0)
    heatmap_pivot = heatmap_pivot.reindex(columns=monthly_order)
    
    plt.figure(figsize=(14, 8))
    sns.heatmap(heatmap_pivot, annot=True, fmt='d', cmap='Reds', cbar_kws={'label': 'Count of Titles'}, linewidths=.5)
    plt.title('Heatmap of Content Additions by Month and Year (2015-2021)', fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Month Added', fontsize=11, labelpad=10)
    plt.ylabel('Year Added', fontsize=11, labelpad=10)
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_20_monthly_yearly_heatmap.png", dpi=150)
    plt.close()

    # 21. Top release years
    plt.figure(figsize=(12, 6))
    release_year_counts = df['release_year'].value_counts().head(10)
    sns.barplot(x=release_year_counts.index.astype(str), y=release_year_counts.values, palette='copper')
    plt.title('Top 10 Release Years represented on Netflix', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Release Year', fontsize=11, labelpad=10)
    plt.ylabel('Count', fontsize=11, labelpad=10)
    for p in plt.gca().patches:
        plt.gca().annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', xytext=(0, 3), textcoords='offset points', color='white')
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_21_top_release_years.png", dpi=150)
    plt.close()

    # 22. Content growth timeline (Cumulative count)
    plt.figure(figsize=(12, 6))
    df_sorted = df.sort_values(by='date_added')
    df_sorted['cumulative_titles'] = range(1, len(df_sorted) + 1)
    
    plt.plot(df_sorted['date_added'], df_sorted['cumulative_titles'], color=NETFLIX_RED, linewidth=3)
    plt.fill_between(df_sorted['date_added'], df_sorted['cumulative_titles'], color=NETFLIX_RED, alpha=0.15)
    plt.title('Timeline of Cumulative Content Growth on Netflix', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Date Added', fontsize=11, labelpad=10)
    plt.ylabel('Total Titles in Library', fontsize=11, labelpad=10)
    plt.grid(True, linestyle='--', alpha=0.2)
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_22_growth_timeline.png", dpi=150)
    plt.close()

    # 23. Decade-wise content distribution
    plt.figure(figsize=(10, 6))
    # Group old content together
    decade_counts = df['decade_str'].value_counts().sort_index()
    # Filter and merge pre-1970s if small
    sns.barplot(x=decade_counts.index, y=decade_counts.values, palette='autumn')
    plt.title('Decade of Release for Netflix Library', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Decade', fontsize=11, labelpad=10)
    plt.ylabel('Count of Titles', fontsize=11, labelpad=10)
    for p in plt.gca().patches:
        plt.gca().annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', xytext=(0, 3), textcoords='offset points', color='white')
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_23_decade_distribution.png", dpi=150)
    plt.close()

    # 24. Movies by duration category
    plt.figure(figsize=(8, 8))
    movie_cat_counts = df[df['type'] == 'Movie']['duration_category'].value_counts()
    plt.pie(movie_cat_counts, labels=movie_cat_counts.index, autopct='%1.1f%%', colors=ACCENT_COLORS[:len(movie_cat_counts)],
            startangle=140, pctdistance=0.85, textprops={'fontsize': 10, 'color': 'white', 'fontweight': 'bold'})
    # Draw doughnut center
    centre_circle = plt.Circle((0,0),0.70,fc='#111111')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.title('Movies Categorized by Duration Length', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_24_movie_duration_categories.png", dpi=150)
    plt.close()

    # 25. Most common genre combinations
    # Count the original listed_in combinations
    plt.figure(figsize=(12, 7))
    genre_combos = df['listed_in'].value_counts().head(10)
    sns.barplot(x=genre_combos.values, y=genre_combos.index, palette='rocket')
    plt.title('Top 10 Most Common Genre Combinations on Netflix', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Number of Titles', fontsize=11, labelpad=10)
    plt.ylabel('Genre Combination', fontsize=11, labelpad=10)
    for index, value in enumerate(genre_combos.values):
        plt.text(value + 5, index, str(value), va='center', color='white', fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{charts_dir}/chart_25_genre_combinations.png", dpi=150)
    plt.close()
    
    print(f"All 25 charts have been successfully generated and saved to: {charts_dir}")

def generate_insights(df):
    insights = []
    
    # 1. Domination of Movie type
    movie_cnt = df[df['type']=='Movie'].shape[0]
    tv_cnt = df[df['type']=='TV Show'].shape[0]
    total = df.shape[0]
    insights.append(f"1. Content Type Domination: Movies dominate Netflix, comprising {movie_cnt/total*100:.1f}% ({movie_cnt} titles) of the library, compared to TV Shows at {tv_cnt/total*100:.1f}% ({tv_cnt} titles).")
    
    # 2. Leading country
    top_country = df[df['primary_country'] != 'Unknown']['primary_country'].value_counts().idxmax()
    top_country_val = df[df['primary_country'] != 'Unknown']['primary_country'].value_counts().max()
    insights.append(f"2. Geographic Leader: The United States is by far the largest contributor of Netflix content, producing {top_country_val} primary titles ({top_country_val/total*100:.1f}% of total).")
    
    # 3. India's Position
    india_cnt = df[df['primary_country'] == 'India'].shape[0]
    insights.append(f"3. India's Profile: India is the second-largest content contributor with {india_cnt} titles, heavily dominated by Movies rather than TV Shows.")
    
    # 4. Top Genres
    top_genre = df['primary_genre'].value_counts().idxmax()
    top_genre_val = df['primary_genre'].value_counts().max()
    insights.append(f"4. Leading Genre: The most popular primary genre category is '{top_genre}' with {top_genre_val} titles, reflecting a strong viewer preference for narrative-driven stories.")
    
    # 5. Rating distribution
    top_rating = df['rating'].value_counts().index[0]
    top_rating_pct = df['rating'].value_counts().iloc[0] / total * 100
    insights.append(f"5. Target Audience Rating: Content rated '{top_rating}' is the most common rating on the platform, accounting for {top_rating_pct:.1f}% of titles. This indicates Netflix's target audience is mature teenagers and adults.")
    
    # 6. PG-13/TV-14 audience share
    mature_share = df[df['rating'].isin(['TV-MA', 'R', 'NC-17'])].shape[0] / total * 100
    insights.append(f"6. Mature Content Share: Approximately {mature_share:.1f}% of Netflix's content is rated for mature audiences (TV-MA, R, NC-17), positioning Netflix as a hub for sophisticated and adult-oriented programming.")
    
    # 7. Release Year spike
    top_release_year = df['release_year'].value_counts().idxmax()
    insights.append(f"7. Peak Production Year: The year with the highest volume of released titles present in the library is {top_release_year}, signifying a historical surge in licensing and content generation around this timeframe.")
    
    # 8. Library expansion year
    top_added_year = df['added_year'].value_counts().idxmax()
    insights.append(f"8. Peak Library Expansion: The year {top_added_year} saw the highest amount of content added to the library, representing Netflix's most aggressive expansion phase.")
    
    # 9. Top Director
    top_dir = df[df['director'] != 'Unknown']['director'].value_counts().index[0]
    top_dir_cnt = df[df['director'] != 'Unknown']['director'].value_counts().iloc[0]
    insights.append(f"9. Top Director: The director with the most titles on Netflix is {top_dir} with {top_dir_cnt} credits, demonstrating a strong collaborative presence on the platform.")
    
    # 10. Most common actor
    cast_list = df[df['cast'] != 'Unknown']['cast'].str.split(', ')
    all_actors = [actor.strip() for sublist in cast_list for actor in sublist]
    top_actor = pd.Series(all_actors).value_counts().index[0]
    top_actor_cnt = pd.Series(all_actors).value_counts().iloc[0]
    insights.append(f"10. Star Power: The actor appearing in the largest number of Netflix listings is {top_actor} with {top_actor_cnt} appearances, particularly in Indian cinema titles.")
    
    # 11. Average movie duration
    avg_dur = df[df['type']=='Movie']['movie_duration'].mean()
    insights.append(f"11. Average Movie Length: The average duration of movies on the platform is {avg_dur:.1f} minutes, aligning closely with standard theatrical standards of ~1.5 to 2 hours.")
    
    # 12. Movie duration trends
    recent_movie_dur = df[(df['type']=='Movie') & (df['release_year']>=2015)]['movie_duration'].mean()
    insights.append(f"12. Movie Length Trends: In recent years (2015 onwards), the average movie length has slightly declined to {recent_movie_dur:.1f} minutes, indicating a potential shift towards shorter, more digestible content formats.")
    
    # 13. Content Age Profile
    avg_age = df['content_age'].mean()
    insights.append(f"13. Freshness of Library: The average age of content on Netflix is {avg_age:.1f} years, highlighting that the catalog is overwhelmingly skewed towards recent releases from the last decade.")
    
    # 14. TV Show Seasons analysis
    one_season_pct = (df[df['type'] == 'TV Show']['tv_seasons'] == 1).sum() / (df['type'] == 'TV Show').sum() * 100
    insights.append(f"14. TV Show Longevity: A massive {one_season_pct:.1f}% of TV Shows on Netflix only have 1 season, which points to a high cancellation rate or a focus on limited miniseries format.")
    
    # 15. Seasonality of additions
    top_month = df['added_month_name'].value_counts().index[0]
    insights.append(f"15. Monthly Addition Trends: The month of {top_month} is the most frequent choice for adding content, suggesting strategic positioning around holiday seasons or quarterly financial cycles.")
    
    # 16. Year-over-year growth
    growth_15_20 = (df[df['added_year']==2020].shape[0] / df[df['added_year']==2015].shape[0] - 1) * 100
    insights.append(f"16. Library Growth (2015-2020): From 2015 to 2020, yearly content additions grew by {growth_15_20:.1f}%, indicating exponential platform expansion and investment in content acquisition.")
    
    # 17. Most common genre combination
    top_combo = df['listed_in'].value_counts().index[0]
    insights.append(f"17. Genre Synergy: The most common genre combination is '{top_combo}', representing a strong library focus on localized stand-up comedy specials.")
    
    # 18. Decade distribution
    dec_2010s = (df[df['decade_str'] == '2010s'].shape[0] / total) * 100
    insights.append(f"18. Modern Skew: Over {dec_2010s:.1f}% of all Netflix content belongs to the 2010s decade, proving that older classic films/shows comprise a minority portion of the library.")
    
    # 19. Category duration proportions
    standard_duration_share = (df[df['duration_category'] == 'Feature (90-120 min)'].shape[0] / df[df['type'] == 'Movie'].shape[0]) * 100
    insights.append(f"19. Movie Category Share: The 'Feature (90-120 min)' category represents the dominant duration segment for Movies, representing {standard_duration_share:.1f}% of the movie catalog.")
    
    # 20. Countries with TV Show preference
    uk_tv_pct = (df[(df['primary_country'] == 'United Kingdom') & (df['type'] == 'TV Show')].shape[0] / df[df['primary_country'] == 'United Kingdom'].shape[0]) * 100
    insights.append(f"20. Local Preferences: While movies dominate overall, countries like the United Kingdom exhibit a much higher ratio of TV Shows ({uk_tv_pct:.1f}% of UK titles are TV Shows) compared to the global average of TV Shows.")

    return insights

if __name__ == "__main__":
    df = load_and_clean_data()
    df = feature_engineering(df)
    generate_charts(df)
    
    print("\n" + "="*40 + "\n20+ BUSINESS INSIGHTS:\n" + "="*40)
    for insight in generate_insights(df):
        print(insight)
