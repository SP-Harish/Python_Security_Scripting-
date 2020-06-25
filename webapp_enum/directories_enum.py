#!/usr/bin/env python

import requests                 #library used to send get and post requests.


def request(target_url):
    try:
      return requests.get("http://"+ target_url)
    except requests.exceptions.ConnectionError:
       pass

target_url = "10.1.1.126/mutillidae/"
            #enter the target url.



with open("/root/Downloads/directory_wordlists.txt", "r") as wordlist_file:         #opening the wordlist file that contains all the words that needs to be tested.(dictionary)
    for line in wordlist_file:                  #iterating over each line in the file. each line contains one word.
        word= line.strip()                      #as wordlist has new line character at end of each word; we need to remove that. strip() function is used to do it,
        test_url = target_url +"/"+word         #appending the word to the url.
        response = request(test_url)
        if response:
             print("[+] Discovered url -->" +test_url)
