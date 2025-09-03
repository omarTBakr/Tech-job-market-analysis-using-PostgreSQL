/*
    Data Analysis Overview:

    - Time Range: Specifies the period during which this data was collected.
    - Country Distribution: Lists all countries included in the dataset and the number of jobs per country.
    - Source Websites: Identifies the websites from which the data was gathered and provides the job count per website.
*/



-- Time Range  and jobs per year 

SELECT COUNT(*) AS total_jobs FROM job_postings_fact;

SELECT 
     EXTRACT(
        YEAR
        FROM job_posted_date
    ) AS year ,
    COUNT(*) AS job_count
FROM job_postings_fact
GROUP BY EXTRACT(
        YEAR
        FROM job_posted_date
    );

-- Country Distribution and jobs per country
 
SELECT 
    job_country ,
    COUNT(*) AS job_count
FROM job_postings_fact
GROUP BY job_country
ORDER BY job_count DESC ;


-- Source Websites and jobs per source website

SELECT 
    SPLIT_PART(job_via, ' ', 2) AS source_website,
    COUNT(*) AS job_count
FROM job_postings_fact
GROUP BY SPLIT_PART(job_via, ' ', 2)
HAVING COUNT(*) > 100
ORDER BY job_count DESC;