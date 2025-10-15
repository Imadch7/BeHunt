import sys
import os
from pathlib import Path
import getpass
from core import url
from core import spider
from core import find_dir
from modules import arg
from modules import docker_hakraw
from modules import inject
from modules import logo

'''
try --> 

    python3 __init__.py -u url-T 2 -w payloads/jstnkndy.txt -O html
'''

class Behunt:

	def __init__(self):
		self.Url = url.URL()
		self.Arg = arg.CLI()
		tar_path = find_dir.Find_Dir.get_PATH()
		os.chdir(tar_path)


if __name__ == "__main__":

	logo.LOGO("                  BeHunt                   ").draw_LG()
	BH = Behunt()
	print("Welcome to Behunt")
	try:
		parser = BH.Arg.Arguments()
		args = parser.parse_args()

		if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
			print("Options:")
			print(parser.format_help())
			sys.exit(0)
		
		#Beginning Attack Process
		url_str = args.url
		if url_str :
			print(url_str)
			inj= inject.Inject(url_str)

			if args.Enum == True:
				enum = docker_hakraw.Url_ENUM(url_str)
				enum.run()
				print("The Result of Enumeration is in data file\n")
			elif args.wordlist:

				if args.Tuning == '1':
					inj.lfi_test(args.wordlist)
					if not args.output:
						Form=input("[*] Enter The Format (json,txt,html) : ")
						inj.response_out(Form)
					else:
						inj.response_out(args.output)
					
				elif args.Tuning == '2':
					print("hello world")
					inj.sqli_test(args.wordlist)
					if not args.output:
						Form=input("[*] Enter The Format (json,txt,html) : ")
						inj.response_out(Form)
					else:
						inj.response_out(args.output)
					
				elif args.Tuning == '3':
					inj.xss_test(args.wordlist)
					if not args.output:
						Form=input("[*] Enter The Format (json,txt,csv) : ")
						inj.response_out(Form)
					else:
						inj.response_out(args.output)
			else:
				print("[*] Add a wordlist")
		else:
			print("Try Behunt -h")

	except IndexError:
		print("No arguments provided. Use -h or --help for usage information.")
		sys.exit(1)
	except Exception as e:
		print(f"An error occurred: {e}")
		inj.response_out(args.output)
		sys.exit(1)
	finally:
		print(f"Welcome another Time {getpass.getuser()}")
