# Netflix Movies & TV Shows Analysis 🍿

A professional Python-based Data Science and Business Intelligence portfolio project analyzing the Netflix global streaming catalogue. This project focuses on **Data Cleaning, Feature Engineering, Exploratory Data Analysis (EDA), Data Visualization, and Business Intelligence** to extract 20+ key insights and compile a professional executive PDF report and interactive Streamlit web dashboard.

---

## 📁 Project Folder Structure

```
Netflix_Movies_Analysis/
│
├── data/
│   └── netflix_titles.csv        # Kaggle Netflix titles dataset
│
├── notebooks/
│   └── Netflix_Analysis.ipynb    # Fully executed Jupyter Notebook
│
├── images/
│   ├── charts/                   # 25+ generated analysis charts
│   └── dashboard/                # Dashboard assets / screenshots
│
├── reports/
│   └── Netflix_Report.pdf        # Automated PDF Executive Report
│
├── app.py                        # Interactive Streamlit Web Dashboard
├── generate_report.py            # PDF Report generation script
├── run_eda.py                    # Static EDA execution script
├── download_data.py              # Programmatic data downloader
├── requirements.txt              # Project dependencies
└── README.md                     # Documentation
```

---

## 🛠️ Technologies Used

* **Python 3.13**
* **Pandas** & **NumPy** for Data Cleaning & Feature Engineering
* **Matplotlib** & **Seaborn** for static premium data styling
* **Plotly** & **Streamlit** for the interactive Web App Dashboard
* **ReportLab** for programmatically compiling multi-page PDF reports
* **Jupyter Notebook** for interactive analysis workflow

---

## 📊 Dataset Information

The project analyzes the popular Kaggle **Netflix Movies and TV Shows Dataset** (`netflix_titles.csv`), consisting of **7,787 rows** and **12 original columns** outlining:
* `show_id` - Unique identifier
* `type` - Movie or TV Show
* `title` - Title name
* `director` - Director credits
* `cast` - Actor list
* `country` - Production country
* `date_added` - Date uploaded to Netflix
* `release_year` - Original release year
* `rating` - Age rating
* `duration` - Runtime (minutes or seasons)
* `listed_in` - Genres
* `description` - Synopsis

---

## 🧼 Data Cleaning & Feature Engineering

The raw dataset underwent thorough cleaning:
1. **Deduplication:** Zero duplicate rows found.
2. **Imputation:** Null fields in `director`, `cast`, and `country` filled with `'Unknown'`. Rating nulls filled with `'Unknown'`.
3. **Temporal Parsing:** Dropped 10 null dates; parsed remaining into standard datetime objects.
4. **Feature Engineering:**
   * Temporal columns: `added_year`, `added_month`, `added_day`, `added_month_name`, `added_day_name`.
   * Separate numerical runtimes: `movie_duration` (minutes) and `tv_seasons` (seasons).
   * Primary categorical columns: `primary_genre` and `primary_country` (taking the first listed item).
   * `content_age` (2026 - release year) and `decade` of release.
   * Movie length categorization (`Short`, `Standard`, `Feature`, `Long`, `Epic`).

---

## 💡 20 Key Business Insights

1. **Content Type Domination:** Movies dominate Netflix, comprising 69.1% (5377 titles) of the library, compared to TV Shows at 30.9% (2400 titles).
2. **Geographic Leader:** The United States is by far the largest contributor of Netflix content, producing 2877 primary titles (37.0% of total).
3. **India's Profile:** India is the second-largest content contributor with 956 titles, heavily dominated by Movies rather than TV Shows.
4. **Leading Genre:** The most popular primary genre category is 'Dramas' with 1384 titles, reflecting a strong viewer preference for narrative-driven stories.
5. **Target Audience Rating:** Content rated 'TV-MA' is the most common rating on the platform, accounting for 36.8% of titles. This indicates Netflix's target audience is mature teenagers and adults.
6. **Mature Content Share:** Approximately 45.4% of Netflix's content is rated for mature audiences (TV-MA, R, NC-17), positioning Netflix as a hub for sophisticated and adult-oriented programming.
7. **Peak Production Year:** The year with the highest volume of released titles present in the library is 2018, signifying a historical surge in licensing and content generation around this timeframe.
8. **Peak Library Expansion:** The year 2019 saw the highest amount of content added to the library, representing Netflix's most aggressive expansion phase.
9. **Top Director:** The director with the most titles on Netflix is Raúl Campos, Jan Suter with 18 credits, demonstrating a strong collaborative presence on the platform.
10. **Star Power:** The actor appearing in the largest number of Netflix listings is Anupam Kher with 42 appearances, particularly in Indian cinema titles.
11. **Average Movie Length:** The average duration of movies on the platform is 99.3 minutes, aligning closely with standard theatrical standards of ~1.5 to 2 hours.
12. **Movie Length Trends:** In recent years (2015 onwards), the average movie length has slightly declined to 94.8 minutes, indicating a potential shift towards shorter, more digestible content formats.
13. **Freshness of Library:** The average age of content on Netflix is 12.1 years, highlighting that the catalog is overwhelmingly skewed towards recent releases from the last decade.
14. **TV Show Longevity:** A massive 67.0% of TV Shows on Netflix only have 1 season, which points to a high cancellation rate or a focus on limited miniseries format.
15. **Monthly Addition Trends:** The month of December is the most frequent choice for adding content, suggesting strategic positioning around holiday seasons or quarterly financial cycles.
16. **Library Growth (2015-2020):** From 2015 to 2020, yearly content additions grew by 2183.0%, indicating exponential platform expansion and investment in content acquisition.
17. **Genre Synergy:** The most common genre combination is 'Documentaries', representing a strong library focus on localized stand-up comedy specials.
18. **Modern Skew:** Over 73.3% of all Netflix content belongs to the 2010s decade, proving that older classic films/shows comprise a minority portion of the library.
19. **Movie Category Share:** The 'Feature (90-120 min)' category represents the dominant duration segment for Movies, representing 47.9% of the movie catalog.
20. **Local Preferences:** While movies dominate overall, countries like the United Kingdom exhibit a much higher ratio of TV Shows (40.8% of UK titles are TV Shows) compared to the global average of TV Shows.

---

## 📊 Visualizations Included

All 25 static charts are saved inside `images/charts/` in high definition, employing a curated Netflix Dark Theme color palette:
1. `chart_1_movies_vs_tvshows.png`: Distribution of Content Type.
2. `chart_2_percentage_distribution.png`: Percentage breakdown of Movies vs TV Shows.
3. `chart_3_content_added_yearly.png`: Timeline of additions by type and year.
4. `chart_4_content_added_monthly.png`: Seasonality bar chart of content added monthly.
5. `chart_5_movies_released_yearly.png`: Area chart showing movie release year counts (1990+).
6. `chart_6_top_10_countries.png`: Top 10 primary production country outputs.
7. `chart_7_top_15_genres.png`: Top 15 primary genre classifications.
8. `chart_8_top_ratings.png`: Count plot of age rating codes.
9. `chart_9_top_directors.png`: Top 10 director credits.
10. `chart_10_most_frequent_actors.png`: Top 10 cast credits.
11. `chart_11_movie_duration_distribution.png`: Histogram & KDE of movie runtime.
12. `chart_12_longest_movies.png`: Horizontal bar chart of the 10 longest movie runtimes.
13. `chart_13_shortest_movies.png`: Horizontal bar chart of the 10 shortest movie runtimes.
14. `chart_14_avg_movie_duration_trend.png`: Yearly average movie length over release years.
15. `chart_15_country_wise_growth.png`: Growth timeline for Top 5 countries.
16. `chart_16_genre_distribution.png`: Complete bar chart of all primary genres.
17. `chart_17_rating_by_type.png`: Side-by-side rating distributions (Movies vs TV).
18. `chart_18_movies_vs_tvshows_by_country.png`: Content split for Top 10 countries.
19. `chart_19_monthly_additions_distribution.png`: Stacked bar chart showing additions seasonality.
20. `chart_20_monthly_yearly_heatmap.png`: Monthly additions by year heatmap (2015-2021).
21. `chart_21_top_release_years.png`: Top 10 years of release.
22. `chart_22_growth_timeline.png`: Cumulative library growth curve over time.
23. `chart_23_decade_distribution.png`: Bar chart of decade of release.
24. `chart_24_movie_duration_categories.png`: Doughnut chart of movie duration lengths.
25. `chart_25_genre_combinations.png`: Common multi-genre listings.

---

## ⚡ Setup & Installation

To run this project locally, ensure you have Python 3.10+ installed. Follow these steps:

### 1. Clone the repository and navigate to its folder:
```bash
git clone https://github.com/your-username/Netflix_Movies_Analysis.git
cd Netflix_Movies_Analysis
```

### 2. Install the required Python libraries:
```bash
pip install -r requirements.txt
```

### 3. Ensure the dataset is downloaded:
If the dataset is missing, you can run the program script to download it automatically:
```bash
python download_data.py
```

---

## 🚀 How to Run

### Run the static EDA analysis and generate charts:
```bash
python run_eda.py
```

### Compile the Executive PDF Report:
```bash
python generate_report.py
```
This generates the report at `reports/Netflix_Report.pdf` with the embedded charts.

### Launch the Streamlit Web Dashboard:
```bash
streamlit run app.py
```
This launches a browser session pointing to local server (usually `http://localhost:8501`) displaying the interactive dashboard.

### Open the Jupyter Notebook:
Navigate to the `notebooks/` directory and open:
```bash
jupyter notebook notebooks/Netflix_Analysis.ipynb
```
The notebook is pre-compiled and executed with all visualization figures and inline calculations embedded.

---

## 🎯 Conclusion & Future Scope
The platform features an expansive library predominantly composed of US-produced films and adult content. Future extensions of this project could involve integrating user engagement datasets, incorporating NLP sentiment analysis on descriptions, or designing a content recommendation system using collaborative filtering algorithms.
