import pandas as pd
import os
import pytest
from tests import mock_data, get_mock_csv_file
from src import load_data, clean_data, clean_extra_spaces, convert_to_datetime, convert_to_categorical, add_new_column


def test_load_data(get_mock_csv_file):
    file_path = get_mock_csv_file
    try:
        df = load_data(file_path, encoding="utf-8")
        assert isinstance(df, pd.DataFrame), "Function should return a pandas DataFrame"
        assert not df.empty, "DataFrame should not be empty"
        assert "Product" in df.columns, "Missing 'Product' column"
        assert len(df) == 6, "Unexpected row count"
        assert df.shape[1] == 6, "Unexpected number of columns"
    finally:
        os.remove(file_path)  # Clean up


def test_load_data_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_data("non_existent_file.csv")


def test_clean_data(mock_data):
    cleaned_data = clean_data(mock_data, ["Postal code"], True, True)
    assert "Sales" in cleaned_data.columns
    assert "Postal code" not in cleaned_data.columns
    assert not cleaned_data.isna().any().any(), "There are NaN values in the DataFrame"
    assert not cleaned_data.duplicated().any(), "There are duplicate rows in the DataFrame"
    assert not cleaned_data.empty, "DataFrame is empty after cleaning"
    assert cleaned_data.shape[1] == 5, "Expected a different number of columns"


def test_clean_extra_spaces(mock_data):
    cleaned_data = clean_extra_spaces(mock_data)
    assert not cleaned_data.empty, "DataFrame is empty after cleaning"
    assert "Date" in cleaned_data.columns
    assert all(not col.startswith(" ") and not col.endswith(" ") for col in cleaned_data.columns), \
        "Extra spaces in column names"
    assert all((cleaned_data[col] != "").all() for col in cleaned_data.select_dtypes(include="object")), \
        "Empty strings found in DataFrame"
    assert all(
        not cleaned_data[col].str.contains(r'^\s|\s$', regex=True).any()
        for col in cleaned_data.select_dtypes(include="object")
    ), "Extra spaces found in string columns"


def test_convert_to_datetime(mock_data):
    cleaned_data = convert_to_datetime(mock_data, "Date", "%Y-%m-%d")
    assert pd.api.types.is_datetime64_any_dtype(cleaned_data["Date"]), "Column should be datetime"


def test_convert_to_datetime_value_error():
    df = pd.DataFrame({"dates": ["2023-02-30", "2023-13-01"]})
    with pytest.raises(ValueError, match="Date conversion failed due to invalid or out-of-range date."):
        convert_to_datetime(df, "dates", "%Y-%m-%d")


def test_convert_to_categorical(mock_data):
    cleaned_data = convert_to_categorical(mock_data, "Deal size")
    assert isinstance(cleaned_data["Deal size"].dtype, pd.CategoricalDtype)


def test_convert_to_categorical_type_error(mock_data):
    # Passing non-DataFrame object
    with pytest.raises(TypeError):
        convert_to_categorical("not_a_dataframe", "Deal size")


def test_convert_to_categorical_key_error(mock_data):
    # Invalid column name
    with pytest.raises(KeyError):
        convert_to_categorical(mock_data, "non_existent_column")


def test_add_new_column():
    # Mock DataFrame
    data = {"sales": [300, 700, 850], "costs": [250, 575, 660]}
    df = pd.DataFrame(data)

    # Inline computation function
    def calculate_profit(row):
        return row["sales"] - row["costs"]

    df_with_new_column = add_new_column(df, "profit", calculate_profit)

    # Assertions
    assert "profit" in df_with_new_column.columns
    assert all(df_with_new_column["profit"] == pd.Series([50, 125, 190]))

    # Test for exception when the column already exists
    with pytest.raises(ValueError, match="Column 'profit' already exists."):
        add_new_column(df_with_new_column, "profit", calculate_profit)

