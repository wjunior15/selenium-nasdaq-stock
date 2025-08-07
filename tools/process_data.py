import pandas as pd
import numpy as np

def order_by_change(in_df):
    """
    Orders the DataFrame by the 'Change' column in descending order.
    """
    try:
        in_df["Change %"].dropna(inplace=True)
        in_df["Change %"] = in_df["Change %"].str.replace('%', '').astype(float)
        in_df.rename(columns={"Change %": "Change"}, inplace=True)
        ordered_df = in_df.sort_values(by='Change', ascending=False)
        print("DataFrame ordered by Change %.")
        return ordered_df
    
    except Exception as e:
        print(f"Error ordering DataFrame: {e}")
        return pd.DataFrame()
    
def build_dataframe(in_data):
    """
    Builds a DataFrame from the provided data.
    """
    try:
        df = pd.DataFrame(in_data)
        df = df.dropna()
        df.columns = ["Symbol", "Name", "Last Price", "High", "Low", "Change %", "Volume", "Upside", "Time"]
        df.drop(columns=["Symbol", "Upside"], inplace=True)        
        return df
    
    except Exception as e:
        print(f"Error building DataFrame: {e}")
        return pd.DataFrame()