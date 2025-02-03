#Functions for loading, cleaning, and transforming data.

import pandas as pd

# Data loading function
def load_data(file_path, encoding='utf-8'):
    """
    Loads a dataset from a given filepath with a specified encoding.

    Args:
    - file_path (str): The path to the dataset file.
    - encoding (str): The encoding of the file. Default is 'utf-8'.

    Returns:
    - pd.DataFrame: A DataFrame containing the loaded data.

    Raises:
    - Exception: If an error occurs while loading the file (e.g., file not found, invalid format, etc.).
    """
    try:
        df = pd.read_csv(file_path, encoding=encoding)
        print(f"Data loaded successfully from {file_path}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Data cleaning function
def clean_data(df, columns_to_drop=None, drop_na=False):
    """
    Cleans the given dataframe by handling missing values, dropping specified columns, and removing duplicates.

    Args:
        df (pandas.DataFrame): The input dataframe to be cleaned.
        columns_to_drop (list, optional): List of column names to drop from the dataframe. Default is None.
        drop_na (bool, optional): If True, rows with missing values will be dropped. If False, missing values will be filled. Default is False.

    Returns:
        pandas.DataFrame: The cleaned dataframe with specified columns dropped, missing values handled, and duplicates removed.

    Raises:
        Exception: If an error occurs during the cleaning process (e.g., invalid dataframe, incorrect column names).
    """
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop, axis=1)

    if drop_na:
        df = df.dropna()
    else:
        # Impute missing data instead
        df = df.fillna(df.mean())  # Example imputation

    df = df.drop_duplicates()
    return df
