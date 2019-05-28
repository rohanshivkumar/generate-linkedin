from lxml import html, etree
import requests
import re
import os
import traceback
import csv
import json
import random
import time
from googleapiclient.discovery import build
import tkinter as Tk
my_api_key = "" #Enter Your Google API Key
my_cse_id = ""  #Enter Your Google Custom Search Engine ID
my_glassdoor_email = "" #Enter your glassdoor email ID
my_glassdoor_pass = "" #Enter your glassdoor password

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    print(search_term)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    results = []
    try:
        for item in res['items']:
            if("linkedin.com" in item['link'] and "linkedin.com/jobs" not in item['link']
            and "linkedin.com/userp" not in item['link'] 
            and "linkedin.com/title" not in item['link']):
                results.append(item['link'])
        return results
    except KeyError:
        return results
        

def parse(keyword, place):
    csv_file = '%s-%s-job-results.csv' % (keyword, place)
    fieldnames = ['Name', 'Company', 'State',
        'City', 'Salary', 'Location', 'Url','LinkedIn']
    csvfile = open(csv_file, "w")
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    csvfile.close()
    headers = {	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, sdch, br',
                'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
                    'referer': 'https://www.glassdoor.com/',
                    'upgrade-insecure-requests': '1',
                    # 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15',
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive'
                }
    location_headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.01',
                        'accept-encoding': 'gzip, deflate, sdch, br',
                        'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
                        'referer': 'https://www.glassdoor.com/',
                        'upgrade-insecure-requests': '1',
                        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive'}
    data = {"term": place, "maxLocationsToReturn": 10}
    location_url = "https://www.glassdoor.co.in/findPopularLocationAjax.htm?"
    # try:
    # Getting location id for search location
    print("Fetching location details")
    location_response = requests.post(
        location_url, headers=location_headers, data=data).json()
    place_id = location_response[0]['locationId']
    job_listing_url = 'https://www.glassdoor.com/Job/jobs.htm'
    login_url = 'https://www.glassdoor.com/profile/login_input.htm'
    # Form data to get job results
    data = {
        'clickSource': 'searchBtn',
        'sc.keyword': keyword,
        'locT': 'C',
        'locId': place_id,
        'jobType': '',
        }
    login_data = {
        'username' : my_glassdoor_email,
        'password' : my_glassdoor_pass
    }
    job_listings = []
    if place_id:
        try:
            login_response = requests.post(login_url,headers = headers, data= login_data)
            cookies = login_response.cookies 
            print("Login successful")
        except Exception:
            print ("Login failed")
            print(traceback.print_exc())
            return False

        try:
            response = requests.post(job_listing_url, headers=headers, data=data,cookies = cookies)
            i = 0
            # extracting data from
            # https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=true&clickSource=searchBtn&typedKeyword=andr&sc.keyword=android+developer&locT=C&locId=1146821&jobType=
            csv_file = '%s-%s-job-results.csv' % (keyword, place)
            while(i < 3):
                page_listings = []
                csvfile = open(csv_file, "a")
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if(i != 0 and next_url):
                    link = str(next_url).replace(
                        "[", "").replace("]", "").replace("'", "")
                    print(link)
                    response = requests.get(link, headers=headers)
                parser = html.fromstring(response.text)
                # Making absolute url
                base_url = "https://www.glassdoor.com"
                parser.make_links_absolute(base_url)
                XPATH_NEXT_PAGE = '//li[@class="next"]/a/@href'
                XPATH_ALL_JOB = '//li[@class="jl"]'
                XPATH_NAME = './/a/text()'
                XPATH_JOB_URL = './/a/@href'
                XPATH_LOC = './/span[@class="subtle loc"]/text()'
                XPATH_COMPANY = './/div[@class="flexbox empLoc"]/div/text()'
                XPATH_SALARY = './/span[@class="green small"]/text()'
                listings = parser.xpath(XPATH_ALL_JOB)
                next_url = parser.xpath(XPATH_NEXT_PAGE)
                i += 1
                print("Scraping page %s" % i)
                j = 0
                for job in listings:
                    j += 1
                    raw_job_name = job.xpath(XPATH_NAME)
                    raw_job_url = job.xpath(XPATH_JOB_URL)
                    raw_lob_loc = job.xpath(XPATH_LOC)
                    raw_company = job.xpath(XPATH_COMPANY)
                    raw_salary = job.xpath(XPATH_SALARY)
                    # Cleaning data
                    job_name = ''.join(raw_job_name).strip('–') if raw_job_name else None
                    job_location = ''.join(raw_lob_loc) if raw_lob_loc else None
                    raw_state = re.findall(",\s?(.*)\s?", job_location)
                    state = ''.join(raw_state).strip()
                    raw_city = job_location.replace(state, '')
                    city = raw_city.replace(',', '').strip()
                    company = ''.join(raw_company).replace('–', '')
                    salary = ''.join(raw_salary).strip()
                    job_url = raw_job_url[0] if raw_job_url else None
                    job_key = job_name + "-" + company
                    if(job_key in job_listings):
                        continue
                    search_term = company +" " + job_name + ' \"manager\" OR \"director\" linkedIn' 
                    linkedinurl = google_search(search_term, my_api_key, my_cse_id, num=10,siteSearch = "linkedin.com")
                    jobs = {
                        "Name": job_name,
                        "Company": company,
                        "State": state,
                        "City": city,
                        "Salary": salary,
                        "Location": job_location,
                        "Url": job_url,
                        "LinkedIn": linkedinurl
                    }
                    job_listings.append(job_key)
                    page_listings.append(jobs)
                    writer.writerow(jobs)
                    time.sleep(random.randint(1, 3))
                print("Done with page %s, taking a break " % i)
                csvfile.close()
                time.sleep(20)
            return page_listings
        except Exception:
            print("Error occured scraping glassdoor")
            print(traceback.print_exc())
            return False
    else:
        print("location id not available")
        return False

    # except:
    # print("Failed to load locations")s   
def action(p,lbl,keyword,place):
    if(keyword.strip() and place.strip()):
        if(all(x.isalpha() or x.isspace() for x in keyword) and all(x.isalpha() or x.isspace() for x in place)):          
            lbl.config(state = Tk.NORMAL,text = "Fetching Job Details          ",fg = "black")
            lbl.update()
            p.config(text="Please Wait",state = Tk.DISABLED)
            p.update()
            try:
                scraped_data = parse(keyword,place)
                if(type(scraped_data) == bool):
                    print("Error occured")
                else:
                    print("Wrote data to output file \'%s-%s-job-results.csv\'"%(keyword, place))
            except Exception:   
                print(Exception)            
            lbl.config(state = Tk.NORMAL,text="                                                 ")
            lbl.update()
            p.config(text="Find Jobs",state = Tk.NORMAL)
            p.update()
        else:                                 
            lbl.config(state = Tk.NORMAL,text = "Please make sure entries\n contain only alphabets",fg = "red")
            lbl.update()
    else:                                 
        lbl.config(state = Tk.NORMAL,text = "Please enter both fields      ",fg = "red")
        lbl.update()
        
    

if __name__ == "__main__":
    master = Tk.Tk()
    master.title("Retrieve LinkedIn")
    master.geometry("300x170")
    master.resizable(False,False)
    Tk.Label(master, text="Job Name:",anchor=Tk.W,font ="Times").grid(row=0,sticky=Tk.W,padx = 3)
    Tk.Label(master, text="Location:",anchor=Tk.W,font ="Times").grid(row=1,sticky=Tk.W,padx = 3)
    e1 = Tk.Entry(master)
    e2 = Tk.Entry(master)
    e1.grid(row=0, column=1,sticky= Tk.W)
    e2.grid(row=1, column=1,sticky= Tk.W)
    x1 = Tk.Button(master, text='Quit',font ="Times",command=master.quit)
    x2 = Tk.Button(master, text='Find Jobs',font ="Times")
    x1.grid(row=5, column=1, sticky=Tk.W, pady=20)
    x2.grid(row=4, column=1, sticky=Tk.W, pady=1)
    lbl = Tk.Label(master, text="                  ",state = Tk.NORMAL,anchor = Tk.W)
    lbl.grid(row = 3,column = 1)
    x2.config(command = lambda:action(x2,lbl,e1.get(),e2.get()))
    master.mainloop()
    
