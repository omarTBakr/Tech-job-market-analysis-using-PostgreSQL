/*
    High-Level Summary:
    This script analyzes job postings data to provide insights on various job titles, focusing on key metrics such as:
    - Total number of job offerings per job title
    - Average annual salary per job title
    - Number of jobs mentioning degree requirements (with/without degree)
    - Number of jobs offering health insurance (with/without)
    - Distribution of remote vs onsite jobs per job title

    The results are grouped by job title and sorted by the total number of job offerings in descending order.
*/

WITH JobData AS (
    SELECT
        job_title_short AS job_title,
        COUNT(*) AS job_count,
        ROUND(AVG(salary_year_avg), 0) AS average_salary,
        SUM(CASE WHEN job_no_degree_mention IS TRUE THEN 1 ELSE 0 END) AS no_degree,
        SUM(CASE WHEN job_no_degree_mention IS FALSE THEN 1 ELSE 0 END) AS degree,
        SUM(CASE WHEN job_health_insurance IS TRUE THEN 1 ELSE 0 END) AS health_insurance,
        SUM(CASE WHEN job_health_insurance IS FALSE THEN 1 ELSE 0 END) AS no_health_insurance

    FROM 
        job_postings_fact
    -- WHERE 
    --     job_title LIKE '%data%' 
    --     OR job_title LIKE '%machine learning%' 
    --     OR job_title LIKE '%artificial intelligence%' 
    --     OR job_title LIKE '%computer vision%'
    GROUP BY job_title_short
), 
Remote AS (
    SELECT
        job_title_short AS job_title,
        SUM(CASE WHEN job_work_from_home IS TRUE THEN 1 ELSE 0 END) AS remote_jobs,
        SUM(CASE WHEN job_work_from_home IS FALSE THEN 1 ELSE 0 END) AS non_remote_jobs
    FROM 
        job_postings_fact
    GROUP BY 
        job_title_short 
)
SELECT 
    JobData.job_title AS job_title,
    JobData.job_count AS total_jobs,
    JobData.no_degree AS no_degree,
    JobData.degree AS degree,
    JobData.health_insurance AS health_insurance,
    JobData.no_health_insurance AS no_health_insurance,
    JobData.average_salary AS average_salary,
    Remote.remote_jobs AS remote,
    Remote.non_remote_jobs AS onsite 
FROM 
    JobData 
    INNER JOIN Remote ON JobData.job_title = Remote.job_title 
ORDER BY 
    JobData.job_count DESC;
