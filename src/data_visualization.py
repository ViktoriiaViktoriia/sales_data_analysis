import pandas as pd
import plotly.express as px
import pycountry
from typing import Union
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.figure import Figure

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


# Function to get ISO-3 country codes
def get_iso3_country_codes(country_name):
    try:
        return pycountry.countries.lookup(country_name).alpha_3
    except LookupError:
        return None  # If not found, return None


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

        # Group by country and calculate average sales over years
        avg_regional_sales = regional_sales.groupby("COUNTRY")["SALES"].mean().reset_index()

        avg_regional_sales.columns = ["COUNTRY", "AVERAGESALES"]

        # Apply function to create new column with ISO-3 codes
        avg_regional_sales["ISO_CODES"] = avg_regional_sales["COUNTRY"].apply(get_iso3_country_codes)

        fig2 = px.choropleth(
            avg_regional_sales,
            locations="ISO_CODES",
            color="AVERAGESALES",
            hover_name="COUNTRY",
            hover_data={"ISO_CODES": False},
            color_continuous_scale="Viridis",  # Color scale
            projection="natural earth",  # Map projection type
            title="Average Regional Sales Performance (2003-2005)",
            labels={"ISO_CODES": "ISO-3 code", "AVERAGESALES": 'Average sales', "COUNTRY": "Country"}
        )

        # Update layout
        fig2.update_layout(
            title={
                "x": 0.45,  # Center the title
                "xanchor": "center",
                "yanchor": "top"
            }
        )

        logger.info("Regional sales plot successfully created.")
        logger.info("Average regional sales plot saved successfully")
        return fig, fig2

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
            labels={"PRODUCTLINE": "Product", "SALES": "Sales"},
            color_discrete_sequence=["#C75AA1", "#A7CA91", "#C85D00", "#042F9A", "#B4C0E7", "#FFD5E1", "#CB0536"]
        )

        fig1.update_layout(
            xaxis_title="MSRP",
            yaxis_title="Total Sales",
            title=dict(
                text="Total Sales Distribution by MSRP",
                x=0.5,  # Center the title
                xanchor="center",
                yanchor="top",
                y=0.95,
                font=dict(
                    size=24,
                    weight="bold"
                )
            ),
            margin=dict(t=110)
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
            labels={"PRODUCTLINE": "Product", "SALES": "Sales"}
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


def plot_msrp_vs_priceeach(
        df: pd.DataFrame,
        products_column: str,
        msrp_column: str,
        price_column: str) -> Union[go.Figure, None]:
    """
    Plot to compare the MSRP with the PRICEEACH to understand the markup or discount offered to customers.
    The scatter plot helps to determine which product has the best balance of MSRP and actual price.

    Args:
        df (pd.DataFrame): Cleaned data.
        products_column (str): Column name for products.
        msrp_column (str): The column representing the manufacturer's suggested retail price (MSRP).
        price_column (str): Column name for actual price / sale price / final price (PRICEEACH).

    Returns:
        go.Figure, None: Plot appears or nothing.
    """
    try:
        logger.info("Plotting MSRP vs PRICEEACH started...")

        # Check if required columns exist in DataFrame
        missing_columns = [col for col in [price_column, msrp_column, products_column]
                           if col not in df.columns]
        if missing_columns:
            logger.error("Required columns not found in DataFrame.")
            raise

        # MSRP vs Sale price by Product Category
        grouped_df = df.groupby(["PRODUCTLINE"])[["MSRP", "PRICEEACH"]].mean().reset_index()

        grouped_melted_df = grouped_df.melt(
            id_vars="PRODUCTLINE",
            value_vars=["MSRP", "PRICEEACH"],
            var_name="PRICETYPE",
            value_name="PRICEVALUE"
        )

        # Rename "PRICEEACH" to "Sale price" in "PRICETYPE"
        grouped_melted_df["PRICETYPE"] = grouped_melted_df["PRICETYPE"].replace({
            "PRICEEACH": "Sale price",
            "MSRP": "MSRP"  # Keep MSRP unchanged
        })

        fig = px.scatter(
            grouped_melted_df,
            x="PRODUCTLINE",
            y="PRICEVALUE",
            color="PRICETYPE",
            labels={"PRICETYPE": "Price type", "PRODUCTLINE": "Product", "PRICEVALUE": "Price value"},
            title="MSRP vs Sale price per Product"
        )

        fig.update_layout(
            xaxis_title="Product",
            yaxis_title="MSRP vs Sale price",
            xaxis_tickangle=-45,
            title={
                "x": 0.5,  # Center the title
                "xanchor": "center",
                "yanchor": "top"
            }
        )
        logger.info("Plotting MSRP vs PRICEEACH completed successfully.")

        return fig

    except Exception as e:
        logger.error(f"Error in plot_msrp_distribution: {e}")
        return None


def plot_sales_price_quantityordered(
        df: pd.DataFrame,
        products_column: str,
        quantityordered_column: str,
        sales_column: str,
        msrp_column: str,
        price_column: str) -> Union[Figure, None]:
    """
    Figure shows average MSRP and PRICEEACH per product, with analysis of total sales and quantity ordered.
    This visualization helps identify discount impact, and products with the highest demand,
    making it useful for pricing strategy and sales performance evaluation.

    Args:
        df (pd.DataFrame): Cleaned data.
        products_column (str): Column name for products.
        quantityordered_column (str): The column name represents quantity ordered.
        sales_column (str): Column name for sales.
        msrp_column (str): The column representing the manufacturer's suggested retail price (MSRP).
        price_column (str): Column name for actual price / sale price / final price (PRICEEACH).

    Returns:
        Figure: Returns figure.
    """
    try:
        logger.info("Plotting sales, price, quantity ordered started...")

        # Check if required columns exist in DataFrame
        missing_columns = [col for col in [price_column, msrp_column, products_column, sales_column,
                                           quantityordered_column] if col not in df.columns]
        if missing_columns:
            logger.error("Required columns not found in DataFrame.")
            raise

        # Group by product
        df_grouped = df.groupby("PRODUCTLINE").agg({
            "MSRP": "mean",  # Get mean MSRP
            "PRICEEACH": "mean",  # Get mean sale price
            "SALES": "sum",  # Sum of total sales
            "QUANTITYORDERED": "sum"  # Sum of quantity ordered
        }).reset_index()

        # Reshape the data using melt()
        df_melted = df_grouped.melt(
            id_vars=["PRODUCTLINE", "SALES", "QUANTITYORDERED"],
            value_vars=["MSRP", "PRICEEACH"],
            var_name="PRICETYPE",
            value_name="PRICE"
        )

        # Create figure
        fig, ax = plt.subplots(figsize=(20, 35))

        # Normalize quantity ordered for color mapping
        cmap = plt.get_cmap("coolwarm")

        msrp_df = df_melted[df_melted["PRICETYPE"] == "MSRP"]

        # Scatter plot for MSRP
        scatter_msrp = ax.scatter(
            msrp_df["PRICE"], msrp_df["SALES"],
            c=msrp_df["QUANTITYORDERED"],  cmap=cmap,
            alpha=0.8, edgecolors="black", marker="^", label="MSRP", s=400
        )

        priceeach_df = df_melted[df_melted["PRICETYPE"] == "PRICEEACH"]

        # Scatter plot for Sale price (PRICEEACH)
        ax.scatter(
            priceeach_df["PRICE"], priceeach_df["SALES"],
            c=priceeach_df["QUANTITYORDERED"], cmap=cmap,
            alpha=0.8, edgecolors="black", marker="o", label="Sale Price", s=400
        )

        # Add Product name annotations
        for i, row in df_melted.iterrows():
            ax.annotate(row["PRODUCTLINE"], (row["PRICE"], row["SALES"] + 70000),
                        fontsize=12, color="black", ha="center")

        # Labels and Title
        ax.set_xlabel("Price [MSRP & Sale Price]", fontsize=18, labelpad=15)
        ax.set_ylabel("Total sales", fontsize=18, labelpad=15)
        ax.set_title("MSRP vs. Sale Price with Analysis of Sales and Quantity Ordered", fontsize=22, pad=20)

        # Increase font size for tick labels
        ax.tick_params(axis="both", which="major", labelsize=16)

        # Add color bar for quantity ordered
        cbar = plt.colorbar(scatter_msrp, ax=ax)
        cbar.set_label("Quantity ordered", fontsize=18)

        # Format color bar labels to show 'k'
        cbar.ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x/1000)}k"))

        # Move legend outside
        ax.legend(loc="upper left", bbox_to_anchor=(1.2, 1), borderpad=1.7, labelspacing=1.6)

        plt.ylim(100000, 4200000)
        plt.xlim(70, 123)

        # Save the figure
        plt.savefig("reports/plot_sales_prices_quantityordered.jpg", format="jpg", dpi=300, bbox_inches="tight")
        logger.info("Plotting quantity ordered completed successfully. Image saved.")
        return fig

    except Exception as e:
        logger.error(f"Error in plot_sales_prices_quantityordered: {e}")
        return None


def plot_discount_pricing_strategy(
        df: pd.DataFrame,
        products_column: str,
        date_column: str,
        discount_column: str) -> Union[go.Figure, None]:
    """
    Plot demonstrate pricing strategy over time, rolling average discount by product.

    Args:
        df (pd.DataFrame): Cleaned data.
        products_column (str): Column name for products.
        date_column (str): The column representing the date / period.
        discount_column (str): Column name for discount (%).

    Returns:
        go.Figure, None: Plot appears or nothing.
    """

    try:
        logger.info("Plotting discount by product over time...")

        # Check if required columns exist in DataFrame
        missing_columns = [col for col in [products_column, date_column,
                                           discount_column] if col not in df.columns]
        if missing_columns:
            logger.error("Required columns not found in DataFrame.")
            raise

        # Filter only valid discounts (Discount > 0)
        discount_filtered_df = df[df["DISCOUNT_PCT"] > 0]

        # Group by date and product and calculate the average discount percentage
        df_grouped_discount = (
            discount_filtered_df.groupby(["ORDERDATE", "PRODUCTLINE"])
            .agg({"DISCOUNT_PCT": "mean"})
            .reset_index()
        )

        # Group by product, and apply rolling window for discount calculation
        df_grouped_discount["ROLLING_AVG_DISCOUNT_%"] = (
            df_grouped_discount.groupby("PRODUCTLINE")["DISCOUNT_PCT"]
            .rolling(window=30)
            .mean()
            .reset_index(level=0, drop=True)
        )

        # Create Line Chart
        fig = px.line(
            df_grouped_discount,
            x="ORDERDATE",
            y="ROLLING_AVG_DISCOUNT_%",
            color="PRODUCTLINE",
            title="Pricing Strategy: Rolling Average Discount by Product Over Time",
            labels={"ROLLING_AVG_DISCOUNT_%": "Discount (%)", "ORDERDATE": "Date", "PRODUCTLINE": "Product"},
        )

        # Customize layout
        fig.update_layout(
            xaxis_title="Date",
            xaxis=dict(range=["2003-08-01", "2005-07-31"]),  # Set the date range
            yaxis_title="Rolling average discount (%)",
            legend_title="Product",
            hovermode="x unified",
            width=1000,  # Width in pixels
            height=700,  # Height in pixels
            title={
                "x": 0.5,  # Center the title
                "xanchor": "center",
                "yanchor": "top"
            }
        )
        logger.info("Plotting discount pricing strategy completed successfully.")
        return fig

    except Exception as e:
        logger.error(f"Error in plot_pricing_strategy: {e}")
        return None


def plot_dealsize_trends(
        df: pd.DataFrame,
        dealsize_column: str,
        date_column: str) -> Union[go.Figure, None]:
    """
    Plot demonstrate pricing strategy over time, rolling average discount by product.

    Args:
        df (pd.DataFrame): Cleaned data.
        dealsize_column (str): Column name for deal sizes.
        date_column (str): The column representing the date / period.

    Returns:
        go.Figure, None: Plot appears or nothing.
    """

    try:
        logger.info("Plotting deal size trends over time...")

        # Check if required columns exist in DataFrame
        missing_columns = [col for col in [date_column,
                                           dealsize_column] if col not in df.columns]
        if missing_columns:
            logger.error("Required columns not found in DataFrame.")
            raise

        # Count deal sizes per date
        df_grouped_dealsize = (
            df.groupby(["ORDERDATE", "DEALSIZE"], observed=False)
            .size()
            .reset_index(name="COUNTDEALS")
        )

        # Stacked area chart
        fig = px.area(
            df_grouped_dealsize,
            x="ORDERDATE",
            y="COUNTDEALS",
            color="DEALSIZE",
            title="Deal Size Trends Over Time",
            labels={"ORDERDATE": "Order date", "DEALSIZE": "Deal size", "COUNTDEALS": "The number of deals"},
            color_discrete_sequence=["#7C6DAA", "gold", "olive"]
        )

        # Customize layout
        fig.update_layout(
            title=dict(
                x=0.5,  # Center the title
                xanchor="center",
                yanchor="top",
                y=0.95,
                font=dict(
                    size=24,
                    weight="bold"
                )
            ),
            margin=dict(t=120)
        )
        logger.info("Plotting deal size trends completed successfully.")
        return fig

    except Exception as e:
        logger.error(f"Error in plot_pricing_strategy: {e}")
        return None


def plot_rfm(
        df: pd.DataFrame,
        ordernumber_column: str,
        orderdate_column: str,
        customername_column: str,
        sales_column: str) -> Union[go.Figure, None]:
    """
    RFM Analysis: 3D scatter plot visualize three metrics: Recency (x-axis), how recent each customer purchased,
    Frequency (y-axis), how often each customer purchased, Monetary(z-axis), total sales per customer,
    how much each customer spent.

    Args:
        df (pd.DataFrame): Cleaned data.
        ordernumber_column (str): Column name for number of orders.
        orderdate_column (str): The column representing the date of order.
        customername_column (str): The column represents customer name.
        sales_column (str): Column name for sales.

    Returns:
        go.Figure, None: Plot appears or nothing.
    """

    try:
        logger.info("Plotting rfm...")

        # Check if required columns exist in DataFrame
        missing_columns = [col for col in [ordernumber_column, orderdate_column,
                                           customername_column, sales_column] if col not in df.columns]
        if missing_columns:
            logger.error("Required columns not found in DataFrame.")
            raise

        # Check that each order includes multiple items
        df.groupby("ORDERNUMBER").size().describe()

        # Group customers based on their purchase behavior
        # RFM Analysis (Recency, Frequency, Monetary)
        # Last date in the dataset
        analysis_date = df["ORDERDATE"].max()

        rfm = df.groupby("CUSTOMERNAME").agg(
            Recency=("ORDERDATE", lambda x: (analysis_date - x.max()).days),
            Frequency=("ORDERNUMBER", "nunique"),  # Count of unique orders per customer
            Monetary=("SALES", "sum")  # Total spending per customer
        ).reset_index()

        # Assuming 'rfm' DataFrame contains 'Recency', 'Frequency', 'Monetary'
        fig = px.scatter_3d(
            rfm,
            x="Recency",
            y="Frequency",
            z="Monetary",
            color="Monetary",  # Color points based on spending
            labels={"Recency": "Recency (Days)<br>(How recently a customer made a purchase)",
                    "Frequency": "Frequency<br>(Orders per customer. <br>How often a customer buys)",
                    "Monetary": 'Monetary Value<br>(Total sales per customer.<br> How much a customer has spent)'},
            title="3D Visualization of Recency, Frequency, and Monetary")

        # Increase figure size
        fig.update_layout(
            width=1200,
            height=850,
            title={
                "x": 0.5,  # Center the title
                "xanchor": "center",
                "yanchor": "top"
            }
        )

        # 3 pie charts for RFM show how customers are distributed within each metric.
        rfm["Recency_Metric"] = pd.cut(rfm["Recency"], bins=[0, 30, 90, 180, 270, 365, rfm["Recency"].max()],
                                       labels=["Very recent customers: 0-30 days", "Recent customers: 31-90 days",
                                               "Occasional customers: 91-180 days",
                                               "Medium-engagement customers: 181-270 days",
                                               "Low-engagement customers: 271-365 days",
                                               "Inactive customers: 365+ days"],
                                       duplicates="drop")

        rfm["Frequency_Metric"] = pd.cut(rfm["Frequency"], bins=[1, 2, 4, 6, 26],
                                         labels=["Rare buyers: 1-2 orders", "Occasional buyers: 3-4 orders",
                                                 "Frequent buyers: 5-6 orders", "Very frequent buyers: 7+ orders"])

        rfm["Monetary_Metric"] = pd.cut(rfm["Monetary"],
                                        bins=[0, 200000, 400000, 600000, 800000, rfm['Monetary'].max()],
                                        labels=["0-200k", "200k-400k", "400k-600k", "600k-800k", "800k+"],
                                        duplicates="drop")

        # Create summary for each metric
        recency_counts = rfm["Recency_Metric"].value_counts().reset_index()
        recency_counts.columns = ["Category", "Count"]

        frequency_counts = rfm["Frequency_Metric"].value_counts().reset_index()
        frequency_counts.columns = ["Category", "Count"]

        monetary_counts = rfm["Monetary_Metric"].value_counts().reset_index()
        monetary_counts.columns = ["Category", "Count"]

        # Generate three pie charts
        fig1 = px.pie(recency_counts, names="Category", values="Count", title="Customer Recency Distribution",
                      color_discrete_sequence=["lightgreen", "#F4A7A8", "#5872E6", "#ADBBB0", "#97664E", "gold"])
        fig2 = px.pie(frequency_counts, names="Category", values="Count", title="Customer Frequency Distribution",
                      color_discrete_sequence=["#C2C6B3", "#68703E", "#B8A3B0", "#4C7588"])
        fig3 = px.pie(monetary_counts, names="Category", values="Count", title="Customer Monetary Distribution",
                      color_discrete_sequence=["#5B0868", "#97B5C9", "#ECCC09", "#DC0863", "#3FBF63"])

        fig1.update_layout(margin=dict(t=100), title=dict(y=0.95), legend_title="Categories:")
        fig2.update_layout(margin=dict(t=100), title=dict(y=0.95), legend_title="Categories:")
        fig3.update_layout(margin=dict(t=150), title=dict(y=0.95),
                           legend_title="Categories (How much a customer has spent):")

        logger.info("Plotting RFM 3D completed successfully.")

        return fig, fig1, fig2, fig3

    except Exception as e:
        logger.error(f"Error in plot_rfm: {e}")
        return None


