import subprocess
from core import url
import os

class Url_ENUM:
    def __init__(self,URLM):
        self.purl = url.URL()
        self.URLM = URLM
        try:
            pro = subprocess.run(["docker","-v"],
                capture_output=True,
                text=True,
                check=False
            )

            if "Docker version" in pro.stdout:
                print("Docker is already installed")
            elif pro.returncode != 0:
                print("Docker is not installed")
                print("installation... ")
                try:
                    getDocker = subprocess.run(["docker","-v"],
                        capture_output=True,
                        text=True,
                        check=False
                    )
                    if getDocker.returncode != 0:
                        print("Verify your connection, Docker is not installed")
                        exit(0)
                    
                    print(getDocker.stdout.strip())
                except Exception as p:
                    print(f"Maybe Connection Error : {p}")
                    exit(0)

        except Exception as e:
            print(f"Error occured : {e}")
            exit(0)


        self.COMMAND1 = "sudo docker build -t hakluke/hakrawler ."
        self.COMMAND2 = f"echo {URLM} | "
        self.COMMAND3 = f"sudo docker run --rm -i hakluke/hakrawler >> {self.purl.base_url(URLM)}.txt "
        try:
            os.chdir("subdomain")
        except Exception as e:
            print("that file doesn't exist")
            exit(1)
    
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
