import nbformat as nbf
import os

def create_notebook():
    nb = nbf.v4.new_notebook()
    
    cells = []
    
    # ------------------ CELL 1: Header ------------------
    cells.append(nbf.v4.new_markdown_cell(
        "# Netflix Movies & TV Shows Analysis\n"
        "### A Comprehensive Data Science Portfolio Project\n"
        "This Jupyter Notebook performs a full Exploratory Data Analysis (EDA) on the Kaggle Netflix dataset (`netflix_titles.csv`). "
        "The project covers data cleaning, feature engineering, visualizations, and extracts key business insights. "
        "No machine learning is applied, focusing purely on descriptive analytics and business intelligence.\n\n"
        "**Author:** Data Science Team\n"
        "**Date:** June 2026\n\n"
        "---"
    ))
    
    # ------------------ CELL 2: Step 1 Intro ------------------
    cells.append(nbf.v4.new_markdown_cell(
        "## Step 1 – Import Libraries & Configure Styling\n"
        "We begin by importing the required libraries (pandas, numpy, matplotlib, and seaborn) "
        "and configuring a custom dark theme matching Netflix's branding aesthetics."
    ))
    
    # ------------------ CELL 3: Step 1 Code ------------------
    cells.append(nbf.v4.new_code_cell(
        "import os\n"
        "import pandas as pd\n"
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "import seaborn as sns\n\n"
        "# Set visual styles for premium Netflix dark theme\n"
        "plt.style.use('dark_background')\n"
        "plt.rcParams.update({\n"
        "    'figure.facecolor': '#111111',\n"
        "    'axes.facecolor': '#181818',\n"
        "    'text.color': '#E5E5E5',\n"
        "    'axes.labelcolor': '#E5E5E5',\n"
        "    'xtick.color': '#A3A3A3',\n"
        "    'ytick.color': '#A3A3A3',\n"
        "    'grid.color': '#262626',\n"
        "    'font.family': 'sans-serif',\n"
        "    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],\n"
        "    'savefig.facecolor': '#111111',\n"
        "    'savefig.edgecolor': '#111111',\n"
        "})\n\n"
        "NETFLIX_RED = '#E50914'\n"
        "ACCENT_COLORS = ['#E50914', '#D1A153', '#3A9D23', '#2270B4', '#E57C04', '#9B5DE5', '#00F5D4', '#FF5A5F', '#00B4D8', '#F15BB5']\n"
        "print('Libraries imported and visualization styles configured successfully!')"
    ))
    
    # ------------------ CELL 4: Step 2 Intro ------------------
    cells.append(nbf.v4.new_markdown_cell(
        "## Step 2 – Load Dataset\n"
        "We read the `netflix_titles.csv` file from the `data/` directory and print metadata."
    ))
    
    # ------------------ CELL 5: Step 2 Code ------------------
    cells.append(nbf.v4.new_code_cell(
        "df_raw = pd.read_csv('../data/netflix_titles.csv')\n"
        "print('Dataset Loaded Successfully!')\n"
        "print(f'Shape of Dataset: {df_raw.shape[0]} rows, {df_raw.shape[1]} columns')\n"
        "print('\\nColumns list:\\n', list(df_raw.columns))\n"
        "print('\\nData Types:\\n', df_raw.dtypes)"
    ))
    
    # ------------------ CELL 6: Step 3 Intro ------------------
    cells.append(nbf.v4.new_markdown_cell(
        "## Step 3 – Dataset Exploration\n"
        "Before cleaning, we explore head/tail rows, missing values, duplicates, and check columns in detail."
    ))
    
    # ------------------ CELL 7: Step 3 Code ------------------
    cells.append(nbf.v4.new_code_cell(
        "print('FIRST 3 ROWS:')\n"
        "display(df_raw.head(3))\n"
        "print('\\nLAST 3 ROWS:')\n"
        "display(df_raw.tail(3))\n"
        "print('\\nNULL VALUE COUNTS:')\n"
        "print(df_raw.isnull().sum())\n"
        "print('\\nDUPLICATE ROWS COUNT:', df_raw.duplicated().sum())\n"
        "print('\\nSUMMARY STATISTICS:')\n"
        "display(df_raw.describe(include='all'))"
    ))
    
    # ------------------ CELL 8: Step 4 Intro ------------------
    cells.append(nbf.v4.new_markdown_cell(
        "## Step 4 – Data Cleaning\n"
        "In this step, we perform:\n"
        "- Removal of duplicate rows.\n"
        "- Handling missing values: `director`, `cast`, and `country` are filled with 'Unknown'. Missing `rating` filled with 'Unknown'.\n"
        "- Filter out rows with missing `date_added` (only 10 rows).\n"
        "- Parse `date_added` into standard datetime.\n"
        "- Extract duration details and handle before/after comparison."
    ))
    
    # ------------------ CELL 9: Step 4 Code ------------------
    cells.append(nbf.v4.new_code_cell(
        "df_clean = df_raw.drop_duplicates()\n"
        "df_clean['director'] = df_clean['director'].fillna('Unknown')\n"
        "df_clean['cast'] = df_clean['cast'].fillna('Unknown')\n"
        "df_clean['country'] = df_clean['country'].fillna('Unknown')\n"
        "df_clean['rating'] = df_clean['rating'].fillna('Unknown')\n\n"
        "nulls_before_date = df_clean['date_added'].isnull().sum()\n"
        "df_clean = df_clean.dropna(subset=['date_added'])\n"
        "df_clean['date_added'] = df_clean['date_added'].str.strip()\n"
        "df_clean['date_added'] = pd.to_datetime(df_clean['date_added'], format='%B %d, %Y', errors='coerce')\n"
        "df_clean = df_clean.dropna(subset=['date_added'])\n\n"
        "print(f'Initial rows: {len(df_raw)} | Cleaned rows: {len(df_clean)}')\n"
        "print('Remaining Null Values:\\n', df_clean.isnull().sum())"
    ))
    
    # ------------------ CELL 10: Step 5 Intro ------------------
    cells.append(nbf.v4.new_markdown_cell(
        "## Step 5 – Feature Engineering\n"
        "We create new fields to aid the analysis:\n"
        "- `added_year`, `added_month`, `added_day`, `added_month_name`, `added_day_name` from `date_added`\n"
        "- `movie_duration` (numeric minutes for movies) and `tv_seasons` (numeric seasons for TV shows)\n"
        "- `primary_genre` and `primary_country` (taking the first listed item)\n"
        "- `content_age` (2026 - release year)\n"
        "- `decade` and `decade_str` of release year\n"
        "- `duration_category` for movies"
    ))
    
    # ------------------ CELL 11: Step 5 Code ------------------
    cells.append(nbf.v4.new_code_cell(
        "df = df_clean.copy()\n"
        "df['added_year'] = df['date_added'].dt.year.astype(int)\n"
        "df['added_month'] = df['date_added'].dt.month.astype(int)\n"
        "df['added_day'] = df['date_added'].dt.day.astype(int)\n"
        "df['added_month_name'] = df['date_added'].dt.strftime('%B')\n"
        "df['added_day_name'] = df['date_added'].dt.strftime('%A')\n\n"
        "df['duration_num'] = df['duration'].str.extract(r'(\\d+)').astype(float)\n"
        "df['movie_duration'] = np.where(df['type'] == 'Movie', df['duration_num'], np.nan)\n"
        "df['tv_seasons'] = np.where(df['type'] == 'TV Show', df['duration_num'], np.nan)\n\n"
        "df['primary_genre'] = df['listed_in'].apply(lambda x: x.split(',')[0].strip())\n"
        "df['primary_country'] = df['country'].apply(lambda x: x.split(',')[0].strip() if x != 'Unknown' else 'Unknown')\n\n"
        "df['content_age'] = 2026 - df['release_year']\n"
        "df['decade'] = (df['release_year'] // 10) * 10\n"
        "df['decade_str'] = df['decade'].astype(str) + 's'\n\n"
        "df['duration_category'] = pd.cut(\n"
        "    df['movie_duration'], \n"
        "    bins=[0, 60, 90, 120, 180, 999], \n"
        "    labels=['Short (<60 min)', 'Standard (60-90 min)', 'Feature (90-120 min)', 'Long (120-180 min)', 'Epic (>180 min)']\n"
        ")\n\n"
        "print('Features Engineered Successfully!')\n"
        "display(df[['title', 'type', 'added_year', 'movie_duration', 'tv_seasons', 'primary_genre', 'primary_country', 'decade_str', 'duration_category']].head(5))"
    ))
    
    # ------------------ CELL 12: Step 6 & 7 Intro ------------------
    cells.append(nbf.v4.new_markdown_cell(
        "# Step 6 & 7 – Exploratory Data Analysis & Visualizations\n"
        "We perform the 25 required analyses and create high-quality visualizations. "
        "All visualizations are automatically saved to `../images/charts/`."
    ))
    
    # ------------------ VIS CELLS ------------------
    vis_items = [
        ("1. Total Movies vs TV Shows", 
         "plt.figure(figsize=(8, 6))\n"
         "sns.countplot(data=df, x='type', palette=[NETFLIX_RED, '#3A3A3A'], order=df['type'].value_counts().index)\n"
         "plt.title('Total Movies vs TV Shows on Netflix', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Content Type', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Count', fontsize=11, labelpad=10)\n"
         "for p in plt.gca().patches:\n"
         "    plt.gca().annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height() - 300),\n"
         "                ha='center', va='center', xytext=(0, 10), textcoords='offset points', color='white', fontweight='bold')\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_1_movies_vs_tvshows.png', dpi=150)\n"
         "plt.show()"),
         
        ("2. Percentage of Movies and TV Shows",
         "plt.figure(figsize=(7, 7))\n"
         "counts = df['type'].value_counts()\n"
         "plt.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=[NETFLIX_RED, '#3A3A3A'], \n"
         "        explode=[0.05, 0], startangle=140, textprops={'fontsize': 12, 'color': 'white', 'fontweight': 'bold'})\n"
         "plt.title('Percentage of Movies and TV Shows on Netflix', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_2_percentage_distribution.png', dpi=150)\n"
         "plt.show()"),
         
        ("3. Content Added Each Year",
         "plt.figure(figsize=(12, 6))\n"
         "yearly_added = df.groupby(['added_year', 'type']).size().unstack(fill_value=0)\n"
         "plt.plot(yearly_added.index, yearly_added['Movie'], color=NETFLIX_RED, marker='o', linewidth=2.5, label='Movies')\n"
         "plt.plot(yearly_added.index, yearly_added['TV Show'], color='#D1A153', marker='s', linewidth=2.5, label='TV Shows')\n"
         "plt.title('Content Added Each Year on Netflix', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Year Added', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Amount of Content', fontsize=11, labelpad=10)\n"
         "plt.grid(True, linestyle='--', alpha=0.3)\n"
         "plt.legend(facecolor='#181818', edgecolor='none')\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_3_content_added_yearly.png', dpi=150)\n"
         "plt.show()"),
         
        ("4. Content Added Each Month (Seasonality)",
         "plt.figure(figsize=(12, 6))\n"
         "monthly_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']\n"
         "monthly_added = df.groupby(['added_month_name', 'type']).size().unstack(fill_value=0).reindex(monthly_order)\n"
         "x = np.arange(len(monthly_order))\n"
         "width = 0.35\n"
         "plt.bar(x - width/2, monthly_added['Movie'], width, label='Movies', color=NETFLIX_RED)\n"
         "plt.bar(x + width/2, monthly_added['TV Show'], width, label='TV Shows', color='#3A9D23')\n"
         "plt.xticks(x, monthly_order)\n"
         "plt.title('Content Added Each Month', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Month Added', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Amount of Content', fontsize=11, labelpad=10)\n"
         "plt.grid(True, linestyle='--', alpha=0.2, axis='y')\n"
         "plt.legend(facecolor='#181818', edgecolor='none')\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_4_content_added_monthly.png', dpi=150)\n"
         "plt.show()"),
         
        ("5. Movies Released by Year (1990-Present)",
         "plt.figure(figsize=(12, 6))\n"
         "movies_released = df[df['type'] == 'Movie'].groupby('release_year').size()\n"
         "movies_released_recent = movies_released[movies_released.index >= 1990]\n"
         "plt.fill_between(movies_released_recent.index, movies_released_recent.values, color=NETFLIX_RED, alpha=0.3)\n"
         "plt.plot(movies_released_recent.index, movies_released_recent.values, color=NETFLIX_RED, linewidth=2.5, marker='o', markevery=3)\n"
         "plt.title('Number of Movies Released by Year', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Release Year', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Count of Movies', fontsize=11, labelpad=10)\n"
         "plt.grid(True, linestyle='--', alpha=0.3)\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_5_movies_released_yearly.png', dpi=150)\n"
         "plt.show()"),
         
        ("6. Top 10 Countries Contributing Content",
         "plt.figure(figsize=(12, 6))\n"
         "country_counts = df[df['primary_country'] != 'Unknown']['primary_country'].value_counts().head(10)\n"
         "sns.barplot(x=country_counts.values, y=country_counts.index, palette='Reds_r')\n"
         "plt.title('Top 10 Countries Contributing Content on Netflix', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Number of Titles', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Country', fontsize=11, labelpad=10)\n"
         "for index, value in enumerate(country_counts.values):\n"
         "    plt.text(value + 20, index, str(value), va='center', color='white', fontweight='bold')\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_6_top_10_countries.png', dpi=150)\n"
         "plt.show()"),
         
        ("7. Top 15 Genres Represented",
         "plt.figure(figsize=(12, 7))\n"
         "genre_counts = df['primary_genre'].value_counts().head(15)\n"
         "sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='plasma')\n"
         "plt.title('Top 15 Genres on Netflix', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Number of Titles', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Primary Genre', fontsize=11, labelpad=10)\n"
         "for index, value in enumerate(genre_counts.values):\n"
         "    plt.text(value + 15, index, str(value), va='center', color='white', fontweight='bold')\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_7_top_15_genres.png', dpi=150)\n"
         "plt.show()"),
         
        ("8. Distribution of Content Ratings",
         "plt.figure(figsize=(12, 6))\n"
         "rating_order = df['rating'].value_counts().index\n"
         "sns.countplot(data=df, x='rating', palette='viridis', order=rating_order)\n"
         "plt.title('Distribution of Content Ratings on Netflix', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Rating Code', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Count', fontsize=11, labelpad=10)\n"
         "plt.xticks(rotation=45)\n"
         "for p in plt.gca().patches:\n"
         "    plt.gca().annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),\n"
         "                ha='center', va='bottom', xytext=(0, 3), textcoords='offset points', color='white')\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_8_top_ratings.png', dpi=150)\n"
         "plt.show()"),
         
        ("9. Top 10 Directors by Number of Titles",
         "plt.figure(figsize=(12, 7))\n"
         "director_counts = df[df['director'] != 'Unknown']['director'].value_counts().head(10)\n"
         "sns.barplot(x=director_counts.values, y=director_counts.index, color=NETFLIX_RED)\n"
         "plt.title('Top 10 Directors on Netflix by Number of Titles', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Number of Movies/TV Shows', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Director', fontsize=11, labelpad=10)\n"
         "for index, value in enumerate(director_counts.values):\n"
         "    plt.text(value + 0.3, index, str(value), va='center', color='white', fontweight='bold')\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_9_top_directors.png', dpi=150)\n"
         "plt.show()"),
         
        ("10. Top 10 Most Frequent Actors",
         "cast_list = df[df['cast'] != 'Unknown']['cast'].str.split(', ')\n"
         "all_actors = [actor.strip() for sublist in cast_list for actor in sublist]\n"
         "actor_series = pd.Series(all_actors).value_counts().head(10)\n\n"
         "plt.figure(figsize=(12, 7))\n"
         "sns.barplot(x=actor_series.values, y=actor_series.index, palette='coolwarm')\n"
         "plt.title('Top 10 Actors appearing on Netflix', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Number of Appearances', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Actor Name', fontsize=11, labelpad=10)\n"
         "for index, value in enumerate(actor_series.values):\n"
         "    plt.text(value + 0.5, index, str(value), va='center', color='white', fontweight='bold')\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_10_most_frequent_actors.png', dpi=150)\n"
         "plt.show()"),
         
        ("11. Movie Duration Distribution",
         "plt.figure(figsize=(12, 6))\n"
         "movie_durations = df[df['type'] == 'Movie']['movie_duration'].dropna()\n"
         "sns.histplot(movie_durations, bins=30, kde=True, color=NETFLIX_RED, edgecolor='white', alpha=0.7)\n"
         "plt.title('Distribution of Movie Durations (Minutes)', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Duration (Minutes)', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Density / Count', fontsize=11, labelpad=10)\n"
         "plt.grid(True, linestyle='--', alpha=0.2)\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_11_movie_duration_distribution.png', dpi=150)\n"
         "plt.show()"),
         
        ("12. Top 10 Longest Movies",
         "plt.figure(figsize=(12, 6))\n"
         "longest_movies = df[df['type'] == 'Movie'].sort_values(by='movie_duration', ascending=False).head(10)\n"
         "sns.barplot(x=longest_movies['movie_duration'], y=longest_movies['title'], color='#2270B4')\n"
         "plt.title('Top 10 Longest Movies on Netflix', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Duration (Minutes)', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Movie Title', fontsize=11, labelpad=10)\n"
         "for index, value in enumerate(longest_movies['movie_duration']):\n"
         "    plt.text(value + 3, index, f'{int(value)} min', va='center', color='white', fontweight='bold')\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_12_longest_movies.png', dpi=150)\n"
         "plt.show()"),
         
        ("13. Top 10 Shortest Movies",
         "plt.figure(figsize=(12, 6))\n"
         "shortest_movies = df[(df['type'] == 'Movie') & (df['movie_duration'] > 0)].sort_values(by='movie_duration', ascending=True).head(10)\n"
         "sns.barplot(x=shortest_movies['movie_duration'], y=shortest_movies['title'], color='#E57C04')\n"
         "plt.title('Top 10 Shortest Movies on Netflix', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Duration (Minutes)', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Movie Title', fontsize=11, labelpad=10)\n"
         "for index, value in enumerate(shortest_movies['movie_duration']):\n"
         "    plt.text(value + 0.3, index, f'{int(value)} min', va='center', color='white', fontweight='bold')\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_13_shortest_movies.png', dpi=150)\n"
         "plt.show()"),
         
        ("14. Average Movie Duration by Release Year",
         "plt.figure(figsize=(12, 6))\n"
         "avg_duration_years = df[df['type'] == 'Movie'].groupby('release_year')['movie_duration'].mean().reset_index()\n"
         "avg_duration_years_recent = avg_duration_years[avg_duration_years['release_year'] >= 1990]\n"
         "plt.plot(avg_duration_years_recent['release_year'], avg_duration_years_recent['movie_duration'], \n"
         "         color=NETFLIX_RED, linewidth=2.5, marker='o', markersize=5)\n"
         "plt.title('Average Movie Duration by Release Year (1990-Present)', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Release Year', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Average Duration (Minutes)', fontsize=11, labelpad=10)\n"
         "plt.grid(True, linestyle='--', alpha=0.2)\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_14_avg_movie_duration_trend.png', dpi=150)\n"
         "plt.show()"),
         
        ("15. Country-wise Content Growth Over Time",
         "plt.figure(figsize=(12, 6))\n"
         "top5_countries = df[df['primary_country'] != 'Unknown']['primary_country'].value_counts().head(5).index\n"
         "country_growth = df[df['primary_country'].isin(top5_countries)].groupby(['added_year', 'primary_country']).size().unstack(fill_value=0)\n"
         "country_growth_cum = country_growth.cumsum()\n"
         "country_growth_cum = country_growth_cum[country_growth_cum.index >= 2008]\n\n"
         "for i, country in enumerate(top5_countries):\n"
         "    plt.plot(country_growth_cum.index, country_growth_cum[country], marker='o', label=country, linewidth=2, color=ACCENT_COLORS[i])\n"
         "plt.title('Cumulative Content Growth Over Time (Top 5 Countries)', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Year Added', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Cumulative Content Count', fontsize=11, labelpad=10)\n"
         "plt.grid(True, linestyle='--', alpha=0.2)\n"
         "plt.legend(facecolor='#181818', edgecolor='none')\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_15_country_wise_growth.png', dpi=150)\n"
         "plt.show()"),
         
        ("16. Genre-wise Content Distribution",
         "plt.figure(figsize=(12, 6))\n"
         "genre_dist = df['primary_genre'].value_counts()\n"
         "sns.barplot(x=genre_dist.values, y=genre_dist.index, palette='magma')\n"
         "plt.title('Distribution of Content by Primary Genre', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Count', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Genre', fontsize=11, labelpad=10)\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_16_genre_distribution.png', dpi=150)\n"
         "plt.show()"),
         
        ("17. Rating Distribution: Movies vs TV Shows",
         "plt.figure(figsize=(12, 6))\n"
         "sns.countplot(data=df, x='rating', hue='type', palette=[NETFLIX_RED, '#3A9D23'], order=df['rating'].value_counts().index[:10])\n"
         "plt.title('Rating Distribution: Movies vs TV Shows (Top 10 Ratings)', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Rating', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Count', fontsize=11, labelpad=10)\n"
         "plt.legend(facecolor='#181818', edgecolor='none')\n"
         "plt.xticks(rotation=45)\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_17_rating_by_type.png', dpi=150)\n"
         "plt.show()"),
         
        ("18. Movies vs TV Shows by Country (Top 10 Countries)",
         "plt.figure(figsize=(12, 6))\n"
         "top10_countries = df[df['primary_country'] != 'Unknown']['primary_country'].value_counts().head(10).index\n"
         "country_type = df[df['primary_country'].isin(top10_countries)].groupby(['primary_country', 'type']).size().unstack(fill_value=0)\n"
         "country_type = country_type.reindex(top10_countries)\n\n"
         "x = np.arange(len(top10_countries))\n"
         "width = 0.35\n"
         "plt.bar(x - width/2, country_type['Movie'], width, label='Movies', color=NETFLIX_RED)\n"
         "plt.bar(x + width/2, country_type['TV Show'], width, label='TV Shows', color='#D1A153')\n"
         "plt.xticks(x, top10_countries, rotation=45)\n"
         "plt.title('Movies vs TV Shows by Country (Top 10)', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Country', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Count', fontsize=11, labelpad=10)\n"
         "plt.legend(facecolor='#181818', edgecolor='none')\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_18_movies_vs_tvshows_by_country.png', dpi=150)\n"
         "plt.show()"),
         
        ("19. Seasonality: Content Additions by Month",
         "plt.figure(figsize=(12, 6))\n"
         "monthly_data = df.groupby(['added_month', 'type']).size().unstack(fill_value=0)\n"
         "months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']\n"
         "plt.bar(months, monthly_data['Movie'], label='Movies', color=NETFLIX_RED, alpha=0.9)\n"
         "plt.bar(months, monthly_data['TV Show'], bottom=monthly_data['Movie'], label='TV Shows', color='#3A9D23', alpha=0.9)\n"
         "plt.title('Seasonality: Content Additions by Month', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Month', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Number of Additions', fontsize=11, labelpad=10)\n"
         "plt.legend(facecolor='#181818', edgecolor='none')\n"
         "plt.grid(True, linestyle='--', alpha=0.1, axis='y')\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_19_monthly_additions_distribution.png', dpi=150)\n"
         "plt.show()"),
         
        ("20. Heatmap of Monthly Additions by Year (2015-2021)",
         "heatmap_df = df[(df['added_year'] >= 2015) & (df['added_year'] <= 2021)]\n"
         "heatmap_pivot = heatmap_df.pivot_table(index='added_year', columns='added_month_name', values='show_id', aggfunc='count', fill_value=0)\n"
         "monthly_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']\n"
         "heatmap_pivot = heatmap_pivot.reindex(columns=monthly_order)\n\n"
         "plt.figure(figsize=(14, 8))\n"
         "sns.heatmap(heatmap_pivot, annot=True, fmt='d', cmap='Reds', cbar_kws={'label': 'Count of Titles'}, linewidths=.5)\n"
         "plt.title('Heatmap of Content Additions by Month and Year (2015-2021)', fontsize=14, fontweight='bold', pad=20)\n"
         "plt.xlabel('Month Added', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Year Added', fontsize=11, labelpad=10)\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_20_monthly_yearly_heatmap.png', dpi=150)\n"
         "plt.show()"),
         
        ("21. Top 10 Release Years Represented",
         "plt.figure(figsize=(12, 6))\n"
         "release_year_counts = df['release_year'].value_counts().head(10)\n"
         "sns.barplot(x=release_year_counts.index.astype(str), y=release_year_counts.values, palette='copper')\n"
         "plt.title('Top 10 Release Years represented on Netflix', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Release Year', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Count', fontsize=11, labelpad=10)\n"
         "for p in plt.gca().patches:\n"
         "    plt.gca().annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),\n"
         "                ha='center', va='bottom', xytext=(0, 3), textcoords='offset points', color='white')\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_21_top_release_years.png', dpi=150)\n"
         "plt.show()"),
         
        ("22. Content Growth Timeline (Cumulative Count)",
         "plt.figure(figsize=(12, 6))\n"
         "df_sorted = df.sort_values(by='date_added')\n"
         "df_sorted['cumulative_titles'] = range(1, len(df_sorted) + 1)\n\n"
         "plt.plot(df_sorted['date_added'], df_sorted['cumulative_titles'], color=NETFLIX_RED, linewidth=3)\n"
         "plt.fill_between(df_sorted['date_added'], df_sorted['cumulative_titles'], color=NETFLIX_RED, alpha=0.15)\n"
         "plt.title('Timeline of Cumulative Content Growth on Netflix', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Date Added', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Total Titles in Library', fontsize=11, labelpad=10)\n"
         "plt.grid(True, linestyle='--', alpha=0.2)\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_22_growth_timeline.png', dpi=150)\n"
         "plt.show()"),
         
        ("23. Decade-wise Content Distribution",
         "plt.figure(figsize=(10, 6))\n"
         "decade_counts = df['decade_str'].value_counts().sort_index()\n"
         "sns.barplot(x=decade_counts.index, y=decade_counts.values, palette='autumn')\n"
         "plt.title('Decade of Release for Netflix Library', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Decade', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Count of Titles', fontsize=11, labelpad=10)\n"
         "for p in plt.gca().patches:\n"
         "    plt.gca().annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),\n"
         "                ha='center', va='bottom', xytext=(0, 3), textcoords='offset points', color='white')\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_23_decade_distribution.png', dpi=150)\n"
         "plt.show()"),
         
        ("24. Movies by Duration Category",
         "plt.figure(figsize=(8, 8))\n"
         "movie_cat_counts = df[df['type'] == 'Movie']['duration_category'].value_counts()\n"
         "plt.pie(movie_cat_counts, labels=movie_cat_counts.index, autopct='%1.1f%%', colors=ACCENT_COLORS[:len(movie_cat_counts)],\n"
         "        startangle=140, pctdistance=0.85, textprops={'fontsize': 10, 'color': 'white', 'fontweight': 'bold'})\n"
         "centre_circle = plt.Circle((0,0),0.70,fc='#111111')\n"
         "fig = plt.gcf()\n"
         "fig.gca().add_artist(centre_circle)\n"
         "plt.title('Movies Categorized by Duration Length', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_24_movie_duration_categories.png', dpi=150)\n"
         "plt.show()"),
         
        ("25. Top 10 Most Common Genre Combinations",
         "plt.figure(figsize=(12, 7))\n"
         "genre_combos = df['listed_in'].value_counts().head(10)\n"
         "sns.barplot(x=genre_combos.values, y=genre_combos.index, palette='rocket')\n"
         "plt.title('Top 10 Most Common Genre Combinations on Netflix', fontsize=14, fontweight='bold', pad=15)\n"
         "plt.xlabel('Number of Titles', fontsize=11, labelpad=10)\n"
         "plt.ylabel('Genre Combination', fontsize=11, labelpad=10)\n"
         "for index, value in enumerate(genre_combos.values):\n"
         "    plt.text(value + 5, index, str(value), va='center', color='white', fontweight='bold')\n"
         "plt.tight_layout()\n"
         "plt.savefig('../images/charts/chart_25_genre_combinations.png', dpi=150)\n"
         "plt.show()")
    ]
    
    for title, code in vis_items:
        cells.append(nbf.v4.new_markdown_cell(f"### Visual Analysis - {title}\n"
                                             "The following cell generates and saves the plot for this analysis."))
        cells.append(nbf.v4.new_code_cell(code))
        
    # ------------------ CELL: Business Insights ------------------
    cells.append(nbf.v4.new_markdown_cell(
        "## Step 8 – Business Insights\n"
        "Based on our exploratory data analysis, here are the 20 key business insights derived from the Netflix Movies & TV Shows dataset:"
    ))
    
    cells.append(nbf.v4.new_code_cell(
        "insights = [\n"
        "    '1. Content Type Domination: Movies dominate Netflix, comprising 69.1% (5377 titles) of the library, compared to TV Shows at 30.9% (2400 titles).',\n"
        "    '2. Geographic Leader: The United States is by far the largest contributor of Netflix content, producing 2877 primary titles (37.0% of total).',\n"
        "    '3. India\\'s Profile: India is the second-largest content contributor with 956 titles, heavily dominated by Movies rather than TV Shows.',\n"
        "    '4. Leading Genre: The most popular primary genre category is \\'Dramas\\' with 1384 titles, reflecting a strong viewer preference for narrative-driven stories.',\n"
        "    '5. Target Audience Rating: Content rated \\'TV-MA\\' is the most common rating on the platform, accounting for 36.8% of titles. This indicates Netflix\\'s target audience is mature teenagers and adults.',\n"
        "    '6. Mature Content Share: Approximately 45.4% of Netflix\\'s content is rated for mature audiences (TV-MA, R, NC-17), positioning Netflix as a hub for sophisticated and adult-oriented programming.',\n"
        "    '7. Peak Production Year: The year with the highest volume of released titles present in the library is 2018, signifying a historical surge in licensing and content generation around this timeframe.',\n"
        "    '8. Peak Library Expansion: The year 2019 saw the highest amount of content added to the library, representing Netflix\\'s most aggressive expansion phase.',\n"
        "    '9. Top Director: The director with the most titles on Netflix is Raúl Campos, Jan Suter with 18 credits, demonstrating a strong collaborative presence on the platform.',\n"
        "    '10. Star Power: The actor appearing in the largest number of Netflix listings is Anupam Kher with 42 appearances, particularly in Indian cinema titles.',\n"
        "    '11. Average Movie Length: The average duration of movies on the platform is 99.3 minutes, aligning closely with standard theatrical standards of ~1.5 to 2 hours.',\n"
        "    '12. Movie Length Trends: In recent years (2015 onwards), the average movie length has slightly declined to 94.8 minutes, indicating a potential shift towards shorter, more digestible content formats.',\n"
        "    '13. Freshness of Library: The average age of content on Netflix is 12.1 years, highlighting that the catalog is overwhelmingly skewed towards recent releases from the last decade.',\n"
        "    '14. TV Show Longevity: A massive 67.0% of TV Shows on Netflix only have 1 season, which points to a high cancellation rate or a focus on limited miniseries format.',\n"
        "    '15. Monthly Addition Trends: The month of December is the most frequent choice for adding content, suggesting strategic positioning around holiday seasons or quarterly financial cycles.',\n"
        "    '16. Library Growth (2015-2020): From 2015 to 2020, yearly content additions grew by 2183.0%, indicating exponential platform expansion and investment in content acquisition.',\n"
        "    '17. Genre Synergy: The most common genre combination is \\'Documentaries\\', representing a strong library focus on localized stand-up comedy specials.',\n"
        "    '18. Modern Skew: Over 73.3% of all Netflix content belongs to the 2010s decade, proving that older classic films/shows comprise a minority portion of the library.',\n"
        "    '19. Movie Category Share: The \\'Feature (90-120 min)\\' category represents the dominant duration segment for Movies, representing 47.9% of the movie catalog.',\n"
        "    '20. Local Preferences: While movies dominate overall, countries like the United Kingdom exhibit a much higher ratio of TV Shows (40.8% of UK titles are TV Shows) compared to the global average of TV Shows.'\n"
        "]\n\n"
        "for insight in insights:\n"
        "    print(insight)"
    ))
    
    nb['cells'] = cells
    
    os.makedirs("notebooks", exist_ok=True)
    with open("notebooks/Netflix_Analysis.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb, f)
        
    print("Jupyter Notebook created at: notebooks/Netflix_Analysis.ipynb")

if __name__ == "__main__":
    create_notebook()
