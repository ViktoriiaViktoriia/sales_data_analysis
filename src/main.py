import pandas as pd
from src import logger
from src import load_data, clean_data, clean_extra_spaces, convert_to_datetime, convert_to_categorical, add_new_column
from src import (plot_total_sales, plot_regional_sales_by_year, plot_top_products, plot_msrp_distribution,
                 plot_msrp_vs_priceeach)


def discount_percentage_calc(df: pd.DataFrame) -> pd.Series:
    """
        Calculate the discount percentage for each row in a DataFrame.

        Formula: ((MSRP - PRICEEACH) / MSRP) * 100

        Args: df (pd.DataFrame): DataFrame containing 'MSRP' and 'PRICEEACH' columns.

        Returns:
        pd.Series: A Series containing discount percentages.
    """
    return ((df['MSRP'] - df['PRICEEACH']) / df['MSRP']) * 100


def main():
    """
        Main function to run the sales data analysis pipeline.
    """
    logger.info("Script execution started...")

    # Load data
    file_path = "data/sales_data_sample.csv"
    data = load_data(file_path, "ISO-8859-1")

    # Clean data
    cleaned_data = clean_data(data, ['PHONE', 'ADDRESSLINE2', 'POSTALCODE', 'STATE', 'TERRITORY',
                              'CONTACTLASTNAME', 'CONTACTFIRSTNAME'], True, True)

    cleaned_data = clean_extra_spaces(cleaned_data)

    cleaned_data = convert_to_datetime(cleaned_data, "ORDERDATE", "%m/%d/%Y %H:%M")

    cleaned_data = convert_to_categorical(cleaned_data, ["DEALSIZE", "STATUS"])

    # Add new column
    cleaned_data = add_new_column(cleaned_data, "DISCOUNT_PCT", discount_percentage_calc)
    print(cleaned_data.head())
    logger.info("Data cleaning was successfully completed.")

    fig = plot_total_sales(cleaned_data, "ORDERDATE", "SALES", "M")

    fig.write_html("reports/plot_total_sales.html", include_plotlyjs="cdn")
    logger.info("Plot saved successfully")

    fig = plot_regional_sales_by_year(cleaned_data, "SALES", "COUNTRY",
                                                    "YEAR_ID")
    fig.write_html("reports/plot_regional_sales.html", include_plotlyjs="cdn")
    logger.info("Plot saved successfully")

    fig = plot_top_products(cleaned_data, "PRODUCTLINE", "ORDERDATE", "COUNTRY",
                            "SALES", "M")

    fig.write_html("reports/plot_top_selling_products.html", include_plotlyjs="cdn")
    logger.info("Plot saved successfully")

    fig1, fig2 = plot_msrp_distribution(cleaned_data, "PRODUCTLINE", "MSRP", "SALES")

    fig1.write_html("reports/plot_total_sales_by_msrp.html", include_plotlyjs="cdn")
    logger.info("Plot saved successfully")

    fig2.write_html("reports/plot_individual_sales_by_msrp.html", include_plotlyjs="cdn")
    logger.info("Plot saved successfully")

    fig = plot_msrp_vs_priceeach(cleaned_data, "PRODUCTLINE", "MSRP", "PRICEEACH")

    fig.write_html("reports/plot_MSRP_vs_actual_price.html", include_plotlyjs="cdn")
    logger.info("Plot saved successfully")

    logger.info("Main function execution ended.")


if __name__ == '__main__':
    main()


