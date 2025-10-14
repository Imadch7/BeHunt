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
    



    def sqli_test(self,payload_file,_404=None,outformat="json",payls="email"):
        
        print("\n" + "="*70)
        print(f"[:: SQL INJECTION TEST STARTED ::]")
        print(f"Target URL: {self.url}")
        print(f"Payload File: {payload_file}")
        print("="*70)
        
        try:
            ids = self.spi.get_tag_payload(self.url,"input")
            payloads=[]
            if not os.path.exists(payload_file):
                print(f"[!] ERROR: Payload file '{payload_file}' does not exist.")
                print("="*70)
                return
            
            with open(payload_file, 'r',encoding='utf-8') as f:
                payloads = [line.strip() for line in f if line.strip()]
                payloads.append(payls)

            print(f"Total Input Tags Found: {len(ids)}")
            print(f"Total Payloads Loaded: {len(payloads)}")
            print("-" * 70)
            
            for id in ids:
                print(f"--> Testing Input Tag: '{id}'")
                for payload in payloads:
                    url_p=f"{self.url}?{id}=\"{payload}\""
                    response = self.http.send_GET_request(url_p)
                    new_status = response.status_code
                    new_text = response.text
                    text_lower = response.text.lower()

                    new_payload = {
                        "status": new_status,
                        "payload":payload,
                        "text": new_text
                    }

                    print(f"    [>] Pkg Sent | Payload: '{payload[:25]}...' | Status: {new_status}")


                    if response and response.status_code != 404:
                        self.responses["all_responses"].append(new_payload)
                        
                        is_sqli_error = False
                        error_type = "Generic SQL Error"

                        if "syntax" in text_lower or "mysql" in text_lower or "mariadb" in text_lower:
                            is_sqli_error = True
                            error_type = "MySQL/MariaDB Error"
                        
                        elif "unclosed quotation mark" in text_lower or "microsoft sql server" in text_lower or "odbc" in text_lower:
                            is_sqli_error = True
                            error_type = "MSSQL Error"

                        elif "pg_query" in text_lower or "postgresql" in text_lower or "error near" in text_lower:
                            is_sqli_error = True
                            error_type = "PostgreSQL Error"

                        elif "sql" in text_lower or "warning" in text_lower or "database" in text_lower:
                            is_sqli_error = True
                            error_type = "General DB Error"


                        if is_sqli_error:
                            print(f"{Style.DIM}{Fore.RED}    [!!!] VULNERABILITY DETECTED! (Type: {error_type}) [!!!]{Fore.RESET}")
                            print(f"    [!!!] Affected Parameter: '{id}'")
                            print(f"    [!!!] Proof-of-Concept Payload: {Fore.WHITE}{payload}{Style.DIM}")
                            print("-" * 70) 
                            self.vuln = True
                        else:
                            print("    [.] No vulnerability signature found in response.")
                            
            
            print("\n" + "="*70)
            if not self.vuln:
                print("[✓] SCAN COMPLETE: No SQL Injection vulnerabilities found.")
            else:
                print("[!!!] SCAN COMPLETE: Potential SQL Injection vulnerabilities were found. Review logs.")

        except Exception as e:
            print("\n" + "="*70)
            print(f"[X] CRITICAL ERROR OCCURRED: {e}")
            
        print("="*70 + "\n")

    def xss_test(self,payload_file,_404=None):
        try:
            ids = self.spi.get_tag_payload(self.url,"script"),self.spi.get_tag_payload(self.url,"textarea"),self.spi.get_tag_payload(self.url,"form"),self.spi.get_tag_payload(self.url,"input")
            payloads=[]
            if not os.path.exists(payload_file):
                print(f"Payload file {payload_file} does not exist.")
                return
            
            with open(payload_file, 'r',encoding='utf-8') as f:
                payloads = [line.strip() for line in f if line.strip()]
                for id in ids:
                    for payload in payloads:
                        if id!="?":
                            url_p=f"{self.url}?{id}=\"{payload}\""
                        else:
                            url_p=f"{self.url}?{payload}"
                        response = self.http.send_GET_request(url_p)
                        new_status = response.status_code
                        new_text = response.text

                        new_payload = {
                            "status": new_status,
                            "text": new_text
                        }
                        if response and response.status_code != 404:
                            self.responses["all_responses"].append(new_payload)
                            if payload in response.text:
                                print(f"{Style.DIM}{Fore.RED}[x] Potential XSS vulnerability found with payload:{Fore.WHITE} {payload}")
                                self.vuln = True
                            else:
                                print("[-] No vulnerability found with payload: ")
                if not self.vuln:
                    print("No XSS vulnerabilities found.")
        except Exception as e:
            print(f"Erro occured : {e}")
        
    def lfi_test(self,payload_file,_404=None):
        """
        Local File Inclusion test
        """
        try:
            ids = self.spi.get_tag_payload(self.url,"script"),self.spi.get_tag_payload(self.url,"textarea"),self.spi.get_tag_payload(self.url,"input")
            payloads=[]
            if not os.path.exists(payload_file):
                print(f"Payload file {payload_file} does not exist.")
                return
            
            with open(payload_file, 'r',encoding='utf-8') as f:
                payloads = [line.strip() for line in f if line.strip()]
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
                        if response and response.status_code != 404:
                            self.responses["all_responses"].append(new_payload)
                            if "root:x:0:0:root" in response.text or "[boot loader]" in response.text or "[drivers]" in response.text:
                                print(f"{Style.DIM}{Fore.RED}[x] Potential LFI vulnerability found with payload:{Fore.WHITE} {payload}")
                                self.vuln = True
                            else:
                                print("[-] No vulnerability found with payload: ")
                if not self.vuln:
                    print("No LFI vulnerabilities found.")
        except Exception as e:
            print(f"Erro occured : {e}")

    def response_out(self,outformat):

        try:
            if outformat=="json":
                with open(f"output/{self.urlm.base_url(self.url)}_response.{outformat}",'a',encoding='utf-8') as f:
                    json.dump(self.responses,f,indent=4)
            else:
                
                os.makedirs(f"output/{self.urlm.base_url(self.url)}",exist_ok=True)

                for i,res in enumerate(self.responses.get("all_responses", []), 1):
                    res_text = res.get("text","")
                    with open(f"output/{self.urlm.base_url(self.url)}/{self.urlm.base_url(self.url)}_response-{i}-.{outformat}",'a',encoding='utf-8') as f:
                        f.write(res_text)
        except Exception as e:
            print(f"Error occured {e}")


