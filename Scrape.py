# -*- coding: utf-8 -*-
import logging
from bs4 import BeautifulSoup as soup  # HTML data structure
from bs4 import element as elements
from urllib.request import urlopen as uReq  # Web client
import codecs
import csv
import urllib.parse
import urllib.error
import sys
import ArticleData 
import ArticleDataExtractor 
import IOCSV
import connectBSToURL
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
firstLoad=True
Pi=0
Pj=0
Pk=0
P = IOCSV.LoadSave()
print("P")
print(P)
if P:
    P = P.split('|')
    print(P)
    if(P[0]==0):
        Pi=int(P[0])-1
    else:
        Pi=int(P[0])
    if(P[1] ==0):
        Pj=int(P[1])-1
    else:
        Pj=int(P[1])
    if(P[2] ==0):
        Pk=int(P[2])-1
    else:
        Pk=int(P[2])

print(Pi)
print(Pj)
print(Pk)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("chromedriver", chrome_options=options)

debuger = True

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)
mawdoo3Url ='https://mawdoo3.com'
def get_sub_cat_page(cat_url):
     
    driver.get(cat_url)

    while True:
        try:

            more_button = driver.find_element_by_id("more_results_btn")
            if(type(more_button)==webdriver.remote.webelement.WebElement):
        
                if more_button.is_displayed():
                    driver.execute_script("arguments[0].click();", more_button)
                    time.sleep(1)
                else:
                    print("heddin")
                    break
            else:
                print("no web element")
                break
        except NoSuchElementException:
            print ("no web element")
            break
     
    page_source = driver.page_source
    soup1 = soup(page_source, 'lxml')

    return soup1

website_html = connectBSToURL.connectTo(mawdoo3Url)
if(type(website_html)==soup):
    print("scraper is starting ...")
    print()
    logging.debug('scraper is started')
    counter1 = 0
    cats = website_html.select('div[class*="category "]')
    if(type(cats)==list):

        cats=cats[Pi:]
        for i, MainCat in enumerate(cats):
            if(type(MainCat)==elements.Tag):
                if debuger :
                    catHead = MainCat.h2
                    if(type(catHead)==elements.Tag):
                        catlink=catHead.a["href"]
                        if(type(catlink)==str):
                            catName = catHead.find("span",{"class":"title"})
                            if(type(catName)==elements.Tag):
                                catName = catName.text.strip()
                                if(type(catName)!=str):
                                    catName = 'غير معرف'
                                counter1 = counter1 +1
                               
                                print("From category " + str(i+1+Pi))
                                logging.debug("Scraping from Category "+  str(i+1+Pi))
                               
                                
                                #sub categories in Main categories:
                                SubCatUrl = mawdoo3Url+urllib.parse.quote(catlink)
                                cat_page_html = connectBSToURL.connectTo(SubCatUrl)
                                if(type(cat_page_html)==soup):
                                    tmp= cat_page_html.find_all("ul",{"class":"list horizontal"})
                                    if(type(tmp)==elements.ResultSet):
                                        subCatsHead = tmp[0]
                                        #print(type(subCatsHead))
                                        if(type(subCatsHead)==elements.Tag):
                                            subCatsHead = subCatsHead.find_all("li")
                                            #print(subCatsHead)
                                            counter2 = 0
                                            if(i==0):
                                                subCatsHead=subCatsHead[Pj:]
                                            for j, subCat in enumerate(subCatsHead) :
                                                if(type(subCat)==elements.Tag):
                                                    if debuger:
                                                        counter2 = counter2 +1
                                                        if(i==0 ):
                                                            print("-->From sub category " +  str(j+Pj+1))
                                                            logging.debug("-->Scraping from sub category " + str(j+Pj+1))
                                                        else:    
                                                            print("-->From sub category " +  str(j+1))
                                                            logging.debug("-->Scraping from sub category " + str(j+1))
                                                        
                                                        subCatLink = subCat.a["href"]
                                                        if(type(subCatLink)==str):
                                                            #print(subCatLink)
                                                            subCatName = subCat.a
                                                            if(type(subCatName)==elements.Tag):
                                                                subCatName=subCatName.text.strip()
                                                                if(type(subCatName)!=str):
                                                                    subCatName='غير معرف'
                                                                #print(subCatName)
                                                                counter = 0
                                                                #print(subCatName)
                                                                #connect to subcats in main category:
                                                                SubCatUrl = mawdoo3Url+urllib.parse.quote(subCatLink)
                                                                class_cat_page_html = get_sub_cat_page(SubCatUrl)
                                                                if(type(class_cat_page_html)==soup):
                                                                    Articles = class_cat_page_html.findAll("a",{"class":"category-box"})
                                                                    print(len(Articles))
                                                                    if(type(Articles) == elements.ResultSet):
                                                                        logging.debug("Adding ("+str(len(Articles)) +") article")
                                                                        if(i==0 and j==0):
                                                                            Articles=Articles[Pk:]
                                                                        for k, A in enumerate( Articles):
                                                                            if debuger:
                                                                                data = ArticleDataExtractor.extract(A,catName,subCatName )
                                                                                if type(data) == ArticleData.ArticleData :
                                                                                    
                                                                                    
                                                                                    IOCSV.SaveLastRun(str(i+Pi)+"|"+str(j+Pj)+"|"+str(k+Pk+1))
                                                                                    
                                                                                    IOCSV.SaveToCSV(data)
                                                                                    counter = counter + 1
                                                                                    if(i==0 and j==0):
                                                                                        print("----> "+str(k+Pk+1) + "  Articles were added" )
                                                                                    else:
                                                                                        print("----> "+str(k+1) + "  Articles were added" ) 

                                                                                    
                                                                                else:
                                                                                    print('passed error')
                                                                                    logging.error('Article '+str(counter)+ 'was not found')
                                                                            else:
                                                                                break
                                                                        firstLoad=False
                                                                    else:
                                                                        print("corrupted Article link")
                                                                        logging.error("corrupted Aeticle link")
                                                                else:
                                                                    print("sub category page was not found")
                                                                    logging.error("sub category page was not found")
                                                            else:
                                                                print("sub catagory link tag was not found")
                                                                logging.error("sub catagory link tag was not found")
                                                        else:
                                                            print("sub catagory link was not found")
                                                            logging.error("sub catagory link was not found")
                                                    else:
                                                        break
                                                else:
                                                    print("sub catagory tag was not found")
                                                    logging.error("sub catagory tag was not found")
                                        else:
                                            print("sub catagories tags was not found")
                                            logging.error("sub catagories tags was not found")
                                    else:
                                        print("categories list eas not found")
                                        logging.error("categories list eas not found")


                                else:
                                    print("categoy page not found")
                                    logging.error("categoy page not found")

                            else:
                                print("categiry name tag eas not found")
                                logging.error("categiry name tag eas not found")
                        else:
                            print("categiry link not founed")
                            logging.error("categiry link not founed")
                    else:
                        print("category tag was not found")
                        logging.error("category tag was not found")
                else:
                 break
            else:
                print("Problem with grabbing category")
                logging.error("Problem with grabbing category")
    else:
        print("no categories founed")
        logging.error("no categories founed")
else:
    print("no connection")
    logging.error("no connection")

   
   

