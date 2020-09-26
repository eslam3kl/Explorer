#!/usr/bin/env python 

from termcolor import colored 
from pyfiglet import Figlet
import requests 
import optparse 
import urlparse
import re 
import os

dir_location = os.getcwd()

custom_fig = Figlet(font='avatar')
print(colored(custom_fig.renderText('Explorer'), "red", attrs=['bold']))
print(colored('Explorer - Web Crawler\nCoded by Eslam Akl - @eslam3kl\n\n ', 'cyan', attrs=['bold']))

print(colored("[+] Explorer's Mode list:", 'red', attrs=['bold']))
print(colored('{+} Discover subdomains --> 1\n{+} Discover the Hidden & Public directories --> 2\n{+} Collect the links from the source code page --> 3\n{+} Perform all Tasks on the given domain --> 4\n', 'yellow', attrs=['bold']))

#Get the target URL from the user 
def get_user_input():
	parser = optparse.OptionParser()
	parser.add_option("-u", "--url", dest="target_url", help="\tTarget URL (google.com, microsoft.com)")
	parser.add_option("-m", "--mode", dest="mode", help="\tExploration Mode (1,2,3,4)")
	(options, arguments) = parser.parse_args()
	if not options.target_url:
		print(colored('[-] Please see --help to complete the parameters', 'magenta', attrs=['bold']))
		print(colored('[+] Usage: python explorer.py -u example.com -c company_name -m mode', 'magenta', attrs=['bold']))
		print(" ")
		raise SystemExit 
	else: 
		return options.target_url, options.mode

#Send request to the target and return the status code 
def send_request(url): 	
	try: 
		request = requests.get("http://" + url, timeout=1) 
		return request
	except (requests.exceptions.InvalidURL, requests.exceptions.ConnectionError, requests.exceptions.MissingSchema, requests.exceptions.ReadTimeout):
		pass 
	except KeyboardInterrupt: 
		print(colored('\n\n[-]Happy to work with you Bro <3\n[-]Good Bye\n', 'magenta', attrs=['bold']))
		raise SystemExit

#this function is used only to send response code and content to get links function
#the differance from send_requests is timeout 
def send_request_get_content(url): 	
	try: 
		request = requests.get("http://" + url, timeout=4) 
		return request
	except (requests.exceptions.InvalidURL, requests.exceptions.ConnectionError, requests.exceptions.MissingSchema, requests.exceptions.ReadTimeout):
		pass 
	except KeyboardInterrupt: 
		print(colored('\n\n[-]Happy to work with you Bro <3\n[-]Good Bye\n', 'magenta', attrs=['bold']))
		raise SystemExit

#get the valid subdomains 
def get_subdomains(url):
	with open(dir_location + "/sub_list.txt", "r") as subdomain:
		for line in subdomain: 
			word = line.strip()
			subdomain_url = word + "." + url 
			subdomain_status_code = send_request(subdomain_url)
			if subdomain_status_code:
				print(subdomain_url + '\t\t' + colored(str(subdomain_status_code), "magenta", attrs=['bold']))
	print("\n")

#function to get the valid directories from a domain 			
def get_directories(url):
	with open(dir_location + "/dir_list.txt", "r") as directories:
		for line in directories: 
			word = line.strip()
			directory = url + "/" + word
			valid_directory = send_request(directory)
			if valid_directory:
				print(directory+ '\t\t' + colored(str(valid_directory), "magenta", attrs=['bold']))
	print("\n")
				
#function to get the links in the page source
def get_links(url, company_name):
	response_code = send_request_get_content(url)
	content = response_code.content	
	links = re.findall('(?:href=")(.*?)"', content)
	#filter the results 
	for link in links:
		link = urlparse.urljoin(url, link)
		if "#" in link: 
			link = link.split("#")[0]
		if company_name in link and link not in target_links:
			target_links.append(link)
			print(link + '\t\t' + colored(str(response_code), "magenta", attrs=['bold']))
			try:
				get_links(link, company_name)
			except AttributeError: 
				pass




#==========[ STARTING THE MAIN FUNCTION ]==========

#get the user inputs
user_input = get_user_input()
url = user_input[0]
company_name = url.split(".")[0]
mode = user_input[1]
target_links = []
end = colored('\n[+] Happy to work with you Bro <3\n', 'yellow', attrs=['bold'])


if mode == '1': 
	print(colored('[+] Start collecting target subdomins', 'red', attrs=['bold']))
	get_subdomains(url)
	print(end)
elif mode == '2':
	print(colored('[+] Start discover valid Hidden directories', 'red', attrs=['bold'])) 
	get_directories(url)
	print(end)
elif mode == '3': 
	print(colored('[+] Start collecting the links from the source code ', 'red', attrs=['bold']))
	print(colored('This links is only related to your target "' + company_name + '" and may be exist other links for third parties\n', 'green'))	
	response_code = send_request(url)
	content = response_code.content
	get_links(url, company_name)
	print(end)
elif mode == '4': 
	print(colored('[+] Start collecting target subdomins', 'red', attrs=['bold']))
	get_subdomains(url)
	print(colored('[+] Start discover valid Hidden directories', 'red', attrs=['bold'])) 
	get_directories(url)
	response_code = send_request(url)
	content = response_code.content
	print(colored('[+] Start collecting the links from the source code ', 'red', attrs=['bold']))	
	get_links(url, company_name)
	print(end)
else: 
	print(colored('[-] Select mode number to explore, see --help for more info', 'red', attrs=['bold']))

