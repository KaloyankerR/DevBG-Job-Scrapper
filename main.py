from job_scrapper import JobScrapper

print('''
What job are you looking for:

1) Backend Development
2) Frontend Development
3) Fullstack Development
4) Infrastructure
5) Quality Assurance
6) PM/BA and more
7) Mobile development
8) Data Science
9) ERP/CRM Development
10) UI/UX, arts 
 
''')

job_category = int(input("Enter the number: "))
jobs_limit = int(input("Enter how many jobs do you want to scrap: "))

jobs = JobScrapper(job_category=job_category, jobs_limit=jobs_limit)
jobs.search_for_jobs()
jobs.write_in_file()

