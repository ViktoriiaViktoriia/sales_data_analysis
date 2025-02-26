import plotly.graph_objs as go
import plotly.io as pio
from src import plot_total_sales, plot_regional_sales_by_year
from tests import mock_data
import os


def test_plot_total_sales(mock_data):
    """Test that function plot_total_sales returns a valid Plotly figure."""
    # Call function to test
    fig = plot_total_sales(mock_data, "Date", "Sales", "M")
    print(mock_data.head())

    assert fig is not None

    fig.write_html("test_plot_total_sales.html")
    assert os.path.exists("test_plot_total_sales.html")
    os.remove("test_plot_total_sales.html")

    assert isinstance(fig, go.Figure)


def test_plot_regional_sales(mock_data):
    """Test that function plot_regional_sales_by_year returns a valid plotly figure."""
    # Call function to test
    fig = plot_regional_sales_by_year(mock_data, "Sales", "Region", "Year")

    assert fig is not None

    fig.write_html("test_plot_regional_sales.html")
    assert os.path.exists("test_plot_regional_sales.html")
    os.remove("test_plot_regional_sales.html")

    assert isinstance(fig, go.Figure)

    # Check if hovertemplate exists and matches expected template
    # Extract the hover template from the figure's data
    hovertemplate = fig.data[0].hovertemplate

    # Verify that the hovertemplate contains the expected parts
    assert "Country = %{customdata}" in hovertemplate
    assert "Year = %{x}" in hovertemplate
    assert "Total sales = %{y}" in hovertemplate
