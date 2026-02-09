import json
import requests
from datetime import datetime

class OWASP:
    def __init__(self):
        self.paths_list = ["/admin", "/config", "/.env", "/backup", "/.git", "/api", "/app"]
        self.vulnerability_headers = ["Server", "X-Powered-By", "X-Debug-Token", "X-Runtime", "Access-Control-Allow-Origin"]
        self.armor_headers = ["X-Frame-Options", "Content-Security-Policy", "Strict-Transport-Security", "X-Content-Type-Options"]
        self.insecure_paths = dict()

    def get_vulnerability_refrence(self, num):
        match num:
            case 1:
                return "A01:2021 Broken Access Control"
            case 2:
                return "A02:2021 Cryptographic Failures"
            case 3:
                return "A03:2021 Injection"
            case 4:
                return "A04:2021 Insecure Design"
            case 5:
                return "A05:2021 Security Misconfiguration"
            case 6:
                return "A06:2021 Vulnerable and Outdated Components"
            case 7:
                return "A07:2021 Identification and Authentication Failures"
            case 8:
                return "A08:2021 Software and Data Integrity Failures"
            case 9:
                return "A09:2021 Security Logging and Monitoring Failures"
            case 10:
                return "A10:2021 Server Side Request Forgery"

    def build_insecure_paths(self, code, method, headers):
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
            "Headers": headers,
            "Status Code": code,
            "Time": datetime.now().isoformat(),
            "Vulnerability Refrence": []
        }
    
    def make_http_request(self, url):
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
                        arr.append(self.build_insecure_paths(response.status_code, method, response.headers))

                if arr:
                    self.insecure_paths[path] = arr
    

    # A01:2021 Broken Access Control
    def broken_access_control(self):
        for path, responses in self.insecure_paths.items():
            if path == "URL":
                continue

            for response in responses:
                response["Vulnerability Refrence"].append(self.get_vulnerability_refrence(1))

        with open("a01.json", "w") as file:
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
    def security_misconfiguration(self):
        for path, responses in self.insecure_paths.items():
            if path == "URL":
                continue

            for response in responses:
                added = False
                for armor in self.armor_headers:
                    if armor not in response.headers:
                        if not added:
                            response["Vulnerability Refrence"].append(self.get_vulnerability_refrence(5))
                            added = True

                for vul in self.vulnerability_headers:
                    if vul in response.headers:
                        if not added:
                            response["Vulnerability Refrence"].append(self.get_vulnerability_refrence(5))
                            added = True


        with open("a05.json", "w") as file:
            json.dump(self.insecure_paths, file, indent=4)

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
    def security_logging_and_monitoring_failures(self):
        pass

    # A10:2021 Server Side Request Forgery
    def server_side_request_forgery(self):
        pass