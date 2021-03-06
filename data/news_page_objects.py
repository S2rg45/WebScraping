from os import link
from common import config
import requests
import bs4


class NewsPage:
    def __init__(self, news_site_uid, url):
        self._config = config()['sites'][news_site_uid]
        self._queries = self._config['queries']
        self._html = None
        self._url = url
        self._visit(url)

    def _select(self, query_string):
        return self._html.select(query_string)


    def _visit(self, url):
        response = requests.get(url)
        response.raise_for_status()
        self._html = bs4.BeautifulSoup(response.text, 'html.parser')



class HomePage(NewsPage):
    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)
    
    @property
    def article_links(self):
        link_list = []
        for link in self._select(self._queries['homepage_articule_link']):
            print("class",link)
            if link and link.has_attr('href'):
                link_list.append(link)
        return set(link['href'] for link in link_list)


class ArticulePage(NewsPage):

    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)

    
    @property
    def body(self):
        result = self._select(self._queries['articule_body'])
        return result[0].text if len(result) else ''


    @property 
    def title(self):
        result = self._select(self._queries['articule_title'])
        return result[0].text if len(result) else ''
    
    @property
    def url(self):
        return self._url