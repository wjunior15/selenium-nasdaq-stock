from tools.webdriver import setup_webdriver, get_nasdaq_data
from tools.process_data import order_by_change, build_dataframe
from tools.cache import set_redis_data, validate_cache_timestamp, get_redis_data
from config import config
import pandas as pd
from selenium.webdriver.common.by import By

def main():

    driver = setup_webdriver()
    if driver:
        try:
            if not validate_cache_timestamp():
                data = get_nasdaq_data(driver)

                if data:
                    df = build_dataframe(data)
                    df = order_by_change(df)

                    if not df.empty:
                        set_redis_data(df)


        except Exception as e:
            print(f"Fatal ERROR: {e}")

        finally:
            driver.quit()
            print("WebDriver Quit.")
            get_redis_data()


if __name__ == "__main__":
    main()