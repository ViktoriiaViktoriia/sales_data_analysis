import pandas as pd
import tempfile
import pytest


@pytest.fixture
def mock_data():
    """Creates mock data for testing purposes."""
    data = {
        "Product": ["A", "B", "C", "B", "A", "D", "E"],
        "Sales": [300, 450, 500, 450, 300, 250, 400],
        "Date": ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-02", "2025-01-01", "2024-11-30", "2024-10-31"],
        "Year": ["2025", "2025", "2025", "2025", "2025", "2024", "2024"],
        "Region": ["North", "South", "East", "South", "North", "West", "West"],
        "Postal code": ["12345", "32456", "23456", "54321", "34234", "12121", "12121"],
        "Deal size": ["Small", "Medium", "Large", "Medium", "Small", "Small", "Medium"]
    }
    return pd.DataFrame(data)


@pytest.fixture
def get_mock_csv_file(mock_data):
    """Create a temporary CSV file with mock data."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    mock_data.to_csv(temp_file.name, index=False)
    return temp_file.name
