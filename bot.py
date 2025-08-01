from selenium import webdriver
from tools.webdriver import clean_webdriver_cache
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import redis
import os

def setup_webdriver():
    """
    Sets up the Chrome WebDriver using WebDriver Manager.
    Cleans the webdriver cache before setup.
    """
    
    # Clean the webdriver cache - commented out for now
    clean_webdriver_cache()
    
    # Set up Chrome WebDriver
    try:
        options = Options()
        options.add_argument("--headless-new")  # Run in background
        options.add_argument("--log-level=3") #Reduce webdriver logs - 3 = FATAL only
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...") # Set a custom user agent

        service = Service(ChromeDriverManager().install())

        driver = webdriver.Chrome(service=service, options=options)
        print("WebDriver setup successfully.")
        return driver
    
    except Exception as e:
        print(f"Error setting up WebDriver: {e}")
        return None

def set_redis_data(in_df):
    """
    Sets the JSON data in Redis.
    """

    try:
        str_json = in_df.iloc[:5].to_json(orient="records", lines=True)
        print(str_json)

        REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
        REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        r.set('nasdaq_data', str_json)
        print("Data set in Redis.")
        
    except Exception as e:
        print(f"Error setting data in Redis: {e}")


def main():

    driver = setup_webdriver()
    if driver:

        while True:
            try:             
                driver.get("https://www.investing.com/indices/nq-100-components")
                print("Opened", driver.title)

                stock_table = driver.find_elements(By.TAG_NAME, "table")
                print("Found stock table on the page. - Tables found:", len(stock_table))

                rows = stock_table[1].find_elements(By.TAG_NAME, "tr")
                print(f"Found {len(rows)} rows in the stock table.")

                data = []
                for row in rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    row_data = [col.text for col in cols]
                    data.append(row_data)

                


                df = pd.DataFrame(data)
                df = df.dropna()
                df.columns = ["Symbol", "Name", "Last Price", "High", "Low", "Change %", "Volume", "Upside", "Time"]
                df.drop(columns=["Symbol", "Upside"], inplace=True)

                set_redis_data(df)

            except Exception as e:
                print(f"Error during web extraction: {e}")
                break

        driver.quit()
        print("WebDriver Quit.")
        


if __name__ == "__main__":
    main()