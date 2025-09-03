# Job Market Analysis Project

A comprehensive data analysis project examining job market trends, company hiring patterns, and skill demands in the tech industry using SQL for data extraction and Python for visualization.

## Project Overview

This project analyzes a comprehensive job postings dataset to provide insights into:
- Job market volume and trends across different roles
- Salary distributions and compensation analysis  
- Company hiring patterns and specializations
- Skill demand analysis across job categories
- Remote work opportunities and benefits analysis
- Educational requirements across different positions

## Project Structure

```
job-market-analysis/
.
├── data
│   ├── csv_files
│   │   .csv # for populating the data base 
│   └── sql_load  
│       ├── 1_create_database.sql
│       ├── 2_create_tables.sql
│       └── 3_modify_tables.sql
├── python_visualization
│   ├── companies.py
│   ├── exploration.py
│   ├── jobs.py
│   └── skills.py
├── query_results
│    .csv ...
├── README.md
├── report
│   ├── figures
│   │    ...
│   ├── latex_template.tex
│   └── report.pdf
└── sql_queries
    ├── companies.sql
    ├── exploration.sql
    ├── jobs.sql
    ├── project.session.sql
    └── skills.sql


        
```

## Technologies Used

### Data Analysis
- **SQL**: PostgreSQL for complex data queries and aggregations
- **Python**: Data processing and analysis
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations

### Visualization
- **Matplotlib**: Static visualizations and publication-quality plots
- **Seaborn**: Statistical data visualization
- **Plotly**: Interactive dashboards and charts

## Dataset Information

The dataset contains job postings data with the following key metrics:
- **Time Range**: Multi-year job posting data
- **Geographic Coverage**: Multiple countries with focus on major markets
- **Data Sources**: Aggregated from major job posting websites
- **Job Categories**: Tech roles including data science, engineering, analysis, and cloud computing

### Key Tables
- [`company_dim.csv`](data/csv_files/company_dim.csv): Company information and details  
- [`job_postings_fact.csv`](data/csv_files/job_postings_fact.csv): Main job postings data
- [`skills_dim.csv`](data/csv_files/skills_dim.csv): Skills and competency data
- [`skills_job_dim.csv`](data/csv_files/skills_job_dim.csv): Job-skill relationship mapping

## Setup Instructions

### Prerequisites
```bash
pip install pandas matplotlib seaborn plotly numpy pathlib
```

### Database Setup
1. Set up PostgreSQL database
2. Run the setup scripts in order:
   ```sql
   -- Execute in sequence:
   psql -f data/sql_load/1_create_database.sql
   psql -f data/sql_load/2_create_tables.sql  
   psql -f data/sql_load/3_modify_tables.sql
   ```
3. Load the CSV data into the created tables

### Running the Analysis
Execute the SQL queries in logical order:
```sql
-- 1. Dataset exploration
psql -f sql_queries/exploration.sql

-- 2. Job market analysis  
psql -f sql_queries/jobs.sql

-- 3. Skills demand analysis
psql -f sql_queries/skills.sql

-- 4. Company patterns analysis
psql -f sql_queries/companies.sql
```

### Generating Visualizations
```bash
# Generate job market visualizations
python visualization_scripts/jobs.py

# Generate company analysis charts
python visualization_scripts/companies.py
```

## Analysis Results

### 1. Dataset Exploration

![Jobs Per Country](figures/jobs_per_country_bar.png)

Geographic distribution analysis shows market coverage across different regions.

![Jobs Per Year](figures/jobs_per_year_pie.png)

Temporal analysis reveals hiring trends over the dataset timeframe.

![Jobs Per Website Source](figures/jobs_per_website_bar.png)

Data source analysis ensures comprehensive coverage from major job platforms.

**Key SQL**: [`exploration.sql`](sql_queries/exploration.sql)

### 2. Job Market Analysis

![Job Market Dashboard](figures/job_market_dashboard.png)

Comprehensive overview of job market dynamics across different tech roles.

![Salary Comparison](figures/salary_comparison.png)

Detailed salary analysis revealing compensation tiers across job categories.

![Job Volume Analysis](figures/job_volume.png)

Market volume analysis showing job availability by role.

![Comprehensive Comparison](figures/comprehensive_comparison.png)

Benefits and requirements analysis including remote work, health insurance, and education requirements.

**Key SQL**: [`jobs.sql`](sql_queries/jobs.sql)

### 3. Skills Demand Analysis

![Top Individual Skills](figures/top_10_individual_skills.png)

Analysis of the most in-demand individual technical skills across all job categories.

![Skill Types Distribution](figures/skill_types_distribution.png)

Breakdown of skill categories showing demand for programming languages, databases, cloud platforms, and other technical competencies.

**Key SQL**: [`skills.sql`](sql_queries/skills.sql)

### 4. Company Hiring Patterns

![Top ML Companies](figures/top_100_ml_companies.png)

Top 100 companies leading machine learning hiring initiatives.

![Company Hiring Analysis](figures/ml_companies_analysis.png)

Deep dive analysis of machine learning hiring patterns and distribution.

![Top Companies Overall](figures/top_50_all_jobs_companies.png)

Overall hiring volume leaders across all job categories and specializations.

**Key SQL**: [`companies.sql`](sql_queries/companies.sql)

## Executive Summary

![Key Insights](figures/key_insights.png)

![Executive Summary](figures/executive_summary.png)

## Interactive Dashboards

- [Interactive Dashboard](figures/interactive_dashboard.html): Multi-panel overview with interactive filtering
- [Interactive Salary Analysis](figures/interactive_salary.html): Detailed compensation exploration  
- [Bubble Chart Analysis](figures/bubble_chart.html): Multi-dimensional market analysis

## Key Findings

1. **Market Volume**: Significant variation in job availability across roles, with traditional software and data roles leading
2. **Compensation Tiers**: Clear salary stratification with machine learning and senior roles commanding premiums
3. **Skills Demand**: Strong demand for cloud technologies, programming languages, and data analysis tools
4. **Company Patterns**: Tech giants dominate specialized hiring while smaller companies focus on general roles
5. **Benefits Trends**: Remote work opportunities and health coverage vary significantly by role and company size

## Business Applications

This analysis provides valuable insights for:
- **Job Seekers**: Understanding market demand, salary expectations, and skill requirements
- **Employers**: Benchmarking compensation, identifying talent pools, and skill gap analysis  
- **Recruiters**: Market intelligence and candidate sourcing strategies
- **Career Counselors**: Data-driven career guidance and planning

## Technical Implementation

### SQL Query Design
- Efficient use of JOINs and aggregations
- Strategic use of CTEs for complex analysis  
- Comprehensive CASE statements for categorical analysis

### Visualization Approach
- Multi-panel dashboards for comprehensive overviews
- Interactive elements for detailed exploration
- Consistent styling and professional presentation
- Both static publication-quality and interactive formats

## Future Enhancements

- Time series forecasting for trend prediction
- Geographic salary variation deep dive
- Industry-specific specialization analysis
- Real-time data pipeline integration
- Predictive modeling for salary and demand forecasting

---

 