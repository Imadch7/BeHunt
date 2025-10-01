import requests
import file

class HTTPRequestHandler:
    
    def __init__(self):
        pass

    def send_GET_request(self, url, headers=None, params=None):
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"GET request failed: {e}")
            return None

    def send_POST_request(self, url, headers=None, data=None):
        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"POST request failed: {e}")
            return None
    
    def send_PUT_request(self, url, headers=None, data=None):
        try:
            response = requests.put(url, headers=headers, data=data)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"PUT request failed: {e}")
            return None
    def send_DELETE_request(self, url, headers=None):
        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"DELETE request failed: {e}")
            return None
    
    def send_HEAD_request(self, url, headers=None):
        try:
            response = requests.head(url, headers=headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"HEAD request failed: {e}")
            return None
    
    def multiple_subdomain_requests(self, base_url, file, method="GET", headers=None):
        try:
            with open(file, 'r') as fs:
                subdomains = fs.readlines()
                responses = {}
                for subdomain in subdomains:
                    subdomain = subdomain.strip()
                    full_url = f"{base_url}/{subdomain}"
                    if method.upper() == "GET":
                        response = self.send_GET_request(full_url, headers=headers)
                    elif method.upper() == "POST":
                        response = self.send_POST_request(full_url, headers=headers)
                    elif method.upper() == "PUT":
                        response = self.send_PUT_request(full_url, headers=headers)
                    elif method.upper() == "DELETE":
                        response = self.send_DELETE_request(full_url, headers=headers)
                    elif method.upper() == "HEAD":
                        response = self.send_HEAD_request(full_url, headers=headers)
                    else:
                        print(f"Unsupported HTTP method: {method}")
                        exit(1)
                    
                    if response:
                        responses[full_url] = response
                
                return responses
        except FileNotFoundError:
            print(f"File not found: {file}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None