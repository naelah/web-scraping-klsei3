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

def linksByKeys(keys):
    ## return: a dictionary of links

    links_dic = dict()
    # scrape key words one by one
    for key in keys:
        print('Scraping position: ', key, ' ...')
        links_dic[key] = linksByKey(key)
        print('{} {} positions found!'.format(len(links_dic[key]),key))
    return links_dic


""" get all headline links """
def linksByKey(key):
    ## key: name of file
    ## return: a list of links

    # open saved html file
    soup = BeautifulSoup(open(r"C:\Users\naela\Documents\Pet projects\web-scraping-klsei3\topglove.html", encoding="UTF-8").read(), "html.parser")

    header_links = []

    # get headline table
    table = soup.find('table', id="nbTable")

    # saving all links in the table
    links = table.find_all('a', href=True)
    for link in links:
        header_links.append(link['href'])

    return header_links

""" parse and saving dataframe into csv"""
def parseLinks(links_dic):
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


""" extract details from headline page """
def getHighlightDetail(highlight_href):
    ## highlight_href: an article url
    ## retun: details from the page

    print('Scraping ',highlight_href,'...')
    driver.get(highlight_href)
    driver.encoding = "GBK"

    try:
        date=driver.find_element_by_xpath("//time").text
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

    # folder name
    key_words = ['topglove']
    s = requests.session()
    links_dic = linksByKeys(key_words)
    parseLinks(links_dic)

if __name__ == '__main__':
	main()
