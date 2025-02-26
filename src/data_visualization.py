import pandas as pd
import plotly.express as px
from typing import Union
import plotly.graph_objects as go
from src import logger


def plot_total_sales(
        df: pd.DataFrame,
        date_column: str,
        sales_column: str,
        time_period: str) -> Union[go.Figure, None]:
    """
    Plot monthly total sales using Plotly.

    Args:
        df (pd.DataFrame): Cleaned data.
        date_column (str): Column name representing the date.
        sales_column (str): Column name for sales.
        time_period (str): The time period for aggregation: year ("Y"), quarter ("Q"), month ("M"), or day ("D").

    Returns:
        go.Figure, None: Plot appears or nothing.
    """
    try:
        logger.info("Plotting sales trends ...")

        # Check if required columns exist
        if date_column not in df.columns or sales_column not in df.columns:
            logger.error("Required columns not found in DataFrame.")
            return

        # Ensure the date_column is in datetime format
        df[date_column] = pd.to_datetime(df[date_column], errors="raise")

        # Aggregate sales by date
        df["selected_time_period"] = df[date_column].dt.to_period(time_period).astype(str)
        total_sales_summary = df.groupby("selected_time_period")[sales_column].sum().reset_index()

        # Create interactive line plot
        fig = px.line(
            total_sales_summary,
            x=total_sales_summary["selected_time_period"],
            y=total_sales_summary[sales_column],
            title=f"Total Sales",
            labels={"y": "Date", "x": "Total Sales"},
            color_discrete_sequence=["#145A32"]
        )

        # Customize hover template
        fig.update_traces(
            hovertemplate="Date = %{x}<br>Total sales = %{y}<extra></extra>",
            mode="markers+lines"
        )

        # Update layout
        fig.update_layout(
            title={
                "text": "Total Sales",
                "x": 0.5,  # Center the title
                "xanchor": "center",
                "yanchor": "top"
            },

            xaxis_title="Date",
            yaxis_title="Total sales",
            xaxis=dict(tickangle=-45),
            bargap=0.2
        )

        logger.info("Sales trends plotted successfully.")
        return fig

    except Exception as e:
        logger.error(f"Error in plot_sales_trends: {e}")
        return None


def plot_regional_sales_by_year(
    df: pd.DataFrame,
    sales_column: str,
    country_column: str,
    year_column: str
) -> Union[go.Figure, None]:
    """
    Creates a bar plot of total sales by region over time.

    Args:
        df (pd.DataFrame): The input DataFrame containing sales data.
        sales_column (str): The column representing total sales.
        country_column (str): The column representing the region (country).
        year_column (str): The column representing years.

    Returns:
        go.Figure, None: A Plotly bar chart figure appears,
                          or None if an error occurs.
    """

    try:
        logger.info("Starting regional sales visualization.")

        # Check if required columns exist in DataFrame
        missing_columns = [col for col in [sales_column, country_column, year_column] if col not in df.columns]
        if missing_columns:
            logger.error("Required columns not found in DataFrame.")
            raise

        # Aggregate sales by region
        regional_sales = df.groupby([country_column, year_column])[sales_column].sum().reset_index()
        logger.info("Data successfully processed.")

        # Create the bar plot
        fig = px.bar(
            regional_sales,
            x=regional_sales[year_column],
            y=regional_sales[sales_column],
            color=regional_sales[country_column],
            barmode="group",
            labels={'y': 'Total sales', 'x': 'Year', 'color': 'Country'}
        )

        # Assign country info to customdata
        fig.for_each_trace(
            lambda trace: trace.update(
                customdata=regional_sales[regional_sales[country_column] == trace.name][[country_column]]
            )
        )

        # Customize hover template
        fig.update_traces(
            hovertemplate="Country = %{customdata}<br>Year = %{x}<br>Total sales = %{y}<extra></extra>"
        )

        # Update layout
        fig.update_layout(
            title={
                "text": "Regional Sales Performance Over Time",
                "x": 0.5,  # Center the title
                "xanchor": "center",
                "yanchor": "top"
            },

            xaxis_title="Year",
            yaxis_title="Total sales",
            xaxis=dict(tickangle=-45),
            bargap=0.2
        )

        logger.info("Regional sales plot successfully created.")
        return fig

    except Exception as e:
        logger.exception(f"An error occurred while creating the sales plot: {e}")
        return None
