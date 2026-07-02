import os
import subprocess
import sys

def main():
    print("="*60)
    print("Netflix Movies & TV Shows Analysis Project - Main Runner")
    print("="*60)
    
    # 1. Download Dataset
    print("\n[Step 1/4] Checking and downloading dataset...")
    try:
        import download_data
        download_data.download_dataset()
    except Exception as e:
        print(f"Error during step 1: {e}")
        sys.exit(1)
        
    # 2. Run EDA and Generate Charts
    print("\n[Step 2/4] Running exploratory data analysis and saving charts...")
    try:
        # Run run_eda.py as a script or import it
        import run_eda
        df = run_eda.load_and_clean_data()
        df = run_eda.feature_engineering(df)
        run_eda.generate_charts(df)
    except Exception as e:
        print(f"Error during step 2: {e}")
        sys.exit(1)
        
    # 3. Generate Notebook
    print("\n[Step 3/4] Generating Jupyter Notebook...")
    try:
        import generate_notebook
        generate_notebook.create_notebook()
    except Exception as e:
        print(f"Error during step 3: {e}")
        sys.exit(1)
        
    # 4. Generate PDF Report
    print("\n[Step 4/4] Compiling Executive PDF Report...")
    try:
        import generate_report
        generate_report.build_pdf()
    except Exception as e:
        print(f"Error during step 4: {e}")
        sys.exit(1)
        
    print("\n" + "="*60)
    print("Project successfully initialized and compiled!")
    print("="*60)
    print("- Raw dataset saved to: data/netflix_titles.csv")
    print("- Executable notebook saved to: notebooks/Netflix_Analysis.ipynb")
    print("- 25+ visual charts saved to: images/charts/")
    print("- PDF Executive Report saved to: reports/Netflix_Report.pdf")
    print("\nTo launch the interactive dashboard, run:")
    print("  streamlit run app.py")
    print("="*60)

if __name__ == "__main__":
    main()
