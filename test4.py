# bruh
import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
from time import sleep
from my_functions import int_verify

# take unfamiliar skills from User
print("what kind of skills that you do not wanna work with?\n(each skill type it in different line and"
      "you finished press enter)")
issues = ["I had to add some thing here"]
while True:
    issue = input(">").lower()
    if issue == "":
        break
    issues.append(issue)

limit = input("How many page you pages you want to check?\n")
while True:
    try:
        limit = int(limit)
        break
    except ValueError:
        print("please pick a number :")
        limit = input()
limit = int(limit)
page_num = 1

print(f"Processing Start...")

while True:
    global staff
    while True:

        # get url ready to use
        url = "https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=python&searchBy=0" \
              "&rdoOperator=OR&searchType=personalizedSearch&luceneResultSize=25&postWeek=60&txtKeywords=python&pDate=I" \
              f"&sequence=2&startPage={page_num} "
        result = requests.get(url).content
        soup = BeautifulSoup(result, "lxml")

        # taking what we wanted from the url
        titles = soup.find_all("strong", class_="blkclor")
        companies = soup.find_all("h3", class_="joblist-comp-name")
        skills = soup.find_all("span", class_="srp-skills")
        times = soup.find_all("span", class_="sim-posted")
        link = soup.find_all("h2")

        # make it has ability to get read
        title = []
        company = []
        responsibility = []
        skill = []
        time = []
        links = []
        for i in range(len(times)):
            pb = skills[i].text.replace(" ", "").strip()
            for issue in issues:
                if issue in pb or issue == "":
                    print("deleted job")

                elif issue not in pb:
                    print("added job")
                    skill.append(skills[i].text.replace(" ", "").strip())
                    title.append(titles[i].text)
                    company.append(companies[i].text.strip())
                    time.append(times[i].text.strip())
                    links.append(link[i].find("a").attrs["href"])

        # for link in links:
        extra_space = '___________________________'
        for link in links:
            result = requests.get(link)
            src = result.content
            soup = BeautifulSoup(src, "lxml")
            responsibilities = soup.find("div", class_="jd-desc job-description-main").text.strip()
            responsibility.append(responsibilities[len(extra_space):])
        staff = [title, company, responsibility, skill, time, links]
        print(page_num == limit)
        print(page_num)
        print(limit)
        page_num += 1
        if page_num >= limit:
            break

        print("reloaded")

    data = zip_longest(*staff)
    # extracting information in csv file:
    with open("TimesJobs.csv", "w") as file:
        wr = csv.writer(file)
        wr.writerow(["title", "company", "responsibility", "skill", "date", "link"])
        wr.writerows(data)
    print("your file is ready!!")
    sleep(15 * 60)

