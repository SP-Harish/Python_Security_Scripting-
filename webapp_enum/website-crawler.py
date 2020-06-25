#!/usr/bin/env python

import requests
import re
import urlparse                                 #to find all the relative url and join with the absolute URL.
    # def request(target_url):
#     try:
#       return requests.get("http://"+ target_url)
#
#     except requests.exceptions.ConnectionError:
#        pass

target_url = "http://10.1.1.126/mutillidae/"
                #"enter the target url"
target_links = []                                  #list that will be used to store links
def extract_links(target_url):
    response = requests.get(target_url)                                 #storing website response inthe variable.
    return re.findall('(?:href=")(.*?)"', response.content)             #searching in the html content of the page using,response.content.
                                                                        #regex function - findall is used to catch all the the content that matches the regex in the given characters.
                                                                        #.*? it should match everything till the first "

def crawl(target_url):
    href_links= extract_links(target_url)
    for link in href_links:                                                 #to print each link individually in the line.
        link = urlparse.urljoin(target_url, link)                           #it joins the relative url link with the targeturl. thus, making it a full URL
        if "#" in link:                                                     #navigating within the page is done using the #hash link. we dont want the hash component and just want the link.
            link= link.split("#")[0]                                           #splitting the link based on the # and extracting the 1st component from the link.
        if target_url in link and link not in target_links:         #avoiding any repeating link       #filtering all the other links like facebook, twitter etc that are present within the target_url page.
            target_links.append(link)                               #adding links to the list.
            print(link)
            crawl(link)                                             #recursion to crawl all over the page
crawl(target_url)
# print(response.content)             #used to print the html content of the request page that is present in the response variable.