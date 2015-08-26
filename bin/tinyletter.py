#!/usr/bin/env python

import sys
import re
import urllib
import urlparse
import logging
import datetime
import hashlib
import HTMLParser
 
from BeautifulSoup import BeautifulSoup
import PyRSS2Gen

class UserAgent(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'
 
class TinyLetter:
    
    def __init__(self, url):

        if not url.endswith('/'):
            url = url + '/'

        self.url = url
        self.ua = UserAgent()

        self.html_parser = HTMLParser.HTMLParser()

    def as_rss(self, fh, **kwargs):

        page = self.ua.open(self.url) 
        text = page.read()
        page.close()
 
        soup = BeautifulSoup(text)
        title = soup.title.string
        title = title.strip()

        byline = soup.findAll('span', {'class': 'byline'})
        byline = byline[0]
        byline = byline.string

        if byline:
            byline = byline.strip()

        items = []

        letters = self.url + 'letters/'

        rss_map = {
            'title': 'title',
            'description': 'description',
            'link': 'link',
            'guid': 'id',
            'pubDate': 'date',
            }

        for item in self.extract(letters, **kwargs):

            rss_item = {}

            for this, that in rss_map.items():
                rss_item[this] = item.get(that)

            items.append(PyRSS2Gen.RSSItem(**rss_item))

        now = datetime.datetime.now()

        rss = PyRSS2Gen.RSS2(
            title = title,
            link = self.url,
            description = byline,
            lastBuildDate = now,
            items = items
        )

        rss.write_xml(fh)

    def as_markdown(self, fh, **kwargs):

        kwargs['entextify'] = True;

        for item in self.as_list(**kwargs):
            
            title = item.get('title', 'INVISIBLE NEWSLETTER TITLE')
            link = item.get('link', 'INVISIBLE NEWSLETTER LINK')

            fh.write("# %s\n" % title)
            fh.write("## %s\n" % link)
            fh.write("\n")

            for ln in item.get('text', []):
                fh.write(ln)
                fh.write("\n\n")

            fh.write("--\n\n")

    def as_list(self, **kwargs):

        page = self.ua.open(self.url) 
        text = page.read()
        page.close()
 
        soup = BeautifulSoup(text)

        letters = self.url + 'letters/'
        
        for item in self.extract(letters, **kwargs):
            yield item

    # sudo make me a generator... (20150826/straup)

    def extract(self, url, **kwargs):

        items = kwargs.get('items', [])
        max_items = kwargs.get('max_items', 15)
        entextify = kwargs.get('entextify', False)

        max_items = int(max_items)

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
            
            if title:
                title = title['content']
            else:
                title = url

        except Exception, e:
            logging.error("Failed to parse title, because %s" % e)
            title = url

        try:
            desc = soup.find('meta', {'name': 'twitter:description'})
            desc = desc['content']
        except TypeError, e:
            desc = soup.find('meta', {'property': 'og:description'})

            if desc:
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
            'description': desc,
            'link': link,
            'id': guid,
            'date': pubdate,
            'text': []
        }

        if entextify:

            body = soup.find('div', {'class': 'message-body'})
            text = []

            if body:

                buffer = []

                for t in body(text=True):

                    t = t.strip()
                    
                    if len(t) == 0:
                        continue

                    t = self.html_parser.unescape(t)
                    buffer.append(t)

                    if len(t.split(" ")) > 1:
                        text.append(" ".join(buffer))
                        buffer = []
                    
                if len(buffer):
                    text.append(" ".join(buffer))

                item['text'] =  text

        items.append(item)

        if max_items > 0 and len(items) == max_items:
            logging.debug("Reached max items limit, all done")
            return items

        for tag in soup.findAll('a', href=True):
            
            css = tag.get('class', None)
            
            if not css:
                continue
                
            if not css == 'paging-button next':
                continue

            kwargs['items'] = items

            next = 'https://tinyletter.com' + tag['href']
            items = self.extract(next, **kwargs)
            
        return items
