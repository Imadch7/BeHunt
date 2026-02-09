import json
import requests
from datetime import datetime
from core import url

class OWASP:
    def __init__(self):
        self.paths_list = ["/admin", "/config", "/.env", "/backup", "/.git", "/api", "/app"]
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application.json"
        }
        self.url = url.URL()
        self.insecure_paths = dict()

    def build_insecure_paths(self, code, method):
        if code == 404:
            return None
        
        if 200 <= code < 300:
            status = "Success"
        elif 300 <= code < 400:
            status = "Redirect"
        elif 400 <= code < 500:
            status = "Client Error"
        elif 500 <= code < 600:
            status = "Server Error"

        return {
            "Status": status,
            "Method": method,
            "Headers": self.headers,
            "Status Code": code,
            "Time": datetime.now().isoformat(),
            "Vulnrability Refrence": ["A01:2021 Broken Access Control"]
        }
    

    # A01:2021 Broken Access Control
    def broken_access_control(self, url):
        self.insecure_paths["URL"] = url

        with requests.Session() as session:
            for path in self.paths_list:
                full_url = url + path
                arr = []
            
                session.headers.update(self.headers)

                responses = [
                    (session.get(full_url), "GET"),
                    (session.post(full_url), "POST"),
                    (session.put(full_url), "PUT"),
                    (session.delete(full_url), "DELETE")
                ]

                for response, method in responses:
                    if response.status_code != 404:
                        arr.append(self.build_insecure_paths(response.status_code, method))

                if arr:
                    self.insecure_paths[path] = arr

        with open("insecure_paths.json", "w") as file:
            json.dump(self.insecure_paths, file, indent=4)

    
    # A02:2021 Cryptographic Failures
    def cryptographic_failures(self):
        pass

    # A03:2021 Injection
    def injection(self):
        pass

    # A04:2021 Insecure Design
    def insecure_design(self):
        pass

    # A05:2021 Security Misconfiguration
    def sm(self):
        for path, res in self.insecure_paths.items():
            if path == "URL":
                continue

            

    # A06:2021 Vulnerable and Outdated Components
    def vulnerable_and_outdated_components(self):
        pass

    # A07:2021 Identification and Authentication Failures
    def identification_and_authentication_failures(self):
        pass

    # A08:2021 Software and Data Integrity Failures
    def software_and_data_integrity_failures(self):
        pass

    # A09:2021 Security Logging and Monitoring Failures
    def Security_logging_and_monitoring_failures(self):
        pass

    # A10:2021 Server Side Request Forgery (SSRF)
    def server_side_request_forgery(self):
        pass