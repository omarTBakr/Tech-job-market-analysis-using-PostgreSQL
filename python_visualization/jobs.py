import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os
import sys
from pathlib import Path
import os

# Add parent directory to path and set working directory
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

# Create figures directory if it doesn't exist
os.makedirs("report/figures", exist_ok=True)

# Load the data from correct path
df = pd.read_csv("query_results/job_analysis.csv")

# Data preprocessing
df["degree_percentage"] = (df["degree"] / df["total_jobs"]) * 100
df["health_percentage"] = (df["health_insurance"] / df["total_jobs"]) * 100
df["remote_percentage"] = (df["remote"] / df["total_jobs"]) * 100
df["salary_k"] = df["average_salary"] / 1000
df["short_title"] = df["job_title"].str.replace(r"Senior |Machine Learning |Business ", "", regex=True).str[:12]

# Create sorted versions for different metrics
df_by_jobs = df.sort_values("total_jobs", ascending=True)  # Horizontal bars work better with ascending
df_by_salary = df.sort_values("average_salary", ascending=False)
df_by_degree = df.sort_values("degree_percentage", ascending=False)
df_by_remote = df.sort_values("remote_percentage", ascending=False)
df_by_health = df.sort_values("health_percentage", ascending=False)

# Dataset loaded successfully

# =============================================================================
# MAIN DASHBOARD - MATPLOTLIB + SEABORN
# =============================================================================

# Set style for better-looking plots
plt.style.use("seaborn-v0_8")
sns.set_palette("husl")

# Create a comprehensive figure with subplots
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
        txt, (df["total_jobs"].iloc[i], df["salary_k"].iloc[i]), xytext=(5, 5), textcoords="offset points", fontsize=8
    )

# 5. Remote vs Onsite (stacked bar)
df_remote_sorted = df.sort_values("remote_percentage", ascending=False)
width = 0.6
axes[1, 1].bar(df_remote_sorted["short_title"], df_remote_sorted["remote_percentage"], width, label="Remote", color="dodgerblue")
axes[1, 1].bar(
    df_remote_sorted["short_title"],
    100 - df_remote_sorted["remote_percentage"],
    width,
    bottom=df_remote_sorted["remote_percentage"],
    label="Onsite",
    color="lightsteelblue",
)
axes[1, 1].set_title("Work Arrangement")
axes[1, 1].set_xlabel("Job Role")
axes[1, 1].set_ylabel("Percentage")
axes[1, 1].tick_params(axis="x", rotation=45)
axes[1, 1].legend()

# 6. Degree vs No Degree (stacked bar)
df_degree_sorted = df.sort_values("degree_percentage", ascending=False)
width = 0.6
axes[1, 2].bar(
    df_degree_sorted["short_title"], df_degree_sorted["degree_percentage"], width, label="Degree Required", color="gold"
)
axes[1, 2].bar(
    df_degree_sorted["short_title"],
    100 - df_degree_sorted["degree_percentage"],
    width,
    bottom=df_degree_sorted["degree_percentage"],
    label="No Degree Required",
    color="wheat",
)
axes[1, 2].set_title("Education Requirements")
axes[1, 2].set_xlabel("Job Role")
axes[1, 2].set_ylabel("Percentage")
axes[1, 2].tick_params(axis="x", rotation=45)
axes[1, 2].legend()

plt.tight_layout()
plt.savefig("report/figures/job_market_dashboard.png", dpi=300, bbox_inches="tight")
plt.show()

# =============================================================================
# INDIVIDUAL FOCUSED CHARTS
# =============================================================================

# 1. Salary comparison chart
plt.figure(figsize=(12, 8))
df_salary_sorted = df.sort_values("average_salary", ascending=True)  # Ascending for horizontal bars
colors_salary = plt.cm.viridis(np.linspace(0, 1, len(df_salary_sorted)))
bars = plt.barh(df_salary_sorted["job_title"], df_salary_sorted["salary_k"], color=colors_salary)
plt.title("Average Salary by Job Role", fontsize=16, fontweight="bold")
plt.xlabel("Average Salary ($K)")
plt.ylabel("Job Role")

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars, df_salary_sorted["salary_k"])):
    plt.text(value + 2, bar.get_y() + bar.get_height() / 2, f"${value:.0f}K", va="center", fontweight="bold")

plt.tight_layout()
plt.savefig("report/figures/salary_comparison.png", dpi=300, bbox_inches="tight")
plt.show()

# 2. Job volume chart
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
    plt.text(
        bar.get_x() + bar.get_width() / 2, bar.get_height() + 3000, f"{value:,}", ha="center", va="bottom", fontweight="bold"
    )

plt.tight_layout()
plt.savefig("report/figures/job_volume.png", dpi=300, bbox_inches="tight")
plt.show()

# 3. Comprehensive comparison chart - now includes health insurance
fig, axes = plt.subplots(4, 1, figsize=(14, 16))

# Health Insurance Coverage (moved here)
df_health_sorted = df.sort_values("health_percentage", ascending=False)
width = 0.6
axes[0].bar(
    df_health_sorted["job_title"],
    df_health_sorted["health_percentage"],
    width,
    label="With Health Insurance",
    color="mediumseagreen",
)
axes[0].bar(
    df_health_sorted["job_title"],
    100 - df_health_sorted["health_percentage"],
    width,
    bottom=df_health_sorted["health_percentage"],
    label="No Health Insurance",
    color="lightcoral",
)
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

# Salary vs Job Volume Scatter Plot (restored)
axes[3].scatter(df["total_jobs"], df["salary_k"], s=100, alpha=0.7, c=range(len(df)), cmap="viridis")
axes[3].set_title("Salary vs Job Market Volume", fontsize=14, fontweight="bold")
axes[3].set_xlabel("Total Jobs Available")
axes[3].set_ylabel("Average Salary ($K)")
for i, txt in enumerate(df["short_title"]):
    axes[3].annotate(
        txt, (df["total_jobs"].iloc[i], df["salary_k"].iloc[i]), xytext=(5, 5), textcoords="offset points", fontsize=9
    )

plt.tight_layout()
plt.savefig("report/figures/comprehensive_comparison.png", dpi=300, bbox_inches="tight")
plt.show()

# =============================================================================
# PLOTLY INTERACTIVE DASHBOARD
# =============================================================================

# Interactive dashboard with subplots
fig = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=("Job Volume by Role", "Salary Distribution", "Work Benefits Overview", "Role Requirements"),
    specs=[[{"secondary_y": False}, {"secondary_y": False}], [{"secondary_y": False}, {"secondary_y": False}]],
)

# 1. Job volume bar chart
df_jobs_sorted = df.sort_values("total_jobs", ascending=False)
fig.add_trace(
    go.Bar(
        x=df_jobs_sorted["job_title"],
        y=df_jobs_sorted["total_jobs"],
        name="Total Jobs",
        marker_color="lightblue",
        showlegend=False,
    ),
    row=1,
    col=1,
)

# 2. Salary bar chart
df_salary_sorted = df.sort_values("average_salary", ascending=False)
fig.add_trace(
    go.Bar(
        x=df_salary_sorted["job_title"],
        y=df_salary_sorted["salary_k"],
        name="Salary ($K)",
        marker_color="lightgreen",
        showlegend=False,
    ),
    row=1,
    col=2,
)

# 3. Benefits stacked bar (Health Insurance)
fig.add_trace(
    go.Bar(x=df["job_title"], y=df["health_percentage"], name="With Health Insurance", marker_color="mediumseagreen"),
    row=2,
    col=1,
)
fig.add_trace(
    go.Bar(x=df["job_title"], y=100 - df["health_percentage"], name="No Health Insurance", marker_color="lightcoral"),
    row=2,
    col=1,
)

# 4. Education requirements
fig.add_trace(
    go.Bar(x=df["job_title"], y=df["degree_percentage"], name="Degree Required", marker_color="orange", showlegend=False),
    row=2,
    col=2,
)

# Update layout
fig.update_layout(height=800, title_text="Interactive Job Market Dashboard", barmode="stack")
fig.update_xaxes(tickangle=45)
fig.show()

# Save as HTML
fig.write_html("report/figures/interactive_dashboard.html")

# =============================================================================
# PLOTLY EXPRESS CHARTS
# =============================================================================

# 1. Interactive salary chart
fig1 = px.bar(
    df_salary_sorted,
    x="job_title",
    y="salary_k",
    title="Average Salary by Role",
    labels={"salary_k": "Average Salary ($K)", "job_title": "Job Role"},
    color="salary_k",
    color_continuous_scale="viridis",
)
fig1.update_layout(xaxis_tickangle=-45)
fig1.write_html("report/figures/interactive_salary.html")
fig1.show()

# 2. Multi-dimensional bubble chart
fig2 = px.scatter(
    df,
    x="total_jobs",
    y="average_salary",
    size="degree_percentage",
    color="remote_percentage",
    hover_name="job_title",
    title="Job Market Overview (Size = Degree %, Color = Remote %)",
    labels={
        "total_jobs": "Total Jobs",
        "average_salary": "Average Salary ($)",
        "remote_percentage": "Remote %",
        "degree_percentage": "Degree %",
    },
)
fig2.write_html("report/figures/bubble_chart.html")
fig2.show()

# =============================================================================
# KEY INSIGHTS VISUALIZATION
# =============================================================================

# Create key insights summary chart
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle("Job Market Key Insights", fontsize=18, fontweight="bold", y=0.98)

# 1. Market Size Overview (Top 5 roles by volume)
top_5_volume = df.nlargest(5, "total_jobs")
ax1.pie(
    top_5_volume["total_jobs"], labels=top_5_volume["job_title"], autopct="%1.1f%%", colors=plt.cm.Blues(np.linspace(0.4, 1, 5))
)
ax1.set_title("Market Share by Job Volume\n(Top 5 Roles)", fontweight="bold")

# 2. Salary Tiers
salary_ranges = ["<$100K", "$100-120K", "$120-140K", "$140K+"]
salary_counts = [
    len(df[df["average_salary"] < 100000]),
    len(df[(df["average_salary"] >= 100000) & (df["average_salary"] < 120000)]),
    len(df[(df["average_salary"] >= 120000) & (df["average_salary"] < 140000)]),
    len(df[df["average_salary"] >= 140000]),
]
ax2.bar(salary_ranges, salary_counts, color=plt.cm.Greens(np.linspace(0.4, 1, 4)))
ax2.set_title("Salary Distribution Across Roles", fontweight="bold")
ax2.set_ylabel("Number of Roles")

# 3. Critical Stats Summary
categories = ["Total Jobs\n(All Roles)", "Avg Remote\nRate (%)", "Avg Degree\nReq (%)", "Avg Health\nCoverage (%)"]
values = [
    df["total_jobs"].sum() / 1000,  # in thousands
    (df["remote"].sum() / df["total_jobs"].sum()) * 100,
    (df["degree"].sum() / df["total_jobs"].sum()) * 100,
    (df["health_insurance"].sum() / df["total_jobs"].sum()) * 100,
]
colors_stats = ["skyblue", "lightcoral", "gold", "lightgreen"]
bars = ax3.bar(categories, values, color=colors_stats)
ax3.set_title("Market Overview Statistics", fontweight="bold")
ax3.set_ylabel("Value")

# Add value labels on bars
for bar, value, category in zip(bars, values, categories):
    if "Total Jobs" in category:
        label = f"{value:.0f}K"
    else:
        label = f"{value:.1f}%"
    ax3.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + max(values) * 0.02,
        label,
        ha="center",
        va="bottom",
        fontweight="bold",
    )

# 4. High-Value vs High-Volume Comparison
top_salary_roles = df.nlargest(5, "average_salary")
ax4.scatter(top_salary_roles["total_jobs"], top_salary_roles["average_salary"], s=200, c="red", alpha=0.7, label="High Salary")
for i, row in top_salary_roles.iterrows():
    ax4.annotate(
        row["short_title"], (row["total_jobs"], row["average_salary"]), xytext=(5, 5), textcoords="offset points", fontsize=9
    )

top_volume_roles = df.nlargest(5, "total_jobs")
ax4.scatter(top_volume_roles["total_jobs"], top_volume_roles["average_salary"], s=200, c="blue", alpha=0.7, label="High Volume")
ax4.set_xlabel("Total Jobs Available")
ax4.set_ylabel("Average Salary ($)")
ax4.set_title("High-Salary vs High-Volume Roles", fontweight="bold")
ax4.legend()

plt.tight_layout()
plt.savefig("report/figures/key_insights.png", dpi=300, bbox_inches="tight")
plt.show()

# =============================================================================
# EXECUTIVE SUMMARY CHART
# =============================================================================

# Single comprehensive executive summary
fig, ax = plt.subplots(figsize=(14, 10))

# Create a comprehensive overview table as a visualization
summary_data = []
for _, row in df_by_salary.iterrows():
    summary_data.append(
        [
            row["job_title"],
            f"{row['total_jobs']:,}",
            f"${row['average_salary']:,}",
            f"{row['degree_percentage']:.0f}%",
            f"{row['remote_percentage']:.1f}%",
            f"{row['health_percentage']:.1f}%",
        ]
    )

columns = ["Role", "Jobs Available", "Avg Salary", "Degree Req", "Remote Rate", "Health Coverage"]

# Create table visualization
table = ax.table(cellText=summary_data, colLabels=columns, cellLoc="center", loc="center", colColours=["lightblue"] * 6)
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

ax.set_title("Job Market Executive Summary\n(Ranked by Average Salary)", fontsize=16, fontweight="bold", pad=20)
ax.axis("off")

plt.tight_layout()
plt.savefig("report/figures/executive_summary.png", dpi=300, bbox_inches="tight")
plt.show()

# =============================================================================
# REMOVE ANALYSIS FUNCTIONS (REPLACE WITH VISUALIZATIONS)
# =============================================================================

print("\n=== VISUALIZATION COMPLETE ===")
print("Generated visualizations for final report:")
print("- job_market_dashboard.png (Main 6-panel overview)")
print("- salary_comparison.png (Detailed salary analysis)")
print("- job_volume.png (Market volume analysis)")
print("- comprehensive_comparison.png (Benefits & requirements)")
print("- key_insights.png (Executive summary with critical data)")
print("- executive_summary.png (Complete data table)")
print("- Interactive HTML dashboards for presentations")
