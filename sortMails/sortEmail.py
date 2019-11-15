#!/usr/bin/python

import ConfigParser
import ast
import sys
import os, shutil
from email.parser import Parser


############################################################
#
# sortEmail.py
#
# call like this:
# sortEmail.py rawEmailFile
# this file  takes one parameter: 1. file containing raw email
#
# This file will look through the raw mail specified in the rawEmailFile and then
#  iterate through a list of staff. if the staff is mentioned in the 
#  email, it will send a copy of the email to the inbox of the staff.
#  After all mentioned staff have been copied, it will delete the mail.
#
#############################################################

#
# edit this: set location where you wish to put the configuration file
#
CONFIG_FILE = '/home/linuxjobber/tools/config.ini'

################## Do not edit below this line  #######################

def stripSymbols( email):
    email = email.replace ("<","")
    email = email.replace (">","")
    return email

parser = ConfigParser.SafeConfigParser()
parser.read( CONFIG_FILE)

staffs = ast.literal_eval( parser.get('sortMails','staffs'))
known_users = ast.literal_eval( parser.get('sortMails','known_users'))
all_mails_folder = parser.get('sortMails','all_mails_folder')

rawEmailFile = sys.argv[1]
with open( rawEmailFile, 'r') as file:
    strEmail = file.read()

parser = Parser()

if len(sys.argv)  == 1:
    print( "you must call this script like this: sortEmail.py raw.email.file")
    exit()
else:
    emailMsg = parser.parsestr(strEmail)
    #begin sorting
    print( " ............................................")
    print( "This email was sent from: %s") % ( stripSymbols( emailMsg['From'],))
    print( "This email was sent to: %s") % ( stripSymbols( emailMsg['To'],))
    for staff in staffs:
        print(" ====================================================")
        print( "Scanning email for staff: %s") % (staff,)
        if staff not in known_users:
            print("%s is not a known staff in this environment") % (staff,)
        else:
            if staff.upper().lower() in emailMsg['To'].upper().lower():
            #if staff.upper().lower() == emailMsg['To'].upper().lower():
                print("sending copy of mail for %s to: %s") % (staff, known_users[staff]+'new')
                shutil.move( all_mails_folder + rawEmailFile, known_users[staff]+'new')
            else:
                print("This staff is not copied on this email")

    #finish sorting

    #if you are done sorting and the rawEmailFile still exist, then put it in default mail box
    shutil.move( all_mails_folder + rawEmailFile, '/home/sshowunmi/.local/share/evolution/mail/local/' +'new')
