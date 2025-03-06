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


def plot_top_products(
        df: pd.DataFrame,
        products_column: str,
        date_column: str,
        country_column: str,
        sales_column: str,
        time_period: str) -> Union[go.Figure, None]:
    """
    Plot top five best-selling products using Plotly.

    Args:
        df (pd.DataFrame): Cleaned data.
        products_column (str): Column name for products.
        date_column (str): The column representing the date.
        country_column (str): The column representing the region (country).
        sales_column (str): Column name for sales.
        time_period (str): The time period for aggregation: year ("Y"), quarter ("Q"), month ("M"), or day ("D").

    Returns:
        go.Figure, None: Plot appears or nothing.
    """
    try:
        logger.info("Plotting bestsellers ...")

        # Check if required columns exist in DataFrame
        missing_columns = [col for col in [sales_column, country_column, date_column, products_column]
                           if col not in df.columns]
        if missing_columns:
            logger.error("Required columns not found in DataFrame.")
            raise

        # Ensure the date_column is in datetime format
        df[date_column] = pd.to_datetime(df[date_column], errors="raise")

        # Aggregate sales by date
        df["selected_time_period"] = df[date_column].dt.to_period(time_period).astype(str)

        # Group by Product, Country, and Date, summing up the sales
        bestsellers = (
            df.groupby([products_column, country_column, "selected_time_period"])[sales_column]
            .sum()
            .reset_index()
        )

        # Sort best-selling products in descending order and get the top 5
        top_5_products = bestsellers.sort_values(sales_column, ascending=False).head(5)

        # Display the results
        print(top_5_products)

        # Create a bar chart
        fig = px.bar(
            top_5_products,
            x=top_5_products[products_column],
            y=top_5_products[sales_column],
            color=top_5_products[country_column],
            title="Top 5 Best-Selling Products",
            text="selected_time_period"
        )

        # Customize hover template
        fig.update_traces(
            hovertemplate="Product = %{x}<br>Sales = %{y}<br>Date = %{text}<extra></extra>"
        )

        # Update layout
        fig.update_layout(
            title={
                "text": "Top 5 Best-Selling Products",
                "x": 0.5,  # Center the title
                "xanchor": "center",
                "yanchor": "top"
            }
        )

        logger.info("Top 5 products by sales plotted successfully.")
        return fig

    except Exception as e:
        logger.error(f"Error in plot_top_products: {e}")
        return None


def plot_msrp_distribution(
        df: pd.DataFrame,
        products_column: str,
        msrp_column: str,
        sales_column: str) -> Union[go.Figure, None]:
    """
    Plot how MSRP is distributed across products to identify pricing outliers.
    Plots help to analyze if products with higher MSRP values contribute more to total sales.

    Args:
        df (pd.DataFrame): Cleaned data.
        products_column (str): Column name for products.
        msrp_column (str): The column representing the manufacturer's suggested retail price (MSRP).
        sales_column (str): Column name for sales.

    Returns:
        go.Figure, None: Plot appears or nothing.
    """

    try:
        logger.info("Plotting sales by MSRP ...")

        # Check if required columns exist in DataFrame
        missing_columns = [col for col in [sales_column, msrp_column, products_column]
                           if col not in df.columns]
        if missing_columns:
            logger.error("Required columns not found in DataFrame.")
            raise

        # Group by MSRP, Product, summing up the sales
        msrp_distribution_df = df.groupby(["MSRP", "PRODUCTLINE"])["SALES"].sum().reset_index()

        fig1 = px.histogram(
            msrp_distribution_df,
            x="MSRP",
            y="SALES",
            color="PRODUCTLINE",
            labels={"PRODUCTLINE": "Product"}
        )

        fig1.update_layout(
            xaxis_title="MSRP",
            yaxis_title="Total Sales",
            title={
                "text": "Total Sales Distribution by MSRP",
                "x": 0.5,  # Center the title
                "xanchor": "center",
                "yanchor": "top"
            }
        )

        logger.info("Total sales by MSRP plotted successfully.")

        # Scatter plot shows individual data points
        # Explore how MSRP is distributed across products to identify pricing outliers
        fig2 = px.scatter(
            msrp_distribution_df,
            x="MSRP",
            y="SALES",
            color="PRODUCTLINE",
            hover_data=["MSRP"],
            labels={"PRODUCTLINE": "Product"}
        )

        fig2.update_layout(
            xaxis_title="MSRP",
            yaxis_title="Individual Sales",
            title={
                "text": "Individual Sales Distribution by MSRP",
                "x": 0.5,  # Center the title
                "xanchor": "center",
                "yanchor": "top"
            }
        )

        logger.info("Individual sales by MSRP plotted successfully.")

        return fig1, fig2

    except Exception as e:
        logger.error(f"Error in plot_msrp_distribution: {e}")
        return None
