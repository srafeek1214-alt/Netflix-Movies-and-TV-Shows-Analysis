import os
import urllib.request

def download_dataset():
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    target_file = os.path.join(data_dir, "netflix_titles.csv")
    
    if os.path.exists(target_file):
        print(f"Dataset already exists at: {target_file}")
        return
    
    # Try multiple URLs in case one is down or slow
    urls = [
        "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-04-20/netflix_titles.csv",
        "https://raw.githubusercontent.com/shivamb/netflix-shows/master/netflix_titles.csv"
    ]
    
    for url in urls:
        try:
            print(f"Attempting to download dataset from: {url}")
            urllib.request.urlretrieve(url, target_file)
            print(f"Successfully downloaded to: {target_file}")
            # Verify file size is reasonable (should be > 1MB)
            if os.path.getsize(target_file) > 100000:
                return
            else:
                print("Downloaded file is too small, trying next URL...")
        except Exception as e:
            print(f"Failed to download from {url}. Error: {e}")
            
    raise RuntimeError("Could not download the Netflix dataset from any source.")

if __name__ == "__main__":
    download_dataset()
