"""
Companies Analysis Script

This script generates visualizations for company hiring data analysis.
It creates three main visualizations:
1. Top 100 companies hiring in machine learning
2. Top 50 companies hiring across all job categories (stacked bar chart)
3. ML jobs distribution analysis (top 20 detailed view + histogram)

Input: query_results/companies.csv
Output: PNG files in report/figures/ directory
"""

import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os


# Add parent directory to path and set working directory
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

# Create figures/ directory if it doesn't exist
os.makedirs("report/figures/", exist_ok=True)

# Set style for better-looking plots
plt.style.use("default")
sns.set_palette("viridis")

# Set high DPI for all figures
plt.rcParams["figure.dpi"] = 600
plt.rcParams["savefig.dpi"] = 600

# Read the companies data
companies_df = pd.read_csv("query_results/companies.csv")


def create_top_ml_companies_plot():
    """Create visualization for top 100 companies hiring in machine learning"""
    
    # Sort companies by machine_learning_jobs and take top 100
    top_ml_companies = companies_df.nlargest(100, "machine_learning_jobs")

    # Create figure with optimal size for 100 companies
    fig, ax = plt.subplots(1, 1, figsize=(16, 24))

    # Create a gradient color map for visual appeal
    colors = plt.cm.plasma(np.linspace(0.2, 0.9, 100))

    # Create horizontal bar plot
    company_names = top_ml_companies["name"].tolist()
    ml_jobs = top_ml_companies["machine_learning_jobs"].tolist()

    bars = ax.barh(range(len(company_names)), ml_jobs, color=colors)

    # Customize the plot
    ax.set_yticks(range(len(company_names)))
    ax.set_yticklabels(company_names, fontsize=8)
    ax.set_xlabel("Machine Learning Jobs Count", fontsize=14, fontweight="bold")
    ax.set_title("Top 100 Companies Hiring in Machine Learning", fontsize=18, fontweight="bold", pad=20)

    # Add value labels on bars
    max_jobs = max(ml_jobs)
    for i, (bar, count) in enumerate(zip(bars, ml_jobs)):
        ax.text(
            bar.get_width() + max_jobs * 0.005,
            bar.get_y() + bar.get_height() / 2,
            f"{count:,}",
            va="center",
            fontsize=7,
            fontweight="bold",
        )

    # Invert y-axis so #1 company is on top
    ax.invert_yaxis()

    # Add grid for better readability
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)

    # Set x-axis limits to accommodate labels
    ax.set_xlim(0, max_jobs * 1.15)

    # Adjust layout to prevent label cutoff
    plt.subplots_adjust(left=0.25, right=0.95, top=0.95, bottom=0.05)

    # Save with high DPI
    plt.savefig("report/figures/top_100_ml_companies.png", dpi=600, bbox_inches="tight", facecolor="white", edgecolor="none")
    plt.close()


def create_top_50_all_jobs_plot():
    """Create visualization for top 50 companies hiring across all job types"""
    
    # Sort companies by total_jobs and take top 50
    top_50_companies = companies_df.nlargest(50, "total_jobs")

    # Define job categories and their colors
    job_categories = [
        ("analyst_jobs", "Data Analyst"),
        ("scientist_jobs", "Data Scientist"),
        ("machine_learning_jobs", "Machine Learning"),
        ("cloud_jobs", "Cloud"),
        ("software_jobs", "Software"),
        ("other_engineer_jobs", "Other Engineering"),
    ]

    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD"]

    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(16, 20))

    # Prepare data for stacked horizontal bar chart
    company_names = top_50_companies["name"].tolist()

    # Create arrays for each job type
    job_data = {}
    for col, label in job_categories:
        job_data[label] = top_50_companies[col].tolist()

    # Create stacked horizontal bar chart
    left = np.zeros(len(company_names))
    bars = []

    for i, (label, color) in enumerate(zip(job_data.keys(), colors)):
        bars.append(ax.barh(range(len(company_names)), job_data[label], left=left, color=color, label=label, alpha=0.8))
        left += job_data[label]

    # Customize the plot
    ax.set_yticks(range(len(company_names)))
    ax.set_yticklabels(company_names, fontsize=10)
    ax.set_xlabel("Total Jobs Count", fontsize=14, fontweight="bold")
    ax.set_title("Top 50 Companies - Hiring Across All Job Categories", fontsize=18, fontweight="bold", pad=20)

    # Add total value labels on bars
    total_jobs = top_50_companies["total_jobs"].tolist()
    max_total = max(total_jobs)

    for i, total in enumerate(total_jobs):
        ax.text(total + max_total * 0.01, i, f"{total:,}", va="center", fontsize=9, fontweight="bold")

    # Invert y-axis so top company is on top
    ax.invert_yaxis()

    # Add legend
    ax.legend(loc="lower right", fontsize=10, framealpha=0.9)

    # Add grid for better readability
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)

    # Set x-axis limits to accommodate labels
    ax.set_xlim(0, max_total * 1.12)

    # Adjust layout
    plt.subplots_adjust(left=0.25, right=0.95, top=0.95, bottom=0.05)

    # Save with high DPI
    plt.savefig("report/figures/top_50_all_jobs_companies.png", dpi=600, bbox_inches="tight", facecolor="white", edgecolor="none")
    plt.close()


def create_ml_jobs_distribution_plot():
    """Create ML jobs distribution analysis with top 20 detailed view and histogram"""
    
    # Sort companies by machine_learning_jobs and take top 100
    top_ml_companies = companies_df.nlargest(100, "machine_learning_jobs")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Plot 1: Top 20 companies (detailed view)
    top_20 = top_ml_companies.head(20)
    colors_20 = plt.cm.Set1(np.linspace(0, 1, 20))

    bars1 = ax1.barh(range(len(top_20)), top_20["machine_learning_jobs"], color=colors_20)
    ax1.set_yticks(range(len(top_20)))
    ax1.set_yticklabels(top_20["name"], fontsize=10)
    ax1.set_xlabel("ML Jobs Count", fontsize=12, fontweight="bold")
    ax1.set_title("Top 20 ML Hiring Companies\n(Detailed View)", fontsize=14, fontweight="bold")
    ax1.invert_yaxis()
    ax1.grid(axis="x", alpha=0.3, linestyle="--")

    # Add value labels for top 20
    for bar, count in zip(bars1, top_20["machine_learning_jobs"]):
        ax1.text(
            bar.get_width() + max(top_20["machine_learning_jobs"]) * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{count:,}",
            va="center",
            fontsize=9,
            fontweight="bold",
        )

    # Plot 2: Distribution histogram
    ax2.hist(top_ml_companies["machine_learning_jobs"], bins=20, color="skyblue", alpha=0.7, edgecolor="black")
    ax2.set_xlabel("ML Jobs Count", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Number of Companies", fontsize=12, fontweight="bold")
    ax2.set_title("Distribution of ML Jobs\n(Top 100 Companies)", fontsize=14, fontweight="bold")
    ax2.grid(axis="y", alpha=0.3, linestyle="--")

    plt.tight_layout()
    plt.savefig("report/figures/ml_companies_analysis.png", dpi=600, bbox_inches="tight", facecolor="white", edgecolor="none")
    plt.close()


# Execute all visualizations
if __name__ == "__main__":
    create_top_ml_companies_plot()
    create_top_50_all_jobs_plot()
    create_ml_jobs_distribution_plot()