from utils import get_page
from pyquery import PyQuery as pq

class Crawler():
    def get_proxies(self):
        proxies = []
        for proxy in self.crawl_ip3366():
            proxies.append(proxy)
        for proxy in self.crawl_xicidaili():
            proxies.append(proxy)
        for proxy in self.crawl_iphai():
            proxies.append(proxy)
        return proxies

    # 代理无效
    def crawl_goubanjia(self):
        start_url = 'http://www.goubanjia.com/'
        html = get_page(start_url)
        doc = pq(html)
        items = doc('td.ip').items()
        for item in items:
            item.find('p').remove()
            yield item.text().replace('\n', '')

    # 请求服务器返回521，且代理无效
    def crawl_daili66(self, page_count=4):
        start_url = 'http://www.66ip.cn/{}.html'
        for page in range(1, page_count+1):
            url = start_url.format(page)
            print(url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    # 可用
    def crawl_ip3366(self, page_count=4):
        start_url = 'http://www.ip3366.net/?stype=1&page={}'
        for page in range(1, page_count+1):
            url = start_url.format(page)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('#container #list tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    # 代理无效
    def crawl_kuaidaili(self, page_count=4):
        start_url = 'https://www.kuaidaili.com/free/inha/{}/'
        for page in range(1, page_count + 1):
            url = start_url.format(page)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('#content table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    # 可用
    def crawl_xicidaili(self, page_count=3):
        start_url = 'https://www.xicidaili.com/nn/{}'
        for page in range(1, page_count + 1):
            url = start_url.format(page)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('#ip_list tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(2)').text()
                    port = tr.find('td:nth-child(3)').text()
                    yield ':'.join([ip, port])

    # 可用
    def crawl_iphai(self):
        start_url = 'http://www.iphai.com/free/ng'
        html = get_page(start_url)
        if html:
            doc = pq(html)
            trs = doc('.container table tr:gt(0)').items()
            for tr in trs:
                ip = tr.find('td:nth-child(1)').text()
                port = tr.find('td:nth-child(2)').text()
                yield ':'.join([ip, port])

    # 代理无效
    def crawl_data5u(self):
        start_url = 'http://www.data5u.com/free/gngn/index.shtml'
        html = get_page(start_url)
        if html:
            doc = pq(html)
            uls = doc('.wlist ul .l2').items()
            for ul in uls:
                ip = ul.find('span:nth-child(1)').text()
                port = ul.find('span:nth-child(2)').text()
                yield ':'.join([ip, port])

if __name__ == '__main__':
    crawler = Crawler()
    proxies = crawler.crawl_data5u()
    for proxy in proxies:
        print(proxy)