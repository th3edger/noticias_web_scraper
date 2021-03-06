import bs4
import requests

from common import config

class NewsPage:

    def __init__(self, news_site_id, url):
        self._config = config()['news_sites'][news_site_id]
        self._queries = self._config['queries']

        self._html = None

        self._visit(url)


    def _select(self, query_string):
        return self._html.select(query_string)


    def _visit(self, url):

        cabeceras = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        respuesta = requests.get(url, headers=cabeceras)
        respuesta.raise_for_status()

        self._html = bs4.BeautifulSoup(respuesta.text, 'html.parser')




class HomePage(NewsPage):

    def __init__(self, news_site_id, url):
        self._url = url
        super().__init__(news_site_id, url)


    @property
    def article_links(self):
        lista_links = []
        for link in self._select(self._queries['homepage_article_links']):
            if link and link.has_attr('href'):
                lista_links.append(link)
        
        return set(link['href'] for link in lista_links)



class ArticlePage(NewsPage):

    def __init__(self, news_site_id, url):
        self._url = url
        super().__init__(news_site_id, url)
    
    @property
    def body(self):
        resultado = self._select(self._queries['article_body'])

        return resultado[0].text if len(resultado) else ''

    @property
    def title(self):
        resultado = self._select(self._queries['article_title'])

        return resultado[0].text if len(resultado) else ''
    
    @property
    def url(self):
        return self._url