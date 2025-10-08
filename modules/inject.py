from core import http
from core import spider
from core import url as Url
from colorama import Fore, Style
import os
import json


class Inject:
    def __init__(self,url):
        self.url = url
        self.http = http.HTTPRequestHandler()
        self.vuln = False
        self.spi = spider.spider()
        self.responses = {
            "all_responses": []
        }
        self.urlm = Url.URL()
    



    def sqli_test(self,payload_file,_404=None):
        ids = self.spi.get_tag_payload(self.url,"input")
        payloads=[]
        if not os.path.exists(payload_file):
            print(f"Payload file {payload_file} does not exist.")
            return
        
        with open(payload_file, 'r') as f:
            payloads = [line.strip() for line in f if line.strip()]
        
        '''with open("output/"+self.url+"response.json"):
            responses = {
                "status":,

            }'''
        
        for id in ids:
            for payload in payloads:
                url_p=f"{self.url}?{id}=\"{payload}\""
                response = self.http.send_GET_request(url_p)
                new_status = response.status_code
                new_text = response.text

                new_payload = {
                    "status": new_status,
                    "text": new_text
                }


                if response and response.status_code == 200:
                    self.responses["all_responses"].append(new_payload)
                    if "sql" in response.text.lower() or "syntax" in response.text.lower() or "mysql" in response.text.lower() or "error" in response.text.lower():
                        print(f"{Fore.RED}[x] Potential SQL Injection vulnerability found with payload:{Fore.WHITE} {payload}")
                        self.vuln = True
                    else:
                        print("[-] No vulnerability found with payload: ")
        if not self.vuln:
            print("No SQL Injection vulnerabilities found.")
    

    def xss_test(self,payload_file,_404=None):
        ids = self.spi.get_tag_payload(self.url,"select"),self.spi.get_tag_payload(self.url,"textarea"),self.spi.get_tag_payload(self.url,"form"),self.spi.get_tag_payload(self.url,"input")
        payloads=[]
        if not os.path.exists(payload_file):
            print(f"Payload file {payload_file} does not exist.")
            return
        
        with open(payload_file, 'r') as f:
            payloads = [line.strip() for line in f if line.strip()]
            for id in ids:
                for payload in payloads:
                    url_p=f"{self.url}?{id}=\"{payload}\""
                    response = self.http.send_GET_request(url_p)
                    if response and response.status_code == 200:
                        if payload in response.text:
                            print(f"{Fore.RED}[x] Potential XSS vulnerability found with payload:{Fore.WHITE} {payload}")
                            self.vuln = True
                        else:
                            print("[-] No vulnerability found with payload: ")
            if not self.vuln:
                print("No XSS vulnerabilities found.")
        
    def lfi_test(self,payload_file,_404=None):
        """
        Local File Inclusion test
        """
        ids = self.spi.get_tag_payload(self.url,"select"),self.spi.get_tag_payload(self.url,"textarea"),self.spi.get_tag_payload(self.url,"form"),self.spi.get_tag_payload(self.url,"input")
        payloads=[]
        if not os.path.exists(payload_file):
            print(f"Payload file {payload_file} does not exist.")
            return
        
        with open(payload_file, 'r') as f:
            payloads = [line.strip() for line in f if line.strip()]
            for id in ids:
                for payload in payloads:
                    url_p=f"{self.url}?{id}=\"{payload}\""
                    response = self.http.send_GET_request(url_p)
                    if response and response.status_code == 200:
                        if "root:x:0:0:root" in response.text or "[boot loader]" in response.text or "[drivers]" in response.text:
                            print(f"{Fore.RED}[x] Potential LFI vulnerability found with payload:{Fore.WHITE} {payload}")
                            self.vuln = True
                        else:
                            print("[-] No vulnerability found with payload: ")
            if not self.vuln:
                print("No LFI vulnerabilities found.")

    def response_out(self):

        try:
            with open(f"output/{self.urlm.base_url(self.url)}_response.json",'a') as f:
                json.dump(self.responses,f,indent=4)

        except Exception as e:
            print(f"Error occured {e}")


