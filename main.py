#import libraries
from enum import unique
import sys,re,colors
import requests as r
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import argparse
import matplotlib.pyplot as plt
import funs
my_parser = argparse.ArgumentParser(description='find js files in urls')
unique_js_files = []

# Add the arguments
my_parser.add_argument('-u',
                       metavar='url',
                       type=str,
                       help='target url')
my_parser.add_argument('-f',
                       metavar='file',
                       type=str,
                       help='target file')
my_parser.add_argument('-c', dest='c', action='store_true',help="print comments")
my_parser.add_argument('-a', dest='a', action='store_true',help="include jquery and CDN etc...")
my_parser.add_argument('-usernames', dest='usernames', action='store_true',help="find usernames")
my_parser.add_argument('-passwords', dest='passwords', action='store_true',help="find passwords")
args = my_parser.parse_args()
url = args.u
#Find comments



def main(url):
    print(colors.color.purple(f"scan: {url}"))
    colors.color.reset()
    session = r.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    html = session.get(url).content
    soup = bs(html, "html.parser")
    script_files = []
    for script in soup.find_all("script"):
        if script.attrs.get("src"):
            script_url = urljoin(url, script.attrs.get("src"))
            script_files.append(script_url)
    urls = []
    for js_file in script_files:
        urls.append(js_file)
    print(colors.color.blue("javascript files url:"))
    colors.color.reset()
    found_urls = []
    found_words = []
    usernames = []
    passwords = []
    for url in urls:
        req = r.get(url).text
        if(args.usernames):
            usernames +=re.findall("username.{10}",req)
        if(args.passwords):
            passwords += re.findall('password.{10}',req)
        found_urls += re.findall("(http://|https://)([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?",req)
        found_words += re.findall("(\/\/.*\n|\/\*.*\n\*\/)",req)
        if(not args.a):
            if("//cdn." not in url and "bootstrap" not in url  and "jquery" not in url): 
                print(url)
        else:
            print(url)
    print(colors.color.red("found this urls"))
    colors.color.reset()
    funs.find_urls(found_urls)
    if(args.c):
        funs.find_comment(found_words)
    if(args.usernames):
        print(colors.color.yellow("found usernames"))
        colors.color.reset()
        funs.usernames(usernames)
    if(args.passwords):
        print(colors.color.yellow("found passwords"))
        colors.color.reset()
        funs.passwords(passwords)
# if user include file
if(args.f):
    file = open(args.f,'r')
    for line in file:
        main(line.strip('\n')) 
else:
    main(args.u)
