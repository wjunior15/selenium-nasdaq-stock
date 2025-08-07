import redis
import pandas as pd
from config import config
from datetime import datetime

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
        REDIS_HOST = config.REDIS_HOST
        REDIS_PORT = int(config.REDIS_PORT)

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
    
def get_redis_data():
    """
    Gets the JSON data from Redis.
    """

    try:
        REDIS_HOST = config.REDIS_HOST
        REDIS_PORT = config.REDIS_PORT

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        str_json = r.get('nasdaq_data')
        
        if str_json:
            df = pd.read_json(str_json, orient="records", lines=True)
            print("Data retrieved from Redis:\n", df.head())
            return df
        
        print("No data found in Redis.")
        return None
        
    except Exception as e:
        print(f"Error getting data from Redis: {e}")
        return None