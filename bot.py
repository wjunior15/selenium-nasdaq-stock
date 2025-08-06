from selenium import webdriver
from tools.webdriver import clean_webdriver_cache
from tools.process_data import order_by_change
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import datetime
import pandas as pd
import redis
import os
from config import config
from dotenv import load_dotenv

load_dotenv()

def setup_webdriver():
    """
    Sets up the Chrome WebDriver using WebDriver Manager.
    Cleans the webdriver cache before setup.
    """
    
    # Set up Chrome WebDriver
    try:
        options = Options()
        options.add_argument("--headless-new")  # Run in background
        options.add_argument("--log-level=3") #Reduce webdriver logs - 3 = FATAL only

        str_executor_type = config.EXECUTOR_TYPE.lower()

        if str_executor_type == "remote":
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-blink-features=AutomationControlled")

            #Set webdriver for remote execution
            SELENIUM_HOST = config.SELENIUM_HOST
            SELENIUM_PORT = config.SELENIUM_PORT
        
            driver = webdriver.Remote(command_executor=f"http://{SELENIUM_HOST}:{SELENIUM_PORT}/wd/hub",
                                  options=options)
            print("Remote WebDriver setup successfully.")
            return driver
        
        #Set webdriver for local execution

        clean_webdriver_cache()  # Clean the WebDriver cache before setup
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        print("Local WebDriver setup successfully.")
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

        int_timestamp = int(datetime.now().timestamp())
        print(f"Atualização Cache: {int_timestamp}")

        REDIS_HOST = config.REDIS_HOST
        REDIS_PORT = config.REDIS_PORT

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        r.set('nasdaq_data', str_json)
        print("Data set in Redis.")

        r.set('timestamp', int_timestamp)
        
    except Exception as e:
        print(f"Error setting data in Redis: {e}")

def validate_cache_timestamp():
    """
    Validates the timestamp in Redis cache.
    """

    try:
        REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
        REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        int_cache_time = int(r.get('timestamp'))
        if int_cache_time:
            int_now_time = int(datetime.now().timestamp())
            int_diff = int_now_time - int_cache_time
            if int_diff < 300:
                print("Cache is valid.")
                return True
        
        print("Cache is invalid or expired.")
        return False
        
    except Exception as e:
        print(f"Error validating cache timestamp: {e}")
        return False


def main():

    driver = setup_webdriver()
    if driver:
        try:
            if not validate_cache_timestamp():
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
                df = order_by_change(df)
                print("DataFrame ordered by Change %.")

                if not df.empty:
                    set_redis_data(df)

        except Exception as e:
            print(f"Error during web extraction: {e}")

        finally:
            driver.quit()
            print("WebDriver Quit.")
        


if __name__ == "__main__":
    main()