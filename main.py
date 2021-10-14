from job_scrapper import JobScrapper

jobs = JobScrapper(job_category="backend development", jobs_limit=10)
jobs.search_for_jobs()
jobs.put_in_a_file()

