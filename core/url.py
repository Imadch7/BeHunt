

class URL:

    def __init__(self):
        pass


    def normalize_url(self,url):
        if '?' in url:
            return url.split('?')[0]
        return url
    
    def base_url(self,url):
        if '//' in url:
            return url.split('//')[1].split('/')[0]
        return url.split('/')[0]
    
    def valid_url(self,url):
        if url.startswith('http://') or url.startswith('https://'):
            return True
        return False