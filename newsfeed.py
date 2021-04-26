import feedparser
from bs4 import BeautifulSoup

class ParseFeed():

    def __init__(self, url):
        self.feed_url = url
        
    def clean(self, html):
        '''
        Get the text from html and do some cleaning
        '''
        soup = BeautifulSoup(html)
        text = soup.get_text()
        text = text.replace('\xa0', ' ')
        return text

    def parse(self):
        '''
        Parse the URL, and print all the details of the news 
        '''
        feeds = feedparser.parse(self.feed_url).entries
        finalresponse = {}
        for f in feeds:
            
            
            
            finalresponse = {
                'Description': self.clean(f.get("description", "")),
                'Published Date': f.get("published", ""),
                'Title': f.get("title", ""),
                'Url': f.get("link", "")
            }
        
        print(finalresponse)
        return finalresponse
            
