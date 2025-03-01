# Functions for loading, cleaning, and converting data.

import pandas as pd
from typing import List, Optional
from src import logger


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
        logger.info(f"Data loaded successfully from {file_path}")
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise e   # Re-raise the error to stop further processing
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise ValueError(f"Unexpected error while loading data: {e}")
    return df


# Data cleaning function
def clean_data(
    df: pd.DataFrame,
    columns_to_drop: Optional[List[str]] = None,
    drop_na: bool = False,
    drop_duplicates: bool = False
) -> pd.DataFrame:
    """
    Cleans the dataframe by dropping specified columns, optionally dropping rows with missing values,
    and removing duplicates.

    Args:
        df (pandas.DataFrame): The dataframe to clean.
        columns_to_drop (list, optional): List of column names to drop from the dataframe. Default is None.
        drop_na (bool, optional): If True, rows with missing values will be dropped. Default is False.
        drop_duplicates (bool): If true, duplicated rows will be dropped. Default is False.

    Returns:
        pandas.DataFrame: The cleaned dataframe with specified columns dropped, missing values handled,
        and duplicates removed.

    Raises:
        Exception: If an error occurs during the cleaning process (e.g., invalid dataframe, incorrect column names).
    """
    logger.info("Starting data cleaning process.")

    if columns_to_drop:
        logger.info(f"Dropping columns: {columns_to_drop}")
        df = df.drop(columns=columns_to_drop, axis=1)

    if drop_na:
        logger.info("Dropping rows with NaN values.")
        df = df.dropna()

    if drop_duplicates:
        logger.info(f"Removing {df.duplicated().sum()} duplicate rows.")
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
        logger.info("Removing extra spaces from all string columns. Data cleaning process completed.")
        df[column] = df[column].str.strip().replace(r'\s+', ' ', regex=True)

    return df


logger.info("Starting data conversion process.")


def convert_to_datetime(df: pd.DataFrame, column_name: str, date_format: str = None) -> pd.DataFrame:
    """
    Convert a specified column to datetime format.

    Args:
        df (pd.DataFrame): The input DataFrame containing the column.
        column_name (str): The column to convert.
        date_format (str, optional): Expected date format (e.g., "%Y-%m-%d"). Defaults to None.

    Returns:
        pd.DataFrame: DataFrame with the column converted to datetime.
    """
    try:
        df[column_name] = pd.to_datetime(df[column_name], format=date_format, errors='raise')
        logger.info(f"Column '{column_name}' successfully converted to datetime.")
    except ValueError as e:
        logger.error(f"ValueError occurred while converting column '{column_name}' to datetime: {e}")
        raise ValueError("Date conversion failed due to invalid or out-of-range date.") from e
    except Exception as e:
        logger.error(f"Unexpected error occurred while converting column '{column_name}' to datetime: {e}")
        raise e
    return df


def convert_to_categorical(df: pd.DataFrame, column_name: Optional[List[str]]) -> pd.DataFrame:
    """
    Convert a specified column to categorical type.

    Args:
        df (pd.DataFrame): The input DataFrame containing the column.
        column_name (str): The column to convert.

    Returns:
        pd.DataFrame: DataFrame with the column converted to categorical.
    """
    try:
        df[column_name] = df[column_name].astype('category')
        logger.info(f"Column '{column_name}' successfully converted to categorical type.")
    except KeyError as e:
        logger.error(f"Column '{column_name}' does not exist: {e}")
        raise
    except TypeError as e:
        logger.error(f"TypeError occurred while converting column '{column_name}' to categorical: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error occurred while converting column '{column_name}' to categorical: {e}")
        raise
    return df


logger.info("Data conversion process completed.")


def add_new_column(df: pd.DataFrame, new_column_name: str, column_computation_func) -> pd.DataFrame:
    """
    Adds a new column to the DataFrame based on a column computation.

    Args:
        df (pd.DataFrame): The input DataFrame.
        new_column_name (str): Name of the new column.
        column_computation_func (function): The column computation function tells the program how to calculate the
                                            values for the new column based on the existing data in the DataFrame.

    Returns:
        pd.DataFrame: DataFrame with the new column added.

    Raises:
        ValueError: If the calculation function does not return a valid Series or a new column name already exists.
    """
    try:
        if new_column_name in df.columns:
            raise ValueError(f"Column '{new_column_name}' already exists.")

        # Apply the calculation function to each row
        df[new_column_name] = df.apply(column_computation_func, axis=1)
        logger.info(f"Successfully added new column '{new_column_name}'.")
    except ValueError as e:
        logger.error(f"Error adding column: {e}")
        raise  # Rethrow the exception for external handling if needed
    except Exception as e:
        logger.error(f"Error adding new column '{new_column_name}': {e}")
        raise
    return df
