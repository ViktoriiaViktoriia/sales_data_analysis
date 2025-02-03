# Sales Data Analysis Project

## 📄 Overview
This project focuses on creating modular and maintainable data processing scripts for efficient data analysis and visualization. The structure is designed with separate modules for data loading, cleaning, and visualization. It analyzes sales data to identify trends and provide meaningful insights, such as total sales, top-selling products, bestsellers by region, average deal size, and total sales by MSRP.

## 🗂️ Project Structure
| Directory        | Description                           |
|------------------|---------------------------------------|
| `project_name/`   | Root project directory               |
| ├── `data/`       | Raw and processed data files         |
| ├── `notebooks/`  | Jupyter notebooks for exploration    |
| ├── `src/`        | Source code for data processing      |
| │   ├── `data_cleaning.py`      | Data cleaning functions |
| │   ├── `data_visualization.py` | Data visualization functions |
| │   └── `main.py`               | Main script orchestrating tasks |
| ├── `tests/`      | Unit tests                           |
| └── `README.md`   | Project documentation                |

## 📊 Data source
[Sample Sales Data](https://www.kaggle.com/datasets/kyanyoga/sample-sales-data/data) is a dataset provided by Kaggle.

## ✅ Outcomes
- Data Cleaning: 
   - Drops unnecessary columns 
   - Handles missing values and duplicates
- Visualizations:
   - Sales distribution by region
   - Monthly sales performance
   - Top-selling products
   - Average deal size
   - Sales distribution by MSRP
   - Correlation matrix

## 🚀 How to Get Started
**1. Clone the Repository**
   ```bash
   git clone https://github.com/ViktoriiaViktoriia/sales_data_analysis.git
   cd sales_data_analysis
   ```
**2. Install Dependencies**
   ```bash
   pip install pandas
   pip install plotly
   pip install pytest
   ```
**3. Run the Main Script**
   ```bash
   python src/main.py
   ```

## 🧪 Tests
Run unit tests with:
   ```bash
   pytest tests/
   ```
## 🤝 Contributions
Your feedback and contributions are welcome! Submit issues or pull requests to collaborate.