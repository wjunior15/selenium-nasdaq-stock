import pandas as pd

def order_by_change(in_df):
    """
    Orders the DataFrame by the 'Change' column in descending order.
    """
    try:
        in_df["Change %"] = in_df["Change %"].str.replace('%', '').astype(float)
        in_df["Change %"].fillna(0, inplace=True)
        in_df.rename(columns={"Change %": "Change"}, inplace=True)

        ordered_df = in_df.sort_values(by='Change', ascending=False)
        return ordered_df
    except Exception as e:
        print(f"Error ordering DataFrame: {e}")
        return pd.DataFrame()