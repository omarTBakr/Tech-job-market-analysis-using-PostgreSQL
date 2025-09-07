"""
Job Market Analysis Script

This script creates comprehensive visualizations for job market analysis including:
1. Main dashboard with 6 key metrics
2. Detailed salary comparison
3. Job volume analysis  
4. Benefits and requirements analysis
5. Executive summary table

Input: query_results/job_analysis.csv
Output: PNG files in report/figures/ directory
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import sys
from pathlib import Path

# Add parent directory to path and set working directory
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

# Create figures directory if it doesn't exist
os.makedirs("report/figures", exist_ok=True)

# Set high DPI for all figures
plt.rcParams["figure.dpi"] = 600
plt.rcParams["savefig.dpi"] = 600

# Load and preprocess data
df = pd.read_csv("query_results/job_analysis.csv")

# Data preprocessing
df["degree_percentage"] = (df["degree"] / df["total_jobs"]) * 100
df["health_percentage"] = (df["health_insurance"] / df["total_jobs"]) * 100
df["remote_percentage"] = (df["remote"] / df["total_jobs"]) * 100
df["salary_k"] = df["average_salary"] / 1000
df["short_title"] = df["job_title"].str.replace(r"Senior |Machine Learning |Business ", "", regex=True).str[:12]

# Create sorted versions for different metrics
df_by_jobs = df.sort_values("total_jobs", ascending=True)
df_by_salary = df.sort_values("average_salary", ascending=False)
df_by_degree = df.sort_values("degree_percentage", ascending=False)
df_by_remote = df.sort_values("remote_percentage", ascending=False)
df_by_health = df.sort_values("health_percentage", ascending=False)

# Set style for better-looking plots
plt.style.use("seaborn-v0_8")
sns.set_palette("husl")


def create_main_dashboard():
    """Create comprehensive 6-panel dashboard"""
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle("Job Market Analysis Dashboard", fontsize=16, fontweight="bold")

    # 1. Job volume by role
    df_jobs_desc = df.sort_values("total_jobs", ascending=False)
    axes[0, 0].bar(df_jobs_desc["short_title"], df_jobs_desc["total_jobs"], color="skyblue")
    axes[0, 0].set_title("Total Jobs by Role")
    axes[0, 0].set_xlabel("Job Role")
    axes[0, 0].set_ylabel("Number of Jobs")
    axes[0, 0].tick_params(axis="x", rotation=45)

    # 2. Average salary comparison
    axes[0, 1].barh(df_by_salary["short_title"], df_by_salary["salary_k"], color="lightgreen")
    axes[0, 1].set_title("Average Salary by Role")
    axes[0, 1].set_xlabel("Salary ($K)")
    axes[0, 1].set_ylabel("Job Role")

    # 3. Degree requirements
    axes[0, 2].bar(df_by_degree["short_title"], df_by_degree["degree_percentage"], color="orange")
    axes[0, 2].set_title("Degree Requirements (%)")
    axes[0, 2].set_xlabel("Job Role")
    axes[0, 2].set_ylabel("Percentage Requiring Degree")
    axes[0, 2].tick_params(axis="x", rotation=45)

    # 4. Salary vs Job Volume scatter plot
    axes[1, 0].scatter(df["total_jobs"], df["salary_k"], s=100, alpha=0.7, c=range(len(df)), cmap="viridis")
    axes[1, 0].set_title("Salary vs Job Volume")
    axes[1, 0].set_xlabel("Total Jobs")
    axes[1, 0].set_ylabel("Average Salary ($K)")
    for i, txt in enumerate(df["short_title"]):
        axes[1, 0].annotate(
            txt, (df["total_jobs"].iloc[i], df["salary_k"].iloc[i]), 
            xytext=(5, 5), textcoords="offset points", fontsize=8
        )

    # 5. Remote vs Onsite (stacked bar)
    df_remote_sorted = df.sort_values("remote_percentage", ascending=False)
    width = 0.6
    axes[1, 1].bar(df_remote_sorted["short_title"], df_remote_sorted["remote_percentage"], 
                   width, label="Remote", color="dodgerblue")
    axes[1, 1].bar(df_remote_sorted["short_title"], 100 - df_remote_sorted["remote_percentage"], 
                   width, bottom=df_remote_sorted["remote_percentage"], label="Onsite", color="lightsteelblue")
    axes[1, 1].set_title("Work Arrangement")
    axes[1, 1].set_xlabel("Job Role")
    axes[1, 1].set_ylabel("Percentage")
    axes[1, 1].tick_params(axis="x", rotation=45)
    axes[1, 1].legend()

    # 6. Health insurance coverage
    df_health_sorted = df.sort_values("health_percentage", ascending=False)
    axes[1, 2].bar(df_health_sorted["short_title"], df_health_sorted["health_percentage"], 
                   width, label="Health Insurance", color="mediumseagreen")
    axes[1, 2].bar(df_health_sorted["short_title"], 100 - df_health_sorted["health_percentage"], 
                   width, bottom=df_health_sorted["health_percentage"], label="No Health Insurance", color="lightcoral")
    axes[1, 2].set_title("Health Insurance Coverage")
    axes[1, 2].set_xlabel("Job Role")
    axes[1, 2].set_ylabel("Percentage")
    axes[1, 2].tick_params(axis="x", rotation=45)
    axes[1, 2].legend()

    plt.tight_layout()
    plt.savefig("report/figures/job_market_dashboard.png", dpi=300, bbox_inches="tight")
    plt.close()


def create_salary_comparison():
    """Create detailed salary comparison chart"""
    
    plt.figure(figsize=(12, 8))
    df_salary_sorted = df.sort_values("average_salary", ascending=True)
    colors_salary = plt.cm.viridis(np.linspace(0, 1, len(df_salary_sorted)))
    bars = plt.barh(df_salary_sorted["job_title"], df_salary_sorted["salary_k"], color=colors_salary)
    plt.title("Average Salary by Job Role", fontsize=16, fontweight="bold")
    plt.xlabel("Average Salary ($K)")
    plt.ylabel("Job Role")

    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, df_salary_sorted["salary_k"])):
        plt.text(value + 2, bar.get_y() + bar.get_height() / 2, f"${value:.0f}K", 
                va="center", fontweight="bold")

    plt.tight_layout()
    plt.savefig("report/figures/salary_comparison.png", dpi=300, bbox_inches="tight")
    plt.close()


def create_job_volume_chart():
    """Create job volume analysis chart"""
    
    plt.figure(figsize=(14, 8))
    df_volume_sorted = df.sort_values("total_jobs", ascending=False)
    colors_volume = plt.cm.Blues(np.linspace(0.4, 1, len(df_volume_sorted)))
    bars = plt.bar(df_volume_sorted["job_title"], df_volume_sorted["total_jobs"], color=colors_volume)
    plt.title("Job Market Volume by Role", fontsize=16, fontweight="bold")
    plt.xlabel("Job Role")
    plt.ylabel("Number of Available Jobs")
    plt.xticks(rotation=45, ha="right")

    # Add value labels on bars
    for bar, value in zip(bars, df_volume_sorted["total_jobs"]):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3000, 
                f"{value:,}", ha="center", va="bottom", fontweight="bold")

    plt.tight_layout()
    plt.savefig("report/figures/job_volume.png", dpi=300, bbox_inches="tight")
    plt.close()


def create_benefits_requirements_analysis():
    """Create comprehensive benefits and requirements analysis"""
    
    fig, axes = plt.subplots(3, 1, figsize=(14, 14))

    # Health Insurance Coverage
    df_health_sorted = df.sort_values("health_percentage", ascending=False)
    width = 0.6
    axes[0].bar(df_health_sorted["job_title"], df_health_sorted["health_percentage"], 
               width, label="With Health Insurance", color="mediumseagreen")
    axes[0].bar(df_health_sorted["job_title"], 100 - df_health_sorted["health_percentage"], 
               width, bottom=df_health_sorted["health_percentage"], label="No Health Insurance", color="lightcoral")
    axes[0].set_title("Health Insurance Coverage", fontsize=14, fontweight="bold")
    axes[0].set_ylabel("Percentage")
    axes[0].tick_params(axis="x", rotation=45)
    axes[0].legend()

    # Remote work opportunities
    df_remote_sorted = df.sort_values("remote_percentage", ascending=False)
    axes[1].bar(df_remote_sorted["job_title"], df_remote_sorted["remote_percentage"], color="lightblue")
    axes[1].set_title("Remote Work Opportunities", fontsize=14, fontweight="bold")
    axes[1].set_ylabel("Percentage Remote (%)")
    axes[1].tick_params(axis="x", rotation=45)

    # Degree requirements
    df_degree_sorted = df.sort_values("degree_percentage", ascending=False)
    axes[2].bar(df_degree_sorted["job_title"], df_degree_sorted["degree_percentage"], color="orange")
    axes[2].set_title("Degree Requirements", fontsize=14, fontweight="bold")
    axes[2].set_ylabel("Percentage Requiring Degree (%)")
    axes[2].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.savefig("report/figures/benefits_requirements_analysis.png", dpi=300, bbox_inches="tight")
    plt.close()


def create_executive_summary():
    """Create executive summary table visualization"""
    
    fig, ax = plt.subplots(figsize=(14, 10))

    # Create comprehensive overview table
    summary_data = []
    for _, row in df_by_salary.iterrows():
        summary_data.append([
            row["job_title"],
            f"{row['total_jobs']:,}",
            f"${row['average_salary']:,}",
            f"{row['degree_percentage']:.0f}%",
            f"{row['remote_percentage']:.1f}%",
            f"{row['health_percentage']:.1f}%",
        ])

    columns = ["Role", "Jobs Available", "Avg Salary", "Degree Req", "Remote Rate", "Health Coverage"]

    # Create table visualization
    table = ax.table(cellText=summary_data, colLabels=columns, cellLoc="center", 
                    loc="center", colColours=["lightblue"] * 6)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 2)

    # Style the table
    for i in range(len(columns)):
        table[(0, i)].set_facecolor("#4472C4")
        table[(0, i)].set_text_props(weight="bold", color="white")

    # Alternate row colors
    for i in range(1, len(summary_data) + 1):
        for j in range(len(columns)):
            if i % 2 == 0:
                table[(i, j)].set_facecolor("#F2F2F2")
            else:
                table[(i, j)].set_facecolor("white")

    ax.set_title("Job Market Executive Summary\n(Ranked by Average Salary)", 
                fontsize=16, fontweight="bold", pad=20)
    ax.axis("off")

    plt.tight_layout()
    plt.savefig("report/figures/executive_summary.png", dpi=300, bbox_inches="tight")
    plt.close()


# Execute all visualizations
if __name__ == "__main__":
    create_main_dashboard()
    create_salary_comparison()
    create_job_volume_chart()
    create_benefits_requirements_analysis()
    create_executive_summary()