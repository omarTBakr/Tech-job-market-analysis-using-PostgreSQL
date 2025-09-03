/*
    in this query we will 
    1. get the top 50 companies per specialization 
    2. get the number of jobs specaialization per company 
*/

-- huge number of companies
SELECT DISTINCT name FROM company_dim;

SELECT DISTINCT job_title_short FROM job_postings_fact;
-- ONLY 729 NOW 
SELECT 
    comp.name,
    COUNT(job.job_id) AS job_count
FROM job_postings_fact AS job
INNER JOIN company_dim AS comp ON job.company_id = comp.company_id
GROUP BY comp.name
HAVING COUNT(job.job_id) >=100
ORDER BY job_count DESC;

-- now we need to get the number of jobs specialization per company


SELECT 
    comp.name,
    COUNT(job.job_id) AS total_jobs,
    SUM(CASE WHEN job.job_title_short ILIKE '%analyst%' THEN 1 ELSE 0 END) AS analyst_jobs,
    SUM(CASE WHEN job.job_title_short ILIKE '%scientist%' THEN 1 ELSE 0 END) AS scientist_jobs,
    SUM(CASE WHEN job.job_title_short ILIKE '%machine%' THEN 1 ELSE 0 END) AS machine_learning_jobs,
    SUM(CASE WHEN job.job_title_short ILIKE '%cloud%' THEN 1 ELSE 0 END) AS cloud_jobs,
    SUM(CASE WHEN job.job_title_short ILIKE '%software%' THEN 1 ELSE 0 END) AS software_jobs,
    SUM(CASE WHEN job.job_title_short ILIKE '%engineer%' AND 
             job.job_title_short NOT ILIKE '%machine%' AND 
             job.job_title_short NOT ILIKE '%software%' AND 
             job.job_title_short NOT ILIKE '%cloud%' THEN 1 ELSE 0 END) AS other_engineer_jobs

FROM job_postings_fact AS job
INNER JOIN company_dim AS comp ON job.company_id = comp.company_id
GROUP BY comp.name
HAVING COUNT(job.job_id) >= 100
ORDER BY total_jobs DESC;
