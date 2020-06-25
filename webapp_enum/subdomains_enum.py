#!/usr/bin/env python

import requests


def request(target_url):
    try:
      return requests.get("http://" + target_url)
    except requests.exceptions.ConnectionError:
      pass
target_url = "google.com"
            #input the target website

with open("/root/Downloads/subdomain_wordlists.txt", "r") as wordlist_file:
    for line in wordlist_file:                  #iterating over each line in the file
        word= line.strip()                      #as wordlist has new line character at end of each word; we need to remove that. strip() function is used to do it,
        test_url = word + "." + target_url
        response = request(test_url)
        if response:
             print("[+] Discovered subdomain -->" +test_url)

