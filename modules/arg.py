import argparse

class CLI:

    def __init__(self):
        pass


    def Arguments(self):
        parser = argparse.ArgumentParser(add_help=False,formatter_class=argparse.RawTextHelpFormatter,usage="Behunt [options]")

        parser.add_argument("-u","--url",help="Target HOST/URL",action="store")

        parser.add_argument("-h","--help",action="store_true")

        parser.add_argument("-w","--wordlist",help="payload wordlist",action="store")

        parser.add_argument("-O","--output",help="Output format:       \n 1. txt.\n 2.json.\n 3.html.)",choices=['json','html','txt'],action="store")

        parser.add_argument("-E","--Enum",help="Enumerate all the Subdomaines of the url",action="store_true")

        parser.add_argument("-T","--Tuning",help="Tuning options:       \n" \
                            "[1]. LFI ijection.\n" \
                            "[2]. SQLi(SQL injection)\n" \
                            "[3]. XSS Cross Site Scripting.\n",choices=['1','2','3'],action="store")

        return parser