"""
Data Exploration Script

This script creates basic exploratory visualizations from job market data:
1. Jobs distribution by year (pie chart)
2. Jobs per country (horizontal bar chart, top 100)
3. Jobs per website (vertical bar chart, top 100)

Input files: 
- query_results/jobs_per_year.csv
- query_results/jobs_per_country.csv
- query_results/jobs_per_website.csv

Output: PNG files in report/figures/ directory
"""

import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Add parent directory to path and set working directory
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

# Set high DPI and clean theme
plt.rcParams["figure.dpi"] = 600
plt.rcParams["savefig.dpi"] = 600
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.3
plt.rcParams["axes.facecolor"] = "white"
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["figure.figsize"] = (12, 8)

# Create figures directory if it doesn't exist
os.makedirs("report/figures", exist_ok=True)


def load_csv_without_headers(filename, col1_name, col2_name):
    """Load CSV without headers and assign column names"""
    try:
        df = pd.read_csv(filename, header=None, names=[col1_name, col2_name])
        
        # Convert the count column to numeric, handling any non-numeric values
        df.iloc[:, 1] = pd.to_numeric(df.iloc[:, 1], errors="coerce")
        
        # Remove rows with NaN values and convert to int
        df = df.dropna()
        df.iloc[:, 1] = df.iloc[:, 1].astype(int)
        
        return df
    except FileNotFoundError:
        return None
    except Exception as e:
        return None


def create_pie_chart(df, title, filename):
    """Create pie chart for job per year data"""
    if df is None:
        return

    plt.figure(figsize=(10, 8))
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(df)))
    
    plt.pie(df.iloc[:, 1], labels=df.iloc[:, 0], autopct="%1.1f%%", 
            startangle=90, colors=colors, textprops={"fontsize": 10})
    
    plt.title(title, fontsize=16, fontweight="bold", pad=20)
    plt.axis("equal")
    plt.tight_layout()
    
    plt.savefig(f"report/figures/{filename}", dpi=300, bbox_inches="tight", format="png")
    plt.close()


def create_horizontal_bar_plot(df, title, filename, limit=100):
    """Create horizontal bar plot for jobs per country"""
    if df is None:
        return

    # Take first entries and sort by count
    df_subset = df.head(limit).sort_values(df.columns[1], ascending=True)

    plt.figure(figsize=(12, max(8, len(df_subset) * 0.3)))

    colors = plt.cm.viridis(np.linspace(0, 1, len(df_subset)))
    bars = plt.barh(df_subset.iloc[:, 0], df_subset.iloc[:, 1], color=colors)

    plt.xlabel("Count", fontsize=12, fontweight="bold")
    plt.ylabel("Country", fontsize=12, fontweight="bold")
    plt.title(title, fontsize=16, fontweight="bold", pad=20)

    # Add value labels on bars
    max_value = df_subset.iloc[:, 1].max()
    for i, bar in enumerate(bars):
        plt.text(
            bar.get_width() + max_value * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{int(df_subset.iloc[i, 1])}",
            va="center",
            fontsize=8,
        )

    plt.tight_layout()
    plt.savefig(f"report/figures/{filename}", dpi=300, bbox_inches="tight", format="png")
    plt.close()


def create_vertical_bar_plot(df, title, filename, limit=100):
    """Create vertical bar plot for jobs per website"""
    if df is None:
        return

    # Take first entries and sort by count
    df_subset = df.head(limit).sort_values(df.columns[1], ascending=False)

    plt.figure(figsize=(15, 8))

    colors = plt.cm.plasma(np.linspace(0, 1, len(df_subset)))
    bars = plt.bar(range(len(df_subset)), df_subset.iloc[:, 1], color=colors)

    plt.xlabel("Website", fontsize=12, fontweight="bold")
    plt.ylabel("Count", fontsize=12, fontweight="bold")
    plt.title(title, fontsize=16, fontweight="bold", pad=20)

    # Set x-axis labels with rotation
    plt.xticks(range(len(df_subset)), df_subset.iloc[:, 0], rotation=90, ha="right", fontsize=8)

    # Add value labels on top of bars
    max_value = df_subset.iloc[:, 1].max()
    for i, bar in enumerate(bars):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max_value * 0.01,
            f"{int(df_subset.iloc[i, 1])}",
            ha="center",
            va="bottom",
            fontsize=8,
            rotation=90,
        )

    plt.tight_layout()
    plt.savefig(f"report/figures/{filename}", dpi=300, bbox_inches="tight", format="png")
    plt.close()


def main():
    """Main function to create all visualizations"""
    
    # Load the CSV files
    jobs_per_year = load_csv_without_headers("query_results/jobs_per_year.csv", "Year", "Count")
    jobs_per_country = load_csv_without_headers("query_results/jobs_per_country.csv", "Country", "Count")
    jobs_per_website = load_csv_without_headers("query_results/jobs_per_website.csv", "Website", "Count")

    # Create visualizations
    if jobs_per_year is not None:
        create_pie_chart(jobs_per_year, "Jobs Distribution by Year", "jobs_per_year_pie.png")

    if jobs_per_country is not None:
        create_horizontal_bar_plot(jobs_per_country, "Jobs per Country (Top 100)", "jobs_per_country_bar.png", 100)

    if jobs_per_website is not None:
        create_vertical_bar_plot(jobs_per_website, "Jobs per Website (Top 100)", "jobs_per_website_bar.png", 100)


if __name__ == "__main__":
    main()