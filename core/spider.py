
import bs4
import json
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
            #find all tags
            try:
                try:
                    soup = bs4.BeautifulSoup(response.text, 'html.parser')
                except:
                    soup = bs4.BeautifulSoup(response.text, 'lxml')
                LINKS = [a.get('href') for a in soup.find_all('a', href=True)]
                FORMS = [a.get('form') for a in soup.find_all('form')]
                TEXTAREAS = [a.get('textarea') for a in soup.find_all('textarea')]
                INPUTS = [a.get('input') for a in soup.find_all('input')]
                SELECTS = [a.get('select') for a in soup.find_all('select')]

                tags = {"links":LINKS,
                        "forms":FORMS,
                        "textareas":TEXTAREAS,
                        "inputs":INPUTS,
                        "selects":SELECTS}
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
        # Convert sets to lists for JSON serialization
        def convert(obj):
            if isinstance(obj, set):
                return list(obj)
            if isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [convert(i) for i in obj]
            return obj
        serializable_TAGS = convert(self.TAGS)
        with open('data/'+self.Url.base_url(url)+'.json', 'w') as f:
            json.dump(serializable_TAGS, f, indent=4)


