import sys
from core import arg
from core import spider
from modules import docker_hakraw
from modules import inject

'''
try --> 

    python3 __init__.py -u https://elmouchir.caci.dz/login -w payloads/jstnkndy.txt

'''

if __name__ == "__main__":
	print("Welcome to Behunt")
	try:
		arg_obj = arg.CLI()
		parser = arg_obj.Arguments()
		if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
			print("Options:")
			print(parser.format_help())
			sys.exit(0)

		args = parser.parse_args()
		print(args.url)

		#spi = docker_hakraw.Url_ENUM(args.url)
		#spi.run()
		
		inj = inject.Inject(args.url)
		if(args.wordlist):
			inj.sqli_test(args.wordlist)
			inj.response_out()
	except IndexError:
		print("No arguments provided. Use -h or --help for usage information.")
		sys.exit(1)
	except Exception as e:
		print(f"An error occurred: {e}")
		sys.exit(1)
		
