import pandas as pd
import plotly.express as px
from src import logger


def plot_total_sales(df: pd.DataFrame, date_column: str, sales_column: str, time_period: str) -> None:
    """
    Plot monthly total sales using Plotly.

    Args:
        df (pd.DataFrame): Cleaned data.
        date_column (str): Column name representing the date.
        sales_column (str): Column name for sales.
        time_period (str): The time period for aggregation: year ("Y"), quarter ("Q"), month ("M"), or day ("D").
    """
    try:
        logger.info("Plotting sales trends ...")

        # Check if required columns exist
        if date_column not in df.columns or sales_column not in df.columns:
            logger.error("Required columns not found in DataFrame.")
            return

        # Aggregate sales by date
        df["selected_time_period"] = df[date_column].dt.to_period(time_period).astype(str)
        total_sales_summary = df.groupby("selected_time_period")[sales_column].sum().reset_index()

        # Create interactive line plot
        fig = px.line(
            total_sales_summary,
            x=total_sales_summary["selected_time_period"],
            y=total_sales_summary[sales_column],
            title=f"Total Sales by {time_period}",
            labels={"y": "Date", "x": "Total Sales"},
            plot_color=["#145A32"]
        )

        # Customize hover template
        fig.update_traces(
            hovertemplate="Date = %{x}<br>Total sales = %{y}<extra></extra>",
            mode="markers+lines"
        )

        # Update layout
        fig.update_layout(
            title={
                "text": f"Total Sales by {time_period}",
                "x": 0.5,  # Center the title
                "xanchor": "center",
                "yanchor": "top"
            },

            xaxis_title="Date",
            yaxis_title="Total sales",
            xaxis=dict(tickangle=-45),
            bargap=0.2
        )

        fig.show()
        logger.info("Sales trends plotted successfully.")

    except Exception as e:
        logger.error(f"Error in plot_sales_trends: {e}")
        raise

