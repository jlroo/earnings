#!python3
import requests
import threading
from bs4 import BeautifulSoup


def get_proxies():
    timeout = 610
    proxy_url = "https://www.us-proxy.org/"
    threading.Timer(timeout, get_proxies).start()
    response = requests.get(proxy_url, timeout=5)
    html = BeautifulSoup(response.content, 'html.parser')
    table = html.find('table', {'class': 'table'})
    table = table.findAll("tr")
    addr = [i.findAll("td")[0].text + ":" + i.findAll("td")[1].text for i in table[1:-2]]
    with open('proxies/proxy_file.txt', 'a') as outfile:
        outfile.writelines("\n" + "\n".join(addr))


if __name__ == "__main__":
    get_proxies()
