#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import argparse
from utils import display
from includes import payloads

common_input_fields = ['name','username','uname','login','pass','passwd','password']

def readfile(inputfile):
    with open(inputfile,'r') as file:
        for url in file.readlines():
            url = url.strip()
            scanner(url)

def writefile(vuln_url,outputfile):
    with open(outputfile,'a') as file:
        file.write(vuln_url)

classic_payloads = payloads.classic_payloads

def scanner(url):
    try:
        response = requests.get(url)
        html_content = response.text
        input_field_in_url = []
        soup = BeautifulSoup(html_content,'html.parser')
        input_fields = soup.find_all('input')
        for input_field in input_fields:
            name_attribute = input_field.get('name')
            for name in common_input_fields:
                try:
                    if name in name_attribute:
                        input_field_in_url.append(name_attribute)
                        break
                except:
                    pass
        check_form = {}
        for field in input_field_in_url:
            check_form[field] = 1
        
        check_response = requests.post(url,data=check_form)
        wrong_status_code_eg = check_response.status_code
        sql_errors = ['sql','SQL','Sql','SELECT','select','sql_error']

        print(f"Checking for error based sqli in {url}...\n")
        for payload in classic_payloads:
            form = {}
            for field in input_field_in_url:
                form[field] = payload

            response = requests.post(url,data=form)
            for error in sql_errors:
                if error in response:
                    print("Vulnerable URL -->", url)
                    print("Vulnerable Parameters -->", *input_field)
                    writefile(url,outputfile="output.txt")
    except:
        print("Connection Error: Check the Network and URL.")

    

parser = argparse.ArgumentParser(add_help=False, usage=argparse.SUPPRESS)

parser.add_argument('-h','--help',nargs='?',const=True,help="Display help option.")
parser.add_argument('-u','--url',metavar='URL to scan')
parser.add_argument('-i','--input',metavar='input_file to scan',help="Pass input file name")
parser.add_argument('-o','--output',metavar='output_file to write result',help="Pass the output file name")

args = parser.parse_args()

help = args.help
url = args.url
inputfile = args.input
outputfile = args.output



def main():
    if help:
        display.help_banner()
    elif url:
        display.display_tool_name()
        scanner(url)
    elif inputfile:
        display.display_tool_name()
        readfile(inputfile)
    else:
        display.help_banner()
        
if __name__ == "__main__":
    main()