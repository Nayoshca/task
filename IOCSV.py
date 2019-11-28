# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import codecs
import csv
import urllib.parse
import os
from ArticleData import ArticleData 
def LoadSave():
    contents=""
    if(os.path.exists('save.txt')):
        f=open("save.txt", "r")
        contents =f.read()
        f.close() 
    return contents

s = LoadSave()
if s:
    csvfile = open('Mawdoo3Data.csv', 'a', newline='' ,encoding='utf_8_sig')
    fieldnames = ['Article_Name', 'Article_description','Article_keywords','Article_category','Article_Sub_category','Article_views','Article_index','Article_ref','Article_text']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
else:
    csvfile = open('Mawdoo3Data.csv', 'w', newline='' ,encoding='utf_8_sig')
    fieldnames = ['Article_Name', 'Article_description','Article_keywords','Article_category','Article_Sub_category','Article_views','Article_index','Article_ref','Article_text']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
def SaveToCSV( ArticleData  ):
    #save to CSV     
    writer.writerow({
                'Article_Name': ArticleData.Article_Name, 
                'Article_description': ArticleData.Article_description, 
                'Article_keywords': ArticleData.Article_keywords, 
                'Article_category': ArticleData.Article_category,
                'Article_Sub_category': ArticleData.Article_Sub_category, 
                'Article_views': ArticleData.Article_views, 
                'Article_index': ArticleData.Article_index,
                'Article_ref': ArticleData.Article_ref, 
                'Article_text': ArticleData.Article_text
                })
    csvfile.flush()

def SaveLastRun(data):
    f= open("save.txt","w+")
    f.truncate(0) 
    f.write(data)
    f.close() 





