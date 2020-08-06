import requests # for web requests
from bs4 import BeautifulSoup # a powerful HTML parser
from selenium.webdriver import Chrome
import pandas as pd # for .csv file read and write
import re # for regular regression handling
from requests_html import HTMLSession
session = HTMLSession()
import lxml.html

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
path = r"C:/Users/naela/AppData/Local/Programs/Python/chromedriver.exe"
driver = Chrome(path)
#driver.implicitly_wait(2)

""" get all position <a> tags for the list of job roles, results stored in a dictionary
<a> tag example:
<a class="position-title-link" id="position_title_3" href="https://www.jobstreet.com.sg/en/job/data-analyst-python-sas-sqlbank-35k-to-5k-gd-bonus5-days-west-6111488?fr=21"
target="_blank" title="View Job Details - Data Analyst (Python / SAS / SQL)(BANK / $3.5K to $5K + GD BONUS / 5 Days / West)" data-track="sol-job" data-job-id="6111488"
data-job-title="Data Analyst (Python / SAS / SQL)(BANK / $3.5K to $5K + GD BONUS / 5 Days / West)" data-type="organic" data-rank="3" data-page="1" data-posting-country="SG">
<h2 itemprop="title">Data Analyst (Python / SAS / SQL)(BANK / $3.5K to $5K + GD BONUS / 5 Days / West)</h2></a>"""
def linksByKeys(keys):
    ## keys: a list of job roles
    ## return: a dictionary of links

    links_dic = dict()
    # scrape key words one by one
    for key in keys:
        print('Scraping position: ', key, ' ...')
        links_dic[key] = linksByKey(key)
        print('{} {} positions found!'.format(len(links_dic[key]),key))
    return links_dic


""" get all position <a> tags for a single job role, triggered by linksByKeys function """
def linksByKey(key):
    ## key: a job role
    ## return: a list of links

    # parameters passed to  http get/post function
    base_url = 'https://klse.i3investor.com/m/stock/headlines/7113.jsp'

    soup = BeautifulSoup(open(r"C:\Users\naela\Documents\Pet projects\web-scraping-klsei3\topglove.html", encoding="UTF-8").read(), "html.parser")

    header_links = []
  #  pay_load = {'key':'','area':1,'option':1,'pg':None,'classified':1,'src':16,'srcr':12}
  #  pay_load['key'] = key
    page = requests.get(base_url) # connect to page
    html = page.content # get html content
 #   soup = BeautifulSoup(html, 'lxml') #beautify the html page`
    table = soup.find('table', id="nbTable")
    links = table.find_all('a', href=True)
    for link in links:
        header_links.append(link['href'])

    return header_links

""" parse HTML strings for the list of roles
<a> tag example:
<a class="position-title-link" id="position_title_3" href="https://www.jobstreet.com.sg/en/job/data-analyst-python-sas-sqlbank-35k-to-5k-gd-bonus5-days-west-6111488?fr=21"
target="_blank" title="View Job Details - Data Analyst (Python / SAS / SQL)(BANK / $3.5K to $5K + GD BONUS / 5 Days / West)" data-track="sol-job" data-job-id="6111488"
data-job-title="Data Analyst (Python / SAS / SQL)(BANK / $3.5K to $5K + GD BONUS / 5 Days / West)" data-type="organic" data-rank="3" data-page="1" data-posting-country="SG">"""
def parseLinks(links_dic):
    ## links_dic: a dictionary of links
    ## return: print parsed results to .csv file

    for key in links_dic:
        jobs = []
        for link in links_dic[key]:
            jobs.append([key] + getHighlightDetail(link))

        # transfrom the result to a pandas.DataFrame
        result = pd.DataFrame(jobs,columns=['key_word','date','title','url','content'])

        # save result,
        file_name = key+'.csv'
        result.to_csv(file_name,index=False)


""" parse a single <a> tag, extract the information, triggered by parseLinks function """
def parseLink(link):
	## link: a single position <a> tag
	## return: information of a single position

	# unique id assigned to a position
	highlight_id = link['data-job-id'].strip()
	# job title
	highlight_title = link['data-job-title'].strip()
	# posted country
	highlight_content = link['data-posting-country'].strip()
	# the web address towards to the post detail page
	highlight_href = link['href']
	# go to post detail page, and fetch information
#	other_detail = getJobDetail(job_href)
	return [job_id,job_title,country,job_href] + other_detail


""" extract details from post detail page """
def getHighlightDetail(highlight_href):
    ## job_href: a post url
    ## retun: post details from the detail page

    print('Scraping ',highlight_href,'...')
    driver.get(highlight_href)
	
    try:
        date=soup.find('time').text
    except:
        date = None
    try:
        highlight_title=driver.title
    except:
        highlight_title = None
    try:
        highlight_content = driver.find_element_by_id("blogcontent").text
    except:
        highlight_content = None
   
    return [date, highlight_title, highlight_href, highlight_content]

def main():

    # a list of job roles to be crawled
    key_words = ['topglove']
    s = requests.session()
    links_dic = linksByKeys(key_words)
    parseLinks(links_dic)

if __name__ == '__main__':
	main()
