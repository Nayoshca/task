# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import codecs
import csv
import urllib.parse
from ArticleData import ArticleData
import connectBSToURL
from bs4 import element as elements
import logging
from string import printable
mawdoo3Url ='https://mawdoo3.com'

#input is article URL 
#output is Articla data

def extract( Article_URL ,catName,subCatName):
   "function_docstring"
   data = ArticleData()
   #Article in class of subcat:
   if set(Article_URL["href"]).difference(printable):
        ArticleInSubCatUrl = mawdoo3Url+urllib.parse.quote(Article_URL["href"])
   else :
       ArticleInSubCatUrl = mawdoo3Url+Article_URL["href"]
  # ArticleInSubCatUrl = mawdoo3Url+Article_URL["href"]
  # ArticleInSubCatUrl = mawdoo3Url+urllib.parse.quote(Article_URL["href"])
   #Open connection & grab the page
   Article_cat_page_html = connectBSToURL.connectTo(ArticleInSubCatUrl)    
   if type(Article_cat_page_html) == soup :        
       #get data
       Article_Name = Article_cat_page_html.find("h1", {"class": "title"})
       if(type(Article_Name)==elements.Tag):
           data.Article_Name = Article_Name.string.strip()
       else:
            data.Article_Name='غير معرف'
       #print(Article_Name)
       Article_description = Article_cat_page_html.find("meta", {"name": "description"})
       if(type(Article_description)==elements.Tag):
            data.Article_description = Article_description["content"].strip()
       else:
            data.Article_description='غير معرف'

       #print(Article_description)

       Article_keywords = Article_cat_page_html.find("meta", {"name": "keywords"})
       if(type(Article_keywords)==elements.Tag):
            data.Article_keywords = Article_keywords["content"].strip()
       else:
            data.Article_keywords='غير معرف'

       #print(Article_keywords)

       
       data.Article_category = catName
       #print(Article_category)


       data.Article_Sub_category = subCatName

       Article_views = Article_cat_page_html.find("div", {"class": "views"})
       if(type(Article_views)==elements.Tag):
            temp = Article_views.text.strip() 
            Article_views=[int(s) for s in temp.split() if s.isdigit()]
            data.Article_views = Article_views[0]
       else:
            data.Article_views= 0
       #print(Article_views)

       content = Article_cat_page_html.find("div", {"class": "mw-content-rtl"})
       Article_index =""
       if(type(content)==elements.Tag):         
           index = content.findAll("span",{"class":"toctext"})
           if(type(index)==elements.ResultSet):
               for i in index:
                   Article_index = Article_index + i.get_text().strip()+";"
               #print(Article_index)
           data.Article_index = Article_index
           Article_ref=""
           references = content.findAll("span",{"class":"reference-text"})
           for ref in references:
                Article_ref = Article_ref + ref.get_text().strip()+";"

       data.Article_ref=Article_ref

       Article_text =""
       mydivs = content.findAll(['div', 'ol','script'])
       if(type(mydivs)==elements.ResultSet):
       #print(mydivs)
           for tag in content:
               if  tag in mydivs :
                   continue
               else:
                   try:
                       Article_text = Article_text.strip() + tag.get_text().strip()
                   except AttributeError as e:
                       #logging.error("AttributeError: {0}".format(e))
                       continue

       data.Article_text = Article_text


       #data.display()
       return data
   else:
       pass