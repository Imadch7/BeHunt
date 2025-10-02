import bs4
from . import http
import json


class spider:

    def __init__(self):
        self.http = http.HTTPRequestHandler()

    def gather_links(self, url, headers=None):
        url_forms={}
        response = self.http.send_GET_request(url, headers=headers)
        if response:
            #find all tags
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            links = [a.get('href') for a in soup.find_all('a', href=True)]
            forms = [a.get('form') for a in soup.find_all('form')]
            textareas = [a.get('textarea') for a in soup.find_all('textarea')]
            inputs = [a.get('input') for a in soup.find_all('input')]
            selects = [a.get('select') for a in soup.find_all('select')]

            tags = {links,forms,textareas,inputs,selects}
            url_forms[url] = tags

        return url_forms
    