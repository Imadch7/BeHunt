from core import http
from core import spider
from core import url as Url
from colorama import Fore, Style
import os
import json
import time
import datetime
import random
import sys


class Inject:
    def __init__(self,url):
        self.url = url
        self.http = http.HTTPRequestHandler()
        self.vuln = False
        self.spi = spider.spider()
        self.ids = self.spi.get_tag_payload(self.url,"input")
        self.ids.extend(self.spi.get_tag_payload(self.url,"textarea"))
        self.payloads = []
        self.responses = {
            "all_responses": []
        }
        self.metadata = {
            "metadata": {}
        }
        self.JSON_OUTPUT = {
            **self.metadata,
            **self.responses
        }
        self.urlm = Url.URL()
    

    def response_out(self,outformat,method):
        if method=='1':
            methode="SQL Injection"
        elif method=='2':
            methode="XSS Injection"
        elif method=='3':
            methode="LFI Injection"
        else:
            methode="Unknown"
        try:
            if outformat=="json":
                filename = f"output/{methode}-Result-{self.urlm.base_url(self.url)}_response.{outformat}"
                with open(filename,'a',encoding='utf-8') as f:
                    json.dump(self.JSON_OUTPUT,f,indent=4)
            else:
                
                os.makedirs(f"output/{self.urlm.base_url(self.url)}",exist_ok=True)

                for i,res in enumerate(self.responses.get("all_responses", []), 1):
                    res_text = res.get("text","")
                    with open(f"output/{self.urlm.base_url(self.url)}/{self.urlm.base_url(self.url)}_response-{i}-.{outformat}",'a',encoding='utf-8') as f:
                        f.write(res_text)
        except Exception as e:
            print(f"Error occured {e}")
        
    
    def GET_PAYLOADS(self,payload_file):
        if not os.path.exists(payload_file):
            print(f"[!] ERROR: Payload file '{payload_file}' does not exist.")
            print("="*70)
            return
        
        with open(payload_file, 'r',encoding='utf-8') as f:
            self.payloads = [line.strip() for line in f if line.strip()]

    def SQLI(self,payload,id):
        try:
            for id in self.ids:
                url_p=f"{self.url}?{id}=\"{payload}\""
                response = self.http.send_GET_request(url_p)
                new_status = response.status_code
                new_data = {
                    "test_id":id,
                    "test_type": "SQL Injection",
                    "payload_type":"Boolean",
                    "status": new_status,
                    "target_url":url_p,
                    "response_time_ms": response.elapsed.total_seconds() * 1000,
                    "response_size_bytes": len(response.content),
                    "headers": dict(response.headers),
                    "vulnerability_indicators": {
                        "sql_errors": True,
                        "unusual_response_size": False,
                        "response_time_anomaly": False
                    },
                    "severity": "confirmed",
                    "confirmed": True,
                    "notes": "Requires manual verification"
                }

                if response.status_code == 200:
                    self.responses["all_responses"].append(new_data)
                else:
                    continue
        except Exception as e:
            print(f"Error in SQLI method: {e}")
    
    def XSS(self,payload,id):
        for id in self.ids:
            url_p=f"{self.url}?{id}=\"{payload}\""
            response = self.http.send_GET_request(url_p)
            new_status = response.status_code
            new_data = {
                "test_id":id,
                "test_type": "XSS Injection",
                "payload_type":"JavaScript code",
                "status": new_status,
                "target_url":url_p,
                "response_time_ms": response.elapsed.total_seconds() * 1000,
                "response_size_bytes": len(response.content),
                "headers": dict(response.headers),
                "vulnerability_indicators": {
                    "xss_reflection": True,
                    "unusual_response_size": False,
                    "response_time_anomaly": False
                },
                "severity": "confirmed",
                "confirmed": True,
                "notes": "Requires manual verification"
            }
            if response.status_code == 200:
                self.responses["all_responses"].append(new_data)
            else:
                continue

    def LFI(self,payload,id):
        for id in self.ids:
            url_p=f"{self.url}?{id}=\"{payload}\""
            response = self.http.send_GET_request(url_p)
            new_status = response.status_code
            new_data = {
                "test_id":id,
                "test_type": "LFI Injection",
                "payload_type":"path traversal",
                "status": new_status,
                "target_url":url_p,
                "response_time_ms": response.elapsed.total_seconds() * 1000,
                "response_size_bytes": len(response.content),
                "headers": dict(response.headers),
                "vulnerability_indicators": {
                    "lfi_indicators": True,
                    "unusual_response_size": False,
                    "response_time_anomaly": False
                },
                "severity": "confirmed",
                "confirmed": True,
                "notes": "Requires manual verification"
            }
            if response.status_code == 200:
                self.responses["all_responses"].append(new_data)
            else:
                continue


    def TEST(self,PAYLOAD_FILE,methode):
        print("[*] Starting Payload Injection Test...")
        try:
            sc_id = str(random.randint(1000000, 9999999))
            scan_date = datetime.datetime.now().isoformat()
            self.metadata["metadata"] = {
                "scan_id": sc_id,
                "target_domain": self.urlm.base_url(self.url),
                "scan_date": scan_date,
                "scanner_version": "1.0",
                "authorization": "Authorized Test"
            }
            # Update JSON_OUTPUT with populated metadata
            self.JSON_OUTPUT = {
                **self.metadata,
                **self.responses
            }
            self.GET_PAYLOADS(PAYLOAD_FILE)
            i=1
            total = len(self.payloads)
            if methode=="1":
                for payload in self.payloads:
                    self.SQLI(payload, i)
                    print(f"Processing payload{i/total*100}%: {payload}",end='\r')
                    i+=1
                    sys.stdout.flush()
            elif methode=="2":
                for payload in self.payloads:
                    self.XSS(payload,i)
                    print(f"Processing payload{i/total*100}%: {payload}",end='\r')
                    i+=1
                    sys.stdout.flush()
            elif methode=="3":
                for payload in self.payloads:
                    self.LFI(payload,i)
                    print(f"Processing payload{i/total*100}%:",end='\r')
                    i+=1
                    sys.stdout.flush()
            else:
                print("[*] Invalid Tuning Level")

        except AttributeError as e:
            print(f"AttributeError during TEST: {e}")
        except Exception as e:
            print(f"Error occured during TEST: {e}")
        finally:
            print("\n\n[*] Test Completed. Check output files for results.")

    
'''
import time # Juste pour la démo, simule le travail
from tqdm import tqdm

# Assurez-vous d'avoir initialisé self.payloads quelque part
# Exemple : self.payloads = ["payload1", "payload2", "payload3", "payload4", "payload5"]

# Vous pouvez retirer l'initialisation de 'i' si vous utilisez enumerate
# i = 0  <-- PLUS NÉCESSAIRE SI VOUS UTILISEZ ENUMERATE

print("Démarrage du test d'injection de charge utile...")

# Utilisez tqdm pour envelopper l'énumération de self.payloads
# tqdm : Affiche la barre et le pourcentage
# enumerate : Fournit l'index (i) et l'élément (payload)
for i, payload in tqdm(enumerate(self.payloads), total=len(self.payloads), desc="Progression de l'attaque", unit="payload"):
    
    # Simuler votre fonction (LFI = Local File Inclusion ?)
    # self.LFI(payload, i) 
    
    # Simuler le travail
    time.sleep(0.05) 
    
    # i += 1  <-- PLUS NÉCESSAIRE car enumerate le fait
    
print("\nTest terminé ! Rapport de progression complet. ✅")
'''




