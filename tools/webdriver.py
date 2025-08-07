import os
import shutil
import platform
from config import config
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By


def clean_webdriver_cache():
    """
    Cleans the webdriver cache by removing the 'webdriver' directory
    if it exists in the current working directory.
    """

    sys_name = platform.system()
    if sys_name == 'Windows':
        cache_path = os.path.join(os.environ['USERPROFILE'], '.wdm')
    else:
        cache_path = os.path.expanduser("~/.wdm")
    
    if os.path.exists(cache_path):
        try:
            # Attempt to remove the directory and its contents
            shutil.rmtree(cache_path)
            print(f"Successfully removed webdriver cache at: {cache_path}")
            return
        except Exception as e:
            print(f"Error removing webdriver cache: {e}")
            return
    
    print("No webdriver cache found to clean.")
    return

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
    
def get_nasdaq_data(in_driver):
    try:
            in_driver.set_page_load_timeout(config.SELENIUM_TIMEOUT)
            in_driver.implicitly_wait(10)
            
            in_driver.get("https://www.investing.com/indices/nq-100-components")
            print("Opened", in_driver.title)

            stock_table = in_driver.find_elements(By.TAG_NAME, "table")
            print("Found stock table on the page. - Tables found:", len(stock_table))

            rows = stock_table[1].find_elements(By.TAG_NAME, "tr")
            print(f"Found {len(rows)} rows in the stock table.")

            data = []
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                row_data = [col.text for col in cols]
                data.append(row_data)

            return data
    except Exception as e:
        print(f"Error during web extraction: {e}")
        return None