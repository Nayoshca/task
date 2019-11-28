from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import codecs
import csv
import urllib.parse
import urllib.error
import logging

def connectTo(url):
    try:
     #Open connection & grab the page
        uClient = uReq(url)
        #print(uClient)
        #Parses html to a soup data structure
        page_html = soup(uClient.read(), "html.parser") 
        uClient.close()

        return page_html
    except IOError as err:
        print("I/O error: {0}".format(err))
        logging.error("I/O error: {0}".format(err))
    except ValueError:
        print ("Could not convert data to an integer.")
        logging.error ("Could not convert data to an integer.")
    except UnicodeDecodeError:    
        self.redirect("/urlparseerror?error=UnicodeDecodeError")
        
    except:
        print ("Unexpected error:", sys.exc_info()[0])
        logging.error ("Unexpected error:", sys.exc_info()[0])
        raise
       
