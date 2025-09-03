import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import sys
from pathlib import Path
def main():
    # Add parent directory to path and set working directory
    PROJECT_ROOT = Path(__file__).parent.parent
    sys.path.insert(0, str(PROJECT_ROOT))
    os.chdir(PROJECT_ROOT)

    # Create report/figures/ directory if it doesn't exist
    os.makedirs("report/figures/", exist_ok=True)

    # Set style for better-looking plots
    plt.style.use("default")
    sns.set_palette("husl")

    # Read the data
    skills_df = pd.read_csv("query_results/skill.csv")
    skill_types_df = pd.read_csv("query_results/skill_type.csv")

    def create_individual_skills_plot():
        """Create visualization for top 10 individual skills per job title"""

        job_titles = skills_df["job_title"].tolist()
        n_jobs = len(job_titles)

        # Calculate figure size based on number of job titles
        fig_height = max(6, n_jobs * 4)
        fig, axes = plt.subplots(n_jobs, 1, figsize=(14, fig_height))

        # Handle single job title case
        if n_jobs == 1:
            axes = [axes]

        colors = plt.cm.Set3(np.linspace(0, 1, 10))  # Colors for top 10 skills

        for idx, job_title in enumerate(job_titles):
            job_row = skills_df[skills_df["job_title"] == job_title].iloc[0]
            skill_columns = [col for col in skills_df.columns if col != "job_title"]
            skill_values = [
                (col.replace("_count", "").replace("_", " ").title(), job_row[col])
                for col in skill_columns
            ]
            skill_values.sort(key=lambda x: x[1], reverse=True)
            top_10 = skill_values[:10]
            skill_names = [item[0] for item in top_10]
            skill_counts = [item[1] for item in top_10]

            bars = axes[idx].barh(range(len(skill_names)), skill_counts, color=colors)
            axes[idx].set_yticks(range(len(skill_names)))
            axes[idx].set_yticklabels(skill_names, fontsize=10)
            axes[idx].set_xlabel("Count", fontsize=11, fontweight="bold")
            axes[idx].set_title(f"Top 10 Skills for {job_title}", fontsize=12, fontweight="bold", pad=15)

            for i, (bar, count) in enumerate(zip(bars, skill_counts)):
                axes[idx].text(
                    bar.get_width() + max(skill_counts) * 0.01,
                    bar.get_y() + bar.get_height() / 2,
                    f"{count:,}",
                    va="center",
                    fontsize=9,
                    fontweight="bold",
                )

            axes[idx].invert_yaxis()
            axes[idx].grid(axis="x", alpha=0.3, linestyle="--")
            axes[idx].set_axisbelow(True)
            axes[idx].set_xlim(0, max(skill_counts) * 1.15)

        plt.tight_layout()
        plt.savefig("report/figures/top_10_individual_skills.png", dpi=600, bbox_inches="tight", facecolor="white", edgecolor="none")
        plt.show()

    def create_skill_types_plot():
        """Create visualization for all skill types per job title"""

        job_titles = skill_types_df["job_title"].tolist()
        n_jobs = len(job_titles)

        fig_height = max(6, n_jobs * 3.5)
        fig, axes = plt.subplots(n_jobs, 1, figsize=(12, fig_height))

        if n_jobs == 1:
            axes = [axes]

        skill_type_colors = plt.cm.Set2(np.linspace(0, 1, 10))

        for idx, job_title in enumerate(job_titles):
            job_row = skill_types_df[skill_types_df["job_title"] == job_title].iloc[0]
            type_columns = [col for col in skill_types_df.columns if col != "job_title"]
            type_values = [
                (col.replace("_count", "").replace("_", " ").title(), job_row[col])
                for col in type_columns
            ]
            type_values.sort(key=lambda x: x[1], reverse=True)
            type_names = [item[0] for item in type_values]
            type_counts = [item[1] for item in type_values]

            bars = axes[idx].barh(range(len(type_names)), type_counts, color=skill_type_colors[: len(type_names)])
            axes[idx].set_yticks(range(len(type_names)))
            axes[idx].set_yticklabels(type_names, fontsize=11)
            axes[idx].set_xlabel("Count", fontsize=12, fontweight="bold")
            axes[idx].set_title(f"Skill Categories Distribution for {job_title}", fontsize=13, fontweight="bold", pad=15)

            for i, (bar, count) in enumerate(zip(bars, type_counts)):
                axes[idx].text(
                    bar.get_width() + max(type_counts) * 0.01,
                    bar.get_y() + bar.get_height() / 2,
                    f"{count:,}",
                    va="center",
                    fontsize=10,
                    fontweight="bold",
                )

            axes[idx].invert_yaxis()
            axes[idx].grid(axis="x", alpha=0.3, linestyle="--")
            axes[idx].set_axisbelow(True)
            axes[idx].set_xlim(0, max(type_counts) * 1.12)

        plt.tight_layout()
        plt.savefig("report/figures/skill_types_distribution.png", dpi=600, bbox_inches="tight", facecolor="white", edgecolor="none")
        plt.show()

    # Create both visualizations
    create_individual_skills_plot()
    create_skill_types_plot()

if __name__ == "__main__":
    main()
