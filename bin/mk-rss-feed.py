#!/usr/bin/env python

import sys
import urllib
import urlparse
import logging
import datetime
import hashlib
 
import PyRSS2Gen
from BeautifulSoup import BeautifulSoup

class UserAgent(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'
 
class TinyLetter:
    
    def __init__(self, url):

        if not url.endswith('/'):
            url = url + '/'

        self.url = url
        self.ua = UserAgent()

    def as_rss(self, fh):

        page = self.ua.open(self.url) 
        text = page.read()
        page.close()
 
        soup = BeautifulSoup(text)
        title = soup.title.string
        title = title.strip()

        byline = soup.findAll('span', {'class': 'byline'})
        byline = byline[0]
        byline = byline.string
        byline = byline.strip()

        items = []

        letters = self.url + 'letters/'

        for item in self.process_as_rss(letters):
            items.append(PyRSS2Gen.RSSItem(**item))

        now = datetime.datetime.now()

        rss = PyRSS2Gen.RSS2(
            title = title,
            link = url,
            description = byline,
            lastBuildDate = now,
            items = items
        )

        rss.write_xml(fh)

    def process_as_rss(self, url, items=[], max_items=15):

        logging.debug("parsing %s" % url)

        try:
            page = self.ua.open(url)
            text = page.read()
            page.close()

        except Exception, e:
            logging.error("Failed to open %s, because %s" % (url, e))
            return items
 
        try:
            soup = BeautifulSoup(text)
        except Exception, e:
            logging.error("Failed to parse text, because %s" % e)
            return items

        # Insert sound of old timers chuckling here...

        try:
            link = soup.find('meta', {'name': 'og:url'})
            link = link['content']
        except Exception, e:
            logging.error("Failed to parse link, because %s" % e)
            link = url
            
        try:
            title = soup.find('meta', {'name': 'twitter:title'})
            title = title['content']
        except TypeError, e:
            title = soup.find('meta', {'property': 'og:title'})
            title = title['content']
        except Exception, e:
            logging.error("Failed to parse title, because %s" % e)
            title = url

        try:
            desc = soup.find('meta', {'name': 'twitter:description'})
            desc = desc['content']
        except TypeError, e:
            desc = soup.find('meta', {'property': 'og:description'})
            desc = desc['content']
        except Exception, e:
            logging.error("Failed to parse description, because %s" % e)
            desc = ""

        try:
            header = soup.find('div', {'id': 'message-heading'})
            date = header.find('div', {'class': 'date'})
            date = date.string
            date = date.strip()
            pubdate = datetime.datetime.strptime(date, "%B %d, %Y") 

        except Exception, e:
            logging.error("Failed to parse date because %s, so just using 'now' instead" % e)
            pubdate = datetime.datetime.now()
            
        hash = hashlib.md5()
        hash.update(link)
        guid = hash.hexdigest()

        item = {
            'title': title,
            'link': link,
            'description': desc,
            'guid': guid,
            'pubDate': pubdate
        }

        items.append(item)

        if len(items) == max_items:
            logging.debug("Reached max items limit, all done")
            return items

        for tag in soup.findAll('a', href=True):
            
            css = tag.get('class', None)
            
            if not css:
                continue
                
            if not css == 'paging-button next':
                continue

            next = 'https://tinyletter.com' + tag['href']
            items = self.process_as_rss(next, items)

        return items

if __name__ == '__main__':

    url = sys.argv[1]
    rss = sys.stdout

    tl = TinyLetter(url)
    tl.as_rss(rss)
