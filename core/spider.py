import re
import bs4
import json
import os
try:
    from core.http import HTTPRequestHandler
    from core.url import URL
except ImportError:
    from http import HTTPRequestHandler
    from url import URL

class spider:

    def __init__(self):
        self.http = HTTPRequestHandler()
        self.Url = URL()
        self.visited_urls = set()
        self.TAGS = {}

    def Extract_TAGS(self, url, headers=None):
        url = self.Url.normalize_url(url)
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)
        response = self.http.send_GET_request(url, headers=headers)
        if response and response.text:
            try:
                try:
                    soup = bs4.BeautifulSoup(response.text, 'html.parser')
                except:
                    soup = bs4.BeautifulSoup(response.text, 'lxml')

                LINKS = [a.get('href') for a in soup.find_all('a', href=True)]
                FORMS = [str(form) for form in soup.find_all('form')]
                TEXTAREAS = [str(textarea) for textarea in soup.find_all('textarea')]
                INPUTS = [str(inp) for inp in soup.find_all('input')]
                SELECTS = [str(sel) for sel in soup.find_all('select')]
                SCRIPT= [str(scr) for scr in soup.find_all('script')]

                tags = {
                    "links": LINKS,
                    "forms": FORMS,
                    "textareas": TEXTAREAS,
                    "inputs": INPUTS,
                    "selects": SELECTS,
                    "script": SCRIPT
                }
                return tags
            except bs4.FeatureNotFound as e:
                print("Error: BeautifulSoup feature not found.")
                print(f"{e}")
                return None
    
    def crawl(self, url, headers=None):
        tags = self.Extract_TAGS(url, headers=headers)
        if tags:
            self.TAGS[url] = tags
        
    def save_TAGS(self, url):
        def convert(obj):
            if isinstance(obj, set):
                return list(obj)
            if isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [convert(i) for i in obj]
            return obj
        serializable_TAGS = convert(self.TAGS)
        base = self.Url.base_url(url)
        out_path = os.path.join('data/', f'{base}.json')
        with open(out_path, 'w',encoding='utf-8') as f:
            json.dump(serializable_TAGS, f, indent=4)
    
    '''
        Extract the ids from the specified tag in the saved json file.
        {
        "url":
            "inputs": [
                "<input id=\"entreprise_search\" name=\"entreprise_search\" placeholder=\"Chercher ...\" type=\"text\"/>",
                "<input class=\"checkbox\" id=\"mode\" style=\"height: 1px; width:0px;\" type=\"checkbox\"/>"
            ]
        }
    '''
    
    def get_tag_payload(self, url, tag='input'):

        base = self.Url.base_url(url)
        out_path = os.path.join('data/', f'{base}.json')

        
        if not os.path.exists(out_path):
            self.crawl(url)
            self.save_TAGS(url)

            if not os.path.exists(out_path):
                return []
        
        if tag=='script':
            return ['src']

        # Robust regex for id extraction
        # likely  id     =      "......"
        pattern = r'id\s*=\s*"([^"]+)"'
        payloads = []
        try:
            with open(out_path, 'r',encoding='utf-8') as f:
                data = json.load(f)
                if not data:
                    return []
                tags = data.get(url, {}).get(tag+"s", [])
                if not tags:
                    print("tags empty")
                    return []

                for tag_str in tags:
                    match = re.search(pattern, tag_str)
                    if match:
                        payloads.append(match.group(1))
                
            if payloads:
                return payloads
            else:
                print("it return nothing")
                return []
        except json.JSONDecodeError:
            return []


