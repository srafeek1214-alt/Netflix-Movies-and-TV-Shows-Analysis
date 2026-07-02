import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# Target PDF File path
reports_dir = "reports"
os.makedirs(reports_dir, exist_ok=True)
pdf_path = os.path.join(reports_dir, "Netflix_Report.pdf")

# Define Theme Colors (Light Theme with Netflix Red Accents)
NETFLIX_RED = colors.HexColor("#E50914")
DARK_CHARCOAL = colors.HexColor("#221F1F")
LIGHT_GREY = colors.HexColor("#F5F5F1")
TEXT_GREY = colors.HexColor("#333333")
WHITE = colors.HexColor("#FFFFFF")

# Setup Stylesheet
styles = getSampleStyleSheet()

# Create Custom Paragraph Styles
title_style = ParagraphStyle(
    'CoverTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=32,
    leading=38,
    textColor=NETFLIX_RED,
    alignment=TA_CENTER,
    spaceAfter=15
)

subtitle_style = ParagraphStyle(
    'CoverSubtitle',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=16,
    leading=22,
    textColor=TEXT_GREY,
    alignment=TA_CENTER,
    spaceAfter=40
)

meta_style = ParagraphStyle(
    'CoverMeta',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=11,
    leading=16,
    textColor=colors.HexColor("#666666"),
    alignment=TA_CENTER,
    spaceAfter=10
)

h1_style = ParagraphStyle(
    'Heading1_Custom',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=20,
    leading=26,
    textColor=NETFLIX_RED,
    spaceBefore=15,
    spaceAfter=10,
    keepWithNext=True
)

h2_style = ParagraphStyle(
    'Heading2_Custom',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=14,
    leading=18,
    textColor=DARK_CHARCOAL,
    spaceBefore=12,
    spaceAfter=6,
    keepWithNext=True
)

body_style = ParagraphStyle(
    'Body_Custom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=10.5,
    leading=15,
    textColor=TEXT_GREY,
    alignment=TA_LEFT,
    spaceAfter=10
)

bullet_style = ParagraphStyle(
    'Bullet_Custom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=10,
    leading=14,
    textColor=TEXT_GREY,
    leftIndent=20,
    firstLineIndent=-10,
    spaceAfter=6
)

insight_style = ParagraphStyle(
    'Insight_Custom',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=14,
    textColor=DARK_CHARCOAL,
    leftIndent=20,
    firstLineIndent=-10,
    spaceAfter=6
)

# Page number footer callback
def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(colors.HexColor('#666666'))
    page_num = canvas.getPageNumber()
    if page_num > 1:
        canvas.drawRightString(8.5 * inch - 0.75 * inch, 0.5 * inch, f"Page {page_num}")
        canvas.drawString(0.75 * inch, 0.5 * inch, "Netflix Movies & TV Shows Analysis Report")
        canvas.setStrokeColor(colors.HexColor('#CCCCCC'))
        canvas.setLineWidth(0.5)
        canvas.line(0.75 * inch, 0.65 * inch, 8.5 * inch - 0.75 * inch, 0.65 * inch)
    canvas.restoreState()

def build_pdf():
    # Setup doc template: margins 0.75 inch
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.85*inch
    )
    
    story = []
    
    # ==========================================
    # PAGE 1: COVER PAGE
    # ==========================================
    story.append(Spacer(1, 1.5 * inch))
    # Elegant logo line / header
    story.append(Paragraph("<b>DATA SCIENCE PORTFOLIO</b>", ParagraphStyle('SubHeader', parent=meta_style, textColor=NETFLIX_RED, fontSize=12, spaceAfter=20)))
    story.append(Paragraph("NETFLIX MOVIES &<br/>TV SHOWS ANALYSIS", title_style))
    
    # Decorative line
    d_table = Table([[""]], colWidths=[3.0*inch], rowHeights=[4])
    d_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NETFLIX_RED),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(d_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("An In-Depth Exploratory Data Analysis & Business Intelligence Report", subtitle_style))
    story.append(Spacer(1, 2.0 * inch))
    
    # Metadata Block
    story.append(Paragraph("<b>Prepared By:</b> Antigravity AI Data Scientist", meta_style))
    story.append(Paragraph("<b>Tool Stack:</b> Python, Pandas, Matplotlib, Seaborn, Streamlit, ReportLab", meta_style))
    story.append(Paragraph("<b>Date:</b> June 2026", meta_style))
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 2: OBJECTIVES & METHODOLOGY
    # ==========================================
    story.append(Paragraph("1. Introduction & Objectives", h1_style))
    story.append(Paragraph(
        "This project presents a comprehensive, end-to-end data analysis of Netflix's global streaming catalog, consisting of "
        "nearly 7,800 movies and TV shows. Using advanced python-based data manipulation, feature engineering, and high-DPI custom "
        "visualizations, this report reveals critical business trends, audience rating preferences, geographic concentrations, and content lifecycle dynamics. "
        "The ultimate goal is to translate technical EDA findings into 20+ actionable business recommendations for executive-level decision making.",
        body_style
    ))
    
    story.append(Paragraph("Core Objectives:", h2_style))
    story.append(Paragraph("• <b>Understand Content Mix:</b> Assess the ratios, trends, and seasonal additions of Movies versus TV Shows.", bullet_style))
    story.append(Paragraph("• <b>Evaluate Geographic Distribution:</b> Identify leading production regions and country-specific portfolio variations.", bullet_style))
    story.append(Paragraph("• <b>Investigate Audience Demographics:</b> Analyze content rating categories to profile Netflix's target demographics.", bullet_style))
    story.append(Paragraph("• <b>Discover Key Talents:</b> Track the directors and cast members with the highest presence in the library.", bullet_style))
    story.append(Paragraph("• <b>Temporal Life Cycles:</b> Identify the rate of content decay, average movie lengths, and library freshness indices.", bullet_style))
    
    story.append(Spacer(1, 15))
    story.append(Paragraph("2. Dataset Description", h1_style))
    story.append(Paragraph(
        "The analysis utilizes the famous <b>Kaggle Netflix Movies and TV Shows Dataset</b> (specifically, `netflix_titles.csv`), which details "
        "12 raw attributes for every title on the platform. The fields include: unique identifiers (`show_id`), type (Movie or TV Show), "
        "title name, director credits, main cast lists, country of production, date added to Netflix, release year, audience rating code, "
        "duration length (minutes or seasons), primary genre classifications, and plot descriptions.",
        body_style
    ))
    
    # Summary Info Table
    data_summary = [
        ['Metric', 'Details'],
        ['Total Observations', '7,787 rows'],
        ['Unique Movies', '5,377 (69.1%)'],
        ['Unique TV Shows', '2,400 (30.9%)'],
        ['Original Columns', '12 attributes'],
        ['Engineered Features', '9 additional columns'],
    ]
    t = Table(data_summary, colWidths=[2.5*inch, 4.0*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NETFLIX_RED),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), LIGHT_GREY),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 9.5),
        ('TEXTCOLOR', (0,1), (-1,-1), TEXT_GREY),
    ]))
    story.append(t)
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 3: DATA CLEANING & FEATURE ENGINEERING
    # ==========================================
    story.append(Paragraph("3. Data Cleaning Process", h1_style))
    story.append(Paragraph(
        "Prior to starting the EDA, the raw dataset underwent standard data quality cleaning procedures. Missing values were "
        "analyzed and resolved as follows:",
        body_style
    ))
    story.append(Paragraph("• <b>Deduplication:</b> Explored and verified that there were zero exact duplicate rows in the dataset.", bullet_style))
    story.append(Paragraph("• <b>Imputation of Missing Metadata:</b> For fields like `director`, `cast`, and `country` where valuable metadata was missing, "
                           "values were imputed with 'Unknown' rather than dropping them, preserving {7280/7787*100:.1f}% country rows and preventing metadata bias.", bullet_style))
    story.append(Paragraph("• <b>Imputation of Ratings:</b> Missing values in `rating` were populated with 'Unknown' (only 7 occurrences).", bullet_style))
    story.append(Paragraph("• <b>Temporal Cleaning:</b> Deleted 10 rows where `date_added` was null. Parsed `date_added` strings from formats "
                           "like 'August 14, 2020' into standard Python datetime format.", bullet_style))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("4. Feature Engineering", h1_style))
    story.append(Paragraph(
        "To enable complex queries and multi-dimensional analysis, the following engineered features were appended to the dataset:",
        body_style
    ))
    story.append(Paragraph("1. <b>Temporal Breakdowns:</b> Extracted `added_year`, `added_month`, and `added_day` from the datetime variable, along with textual month name and day-of-week name.", bullet_style))
    story.append(Paragraph("2. <b>Duration Splitting:</b> Parsed the alphanumeric `duration` column and split it into two numeric features: `movie_duration` (expressed in integer minutes for Movies) and `tv_seasons` (integer seasons for TV Shows).", bullet_style))
    story.append(Paragraph("3. <b>Primary Classifications:</b> Extracted the first listed country as `primary_country` and first listed genre as `primary_genre` to handle multi-valued attributes cleanly.", bullet_style))
    story.append(Paragraph("4. <b>Decades & Age:</b> Calculated `decade` (e.g. 2010s) and `content_age` (calculated relative to 2026) to profile inventory freshness.", bullet_style))
    story.append(Paragraph("5. <b>Movie Categories:</b> Grouped movies into duration categories: Short (<60 min), Standard (60-90 min), Feature (90-120 min), Long (120-180 min), and Epic (>180 min).", bullet_style))
    
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 4: VISUAL EDA - SECTION 1
    # ==========================================
    story.append(Paragraph("5. Exploratory Data Analysis & Visualizations", h1_style))
    story.append(Paragraph(
        "Below are selected visualizations from our analysis displaying content distributions and growth patterns.",
        body_style
    ))
    
    # Embed Chart 1 and Chart 3 side-by-side or stacked
    c1_path = "images/charts/chart_1_movies_vs_tvshows.png"
    c3_path = "images/charts/chart_3_content_added_yearly.png"
    
    if os.path.exists(c1_path):
        story.append(Paragraph("<b>Content Composition (Movies vs. TV Shows)</b>", h2_style))
        story.append(Image(c1_path, width=5.5*inch, height=3.0*inch))
        story.append(Paragraph("<i>Interpretation: Movies dominate the Netflix catalogue (representing over two-thirds of all listings), though TV shows have seen growing investment in recent years.</i>", ParagraphStyle('ItalicText', parent=body_style, fontName='Helvetica-Oblique', fontSize=9, leading=12)))
        story.append(Spacer(1, 15))
        
    if os.path.exists(c3_path):
        story.append(Paragraph("<b>Annual Growth Trends (Content Added by Year)</b>", h2_style))
        story.append(Image(c3_path, width=5.5*inch, height=2.8*inch))
        story.append(Paragraph("<i>Interpretation: Library expansion peaked around 2019. Since then, Netflix has slightly slowed content acquisition rate, pivoting towards localized and original productions.</i>", ParagraphStyle('ItalicText', parent=body_style, fontName='Helvetica-Oblique', fontSize=9, leading=12)))
        
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 5: VISUAL EDA - SECTION 2
    # ==========================================
    story.append(Paragraph("Exploratory Data Analysis (Continued)", h1_style))
    
    c11_path = "images/charts/chart_11_movie_duration_distribution.png"
    c20_path = "images/charts/chart_20_monthly_yearly_heatmap.png"
    
    if os.path.exists(c11_path):
        story.append(Paragraph("<b>Movie Length Distribution (in Minutes)</b>", h2_style))
        story.append(Image(c11_path, width=5.5*inch, height=2.7*inch))
        story.append(Paragraph("<i>Interpretation: Movie lengths follow a normal distribution centered tightly around 99.3 minutes, satisfying standard movie-length preferences.</i>", ParagraphStyle('ItalicText', parent=body_style, fontName='Helvetica-Oblique', fontSize=9, leading=12)))
        story.append(Spacer(1, 15))
        
    if os.path.exists(c20_path):
        story.append(Paragraph("<b>Heatmap of Monthly Additions by Year</b>", h2_style))
        story.append(Image(c20_path, width=5.5*inch, height=3.0*inch))
        story.append(Paragraph("<i>Interpretation: The heatmap highlights seasonal upload surges, typically concentrated around October, November, and December, corresponding to year-end holidays.</i>", ParagraphStyle('ItalicText', parent=body_style, fontName='Helvetica-Oblique', fontSize=9, leading=12)))
        
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 6: BUSINESS INSIGHTS
    # ==========================================
    story.append(Paragraph("6. Key Business Insights", h1_style))
    story.append(Paragraph(
        "Based on our exploratory data analysis, here are the 20 key business insights derived from the Netflix catalog:",
        body_style
    ))
    
    insights = [
        "<b>1. Content Type Domination:</b> Movies dominate Netflix, comprising 69.1% (5,377 titles) of the library, compared to TV Shows at 30.9% (2,400 titles).",
        "<b>2. Geographic Leader:</b> The United States is by far the largest contributor of Netflix content, producing 2,877 primary titles (37.0% of total).",
        "<b>3. India's Profile:</b> India is the second-largest content contributor with 956 titles, heavily dominated by Movies rather than TV Shows.",
        "<b>4. Leading Genre:</b> The most popular primary genre category is 'Dramas' with 1,384 titles, reflecting a strong viewer preference for narrative-driven stories.",
        "<b>5. Target Audience Rating:</b> Content rated 'TV-MA' is the most common rating on the platform, accounting for 36.8% of titles. This indicates Netflix's target audience is mature teenagers and adults.",
        "<b>6. Mature Content Share:</b> Approximately 45.4% of Netflix's content is rated for mature audiences (TV-MA, R, NC-17), positioning Netflix as a hub for sophisticated and adult-oriented programming.",
        "<b>7. Peak Production Year:</b> The year with the highest volume of released titles present in the library is 2018, signifying a historical surge in licensing and content generation around this timeframe.",
        "<b>8. Peak Library Expansion:</b> The year 2019 saw the highest amount of content added to the library, representing Netflix's most aggressive expansion phase.",
        "<b>9. Top Director:</b> The director with the most titles on Netflix is Raúl Campos, Jan Suter with 18 credits, demonstrating a strong collaborative presence on the platform.",
        "<b>10. Star Power:</b> The actor appearing in the largest number of Netflix listings is Anupam Kher with 42 appearances, particularly in Indian cinema titles.",
        "<b>11. Average Movie Length:</b> The average duration of movies on the platform is 99.3 minutes, aligning closely with standard theatrical standards of ~1.5 to 2 hours.",
        "<b>12. Movie Length Trends:</b> In recent years (2015 onwards), the average movie length has slightly declined to 94.8 minutes, indicating a potential shift towards shorter, more digestible content formats.",
        "<b>13. Freshness of Library:</b> The average age of content on Netflix is 12.1 years, highlighting that the catalog is overwhelmingly skewed towards recent releases from the last decade.",
        "<b>14. TV Show Longevity:</b> A massive 67.0% of TV Shows on Netflix only have 1 season, which points to a high cancellation rate or a focus on limited miniseries format.",
        "<b>15. Monthly Addition Trends:</b> The month of December is the most frequent choice for adding content, suggesting strategic positioning around holiday seasons or quarterly financial cycles.",
        "<b>16. Library Growth (2015-2020):</b> From 2015 to 2020, yearly content additions grew by 2,183.0%, indicating exponential platform expansion and investment in content acquisition.",
        "<b>17. Genre Synergy:</b> The most common genre combination is 'Documentaries', representing a strong library focus on localized stand-up comedy specials.",
        "<b>18. Modern Skew:</b> Over 73.3% of all Netflix content belongs to the 2010s decade, proving that older classic films/shows comprise a minority portion of the library.",
        "<b>19. Movie Category Share:</b> The 'Feature (90-120 min)' category represents the dominant duration segment for Movies, representing 47.9% of the movie catalog.",
        "<b>20. Local Preferences:</b> While movies dominate overall, countries like the United Kingdom exhibit a much higher ratio of TV Shows (40.8% of UK titles are TV Shows) compared to the global average of TV Shows."
    ]
    
    for insight in insights:
        story.append(Paragraph(f"• {insight}", bullet_style))
        
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 7: CONCLUSION & FUTURE SCOPE
    # ==========================================
    story.append(Paragraph("7. Conclusion", h1_style))
    story.append(Paragraph(
        "Through data exploration, we've demonstrated that Netflix's streaming catalog is strategically optimized for adult audiences (heavy TV-MA content share) "
        "and is primarily focused on American-produced films and international dramas/comedies. "
        "The peak library growth occurred in 2019, followed by a transition period where content counts slightly adjusted, "
        "prioritizing higher-quality original shows and local language films to drive international subscriber acquisition.",
        body_style
    ))
    
    story.append(Paragraph("8. Future Scope", h1_style))
    story.append(Paragraph(
        "While this analysis provides a clear historical picture of the Netflix catalogue, adding the following items in the future "
        "would provide deeper insights:",
        body_style
    ))
    story.append(Paragraph("• <b>User Engagement Integration:</b> Merging the library dataset with hourly viewership hours (e.g. Netflix engagement reports) to check the correlation between content volume and audience attention.", bullet_style))
    story.append(Paragraph("• <b>Financial Data Merging:</b> Combining title production budgets with rating and genre categories to analyze ROI.", bullet_style))
    story.append(Paragraph("• <b>Sentiment Analysis on Descriptions:</b> Performing NLP on description text to find core thematic patterns across rating categories.", bullet_style))
    story.append(Paragraph("• <b>Recommendation Systems:</b> Applying collaborative filtering or content-based filtering algorithms to predict user recommendations based on the engineered genre features.", bullet_style))
    
    # Build Document
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"PDF report successfully compiled at: {pdf_path}")

if __name__ == "__main__":
    build_pdf()
