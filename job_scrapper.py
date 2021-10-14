import csv
import requests
from bs4 import BeautifulSoup


class JobScrapper:
    devbg_url = "https://dev.bg/company/"
    job_categories = ["backend development", "frontend development",
                      "fullstack development", "infrastructure",
                      "quality assurance", "pm/ba and more",
                      "mobile development", "data science", "erp/crm development",
                      "ui/ux, arts"]

    def __init__(self, job_category: str, jobs_limit: int = 25):
        if job_category.lower() not in self.job_categories:
            raise Exception("The job you are searching for isn't here.")

        self.job_category = job_category.lower()
        self.site_url = ""
        self.site_url = self.devbg_url + self.get_job_category_url(self.job_category)
        self.jobs_counter = 0
        self.jobs_limit = jobs_limit
        self.npo_jobs = []

    def search_for_jobs(self):
        while True:
            response = requests.get(self.site_url)
            data = response.text
            soup = BeautifulSoup(data, "html.parser")

            jobs = soup.find_all("div", {"class": "job-list-item"})
            for job in jobs:
                job_title = job.find("h6", {"job-title"}).text
                post_date = job.find("span", {"class": "date date-with-icon"}).text
                location = job.find("span", {"class": "badge"}).text
                company_name = job.find("span", {"class": "company-name hide-for-small"}).text
                link = job.find("a", {"class": "overlay-link"}).get("href")
                job_skills = self.get_required_skills(link=link)
                self.jobs_counter += 1
                self.npo_jobs.append([job_title, post_date, location, company_name, link, job_skills])

                if self.jobs_counter >= self.jobs_limit:
                    return self.__repr__()

            try:
                url_next_page_tag = soup.find("a", {"class": "next page-numbers"})
                if url_next_page_tag.get("href"):
                    self.site_url = url_next_page_tag.get("href")
            except AttributeError:
                return self.__repr__()

    def print_jobs(self):
        for i in range(len(self.npo_jobs)):
            title = self.npo_jobs[i][0]
            date = self.npo_jobs[i][1]
            location = self.npo_jobs[i][2]
            company = self.npo_jobs[i][3]
            skills = "".join(["\n\t-" + x for x in self.npo_jobs[i][5]])

            print(f"Title: {title}\nPosted on: {date}\n"
                  f"Location: {location}\nCompany: {company}\n"
                  f"Tags: {skills}\n")

    @staticmethod
    def get_job_category_url(job_category: str):
        return {"backend development": "jobs/back-end-development/",
                "frontend development": "jobs/front-end-development/",
                "fullstack development": "jobs/full-stack-development/",
                "infrastructure": "jobs/operations/",
                "quality assurance": "jobs/quality-assurance/",
                "pm/ba and more": "jobs/pm-ba-and-more/",
                "mobile development": "jobs/mobile-development/",
                "data science": "jobs/data-science/",
                "erp/crm development": "jobs/erp-crm-development/",
                "ui/ux, arts": "jobs/ui-ux-and-arts/"}[job_category]

    @staticmethod
    def get_required_skills(link):
        response = requests.get(link)
        data = response.text
        link_soup = BeautifulSoup(data, "html.parser")

        job_skills = link_soup.find_all("a", {"class": "pill"})
        job_skills_list = []

        for skill in job_skills:
            job_skill = skill.text.split(" ")[:-1]
            job_skills_list.append(" ".join(job_skill))

        return job_skills_list
        # return '\n\t-'.join(job_skills_list)

    def put_in_a_file(self):
        if len(self.npo_jobs) > 0:
            with open("devbg_jobs.csv", "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerows(self.npo_jobs)
        else:
            raise Exception("You need to have jobs to put them in a file!")

    def __repr__(self):
        return f"Job category{self.job_category}\nJobs counter: {self.jobs_counter}"

# TODO: change the logic with categories
# TODO: make a file namer function
# TODO: add junior/intern and it management categories
