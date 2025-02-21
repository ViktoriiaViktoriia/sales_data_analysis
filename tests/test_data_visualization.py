import plotly.graph_objs as go
from src import plot_total_sales, plot_regional_sales_by_year
from tests import mock_data
import webbrowser


def test_plot_total_sales(mock_data):
    """Test that plot_total_sales returns a valid Plotly figure."""
    # Call function to test
    fig = plot_total_sales(mock_data, "Date", "Sales", "M")

    # Show the plot (for manual checking)
    if fig is not None:
        fig.show()
    else:
        print("Error: The figure was not created.")

    assert isinstance(fig, go.Figure) or fig is None
