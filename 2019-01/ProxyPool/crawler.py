from utils import get_page
from pyquery import PyQuery as pq

class Crawler():
    def get_proxies(self):
        proxies = []
        for proxy in self.crawl_goubanjia():
            proxies.append(proxy)
        return proxies

    def crawl_goubanjia(self):
        start_url = 'http://www.goubanjia.com/'
        html = get_page(start_url)
        doc = pq(html)
        items = doc('td.ip').items()
        for item in items:
            item.find('p').remove()
            yield item.text().replace('\n', '')

if __name__ == '__main__':
    crawler = Crawler()
    crawler.crawl_goubanjia()