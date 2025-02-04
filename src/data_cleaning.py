#Functions for loading, cleaning, and transforming data.

import pandas as pd
from typing import List, Optional

# Data loading function
def load_data(file_path: str, encoding: Optional[str] = "utf-8") -> pd.DataFrame:
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
        return pd.DataFrame()  # Return an empty DataFrame

# Data cleaning function
def clean_data(
    df: pd.DataFrame,
    columns_to_drop: Optional[List[str]] = None,
    drop_na: bool = False,
    drop_duplicates: bool = False
) -> pd.DataFrame:
    """
    Cleans the dataframe by dropping specified columns, optionally dropping rows with missing values, and removing duplicates.

    Args:
        df (pandas.DataFrame): The dataframe to clean.
        columns_to_drop (list, optional): List of column names to drop from the dataframe. Default is None.
        drop_na (bool, optional): If True, rows with missing values will be dropped. Default is False.
        drop_duplicates (bool): If true, duplicated rows will be dropped. Default is False.

    Returns:
        pandas.DataFrame: The cleaned dataframe with specified columns dropped, missing values handled, and duplicates removed.

    Raises:
        Exception: If an error occurs during the cleaning process (e.g., invalid dataframe, incorrect column names).
    """
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop, axis=1)

    if drop_na:
        df = df.dropna()

    if drop_duplicates:
        df = df.drop_duplicates()

    return df

def clean_extra_spaces(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove leading, trailing, and excess spaces from all string columns.

    Args:
        df (pd.DataFrame): DataFrame to clean.

    Returns:
        pd.DataFrame: Cleaned DataFrame with extra spaces removed.
    """
    string_columns = df.select_dtypes(include='object').columns

    for column in string_columns:
        df[column] = df[column].str.strip().replace(r'\s+', ' ', regex=True)

    return df
