import pandas as pd
import os
import pytest
from tests import mock_data, get_mock_csv_file
from src import load_data, clean_data, clean_extra_spaces, convert_to_datetime, convert_to_categorical


def test_load_data(get_mock_csv_file):
    file_path = get_mock_csv_file
    try:
        df = load_data(file_path, encoding="utf-8")
        assert isinstance(df, pd.DataFrame), "Function should return a pandas DataFrame"
        assert not df.empty, "DataFrame should not be empty"
        assert "Product" in df.columns, "Missing 'Product' column"
        assert len(df) == 6, "Unexpected row count"
    finally:
        os.remove(file_path)  # Clean up


def test_load_data_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_data("non_existent_file.csv")


def test_clean_data(mock_data):
    cleaned_data = clean_data(mock_data)
    assert 'Sales' in cleaned_data.columns
