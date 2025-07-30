import os
import shutil
import platform

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