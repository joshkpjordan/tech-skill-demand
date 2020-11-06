import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

prefix = "https://www.seek.co.az"
# https://www.seek.co.nz/jobs-in-marketing-communications
current_category_link = "https://www.seek.co.nz/jobs-in-information-communication-technology"

total_pages_in_category = 105
        
raw_job_text = "" # string to put all the job posts for this job category
page = 1
    
# scrape 6 pages of data unless there are fewer
while page < total_pages_in_category:
    # Get data from the seek search page for "data"
    webpage_response = requests.get(current_category_link + "?page=" +str(page)) # loop through each page until we have data we need
    webpage = webpage_response.content
    soup = BeautifulSoup(webpage, "html.parser")

    # Get all the links for jobs
    listing_links = soup.find_all(attrs={"class": "_1w1o77v"}) # seek CSS class to get links to each job page

    links = []
    # strip the url string of unnecessary cookies and append to prefix
    for a in listing_links:
        links.append(prefix + a["href"][0:13])

    for link in links:
        jobpage_response = requests.get(link)
        jobpage = jobpage_response.content
        job_soup = BeautifulSoup(jobpage, "html.parser")
        job_div = job_soup.select(".WaMPc_4") # Seek css class to get the div containing p and ul, li tags
    
        # get <p> and add a trailing space to all text, remove /xa0
        try:
            p = job_div[0].find_all("p")
        except IndexError:
            p = ""
        
        p_text = ""
        for e in p:
            text = e.get_text()
            p_text += text.ljust(len(text)+1)
        p_text = p_text.replace(u"\xa0",u" ")
      
        # check if li tags exist
        try:
            all_li = job_div[0].ul.find_all("li")
        except AttributeError:
            all_li = ""
   
        # get <li> and add a trailing space to all text, remove /xa0
        li_text = ""
        for e in all_li:
            text = e.get_text()
            li_text += text.ljust(len(text)+1)
        li_text = li_text.replace(u"\xa0",u" ")
    
        raw_job_text += p_text + li_text

    
    page += 1
    
# clean the text for the job posts in this category
cleaned = re.sub('\W+', ' ', raw_job_text).lower()
       
now = datetime.now()
f = open("itnz1.txt", "x")
f.write(str(cleaned))
f.close()
