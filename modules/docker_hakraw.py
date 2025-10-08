import subprocess
from core import url
import os

class Url_ENUM:
    def __init__(self,URLM):
        self.purl = url.URL()
        self.URLM = URLM
        self.COMMAND1 = "sudo docker build -t hakluke/hakrawler ."
        self.COMMAND2 = f"echo {URLM} | "
        self.COMMAND3 = f"sudo docker run --rm -i hakluke/hakrawler >> {self.purl.base_url(URLM)}.txt "
        os.chdir("HR")
    
    def run(self):
        try:
    
            process = subprocess.Popen(self.COMMAND1,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.wait()
    
            process2 = subprocess.Popen(self.COMMAND2+self.COMMAND3,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process2.wait()
            stdout, stderr = process2.communicate()
            if process2.returncode == 0:
                if os.path.exists("../data") == False:
                    os.mkdir("../data")
                proces= subprocess.Popen(f'mv {self.purl.base_url(self.URLM)}.txt ../data', shell=True)
                proces.wait()
                print(f"Output file {self.purl.base_url(self.URLM)}.txt moved to ./data directory")
            else:
                print("Error occurred while running hakrawler:")
                print(stderr.decode())
        except Exception as e:
            print(f"An error occurred: {e}")
