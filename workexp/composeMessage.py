import ConfigParser
import MySQLdb
import sys
import fileinput
import os
from datetime import date, timedelta
from shutil import copyfile

#CONFIG_FILE = '/tools/tool/config.ini'
CONFIG_FILE = '/home/linuxjobber/tools/config.ini'

parser = ConfigParser.SafeConfigParser()
parser.read( CONFIG_FILE)

class compose:

    def __init__(self, messageType):
        
        if messageType == 'income_verification':
            self.msg_file = 'income_verification'
            connection = MySQLdb.connect (host=parser.get('linuxjobber','HOST'),user=parser.get('linuxjobber','USER'),passwd=parser.get('linuxjobber','PASSWD'),db=parser.get('linuxjobber','DB'))
            b= str(""" select title, message, slug from home_message WHERE slug = '%s'""" % (self.msg_file,))
            cursor = connection.cursor ()
            cursor.execute(b)

            #fetch the message
            results = cursor.fetchall ()

            for row in results:
                self.Title = row[0]
                self.message = row[1]

            self.Title = self.Title.replace(" ","_")
            self.message = self.message.replace("<br />","_")

        elif messageType == 'graduation_reminder':
            self.msg_file = 'graduation_reminder'
            connection = MySQLdb.connect (host=parser.get('linuxjobber','HOST'),user=parser.get('linuxjobber','USER'),passwd=parser.get('linuxjobber','PASSWD'),db=parser.get('linuxjobber','DB'))
            b= str(""" select title, message, slug from home_message WHERE slug = '%s'""" % (self.msg_file,))
            cursor = connection.cursor ()
            cursor.execute(b)

            #fetch the message
            results = cursor.fetchall ()

            for row in results:
                self.Title = row[0]
                self.message = row[1]

            self.Title = self.Title.replace(" ","_")
            self.message = self.message.replace("<br />","_")

    def sendMessageGrad(self, email, first_name, date):
        mes = '1'
        date =  str(date.date())
        if date == None:
            pass
        else:
            os.system('python wemailer.py %s %s %s %s %s %s' % ( email, first_name, date, self.Title, self.message, mes))
            return "...message sent"

    def sendMessage( self, email, first_name, date):
        mes = '2'
        #self.setMsgFile( 'wemailer.py', self.msg_file,'MSGS_FILE')
        #os.system('python wemailer.py %s %s %s' % ( 'showpopulous@gmail.com', first_name, date))
        #print("emailing: "+email+" "+first_name+" "+str(date))
        #os.system('python wemailer.py %s %s %s %s %s %s' % ( email, first_name, date, self.Title, self.message, mes))
        os.system('python wemailer.py %s %s %s %s %s %s' % ( email, first_name, self.Title, self.message, mes, date))
        #self.setMsgFile( 'wemailer.py', 'MSGS_FILE',self.msg_file)
        return "...message sent"

    def setMsgFile( self, fileToEdit, msgFile, temp):
        for line in fileinput.input( fileToEdit, inplace=True):
            #remove all extra characters including new line
            line= line.rstrip().replace(temp, msgFile)
            #add new line
            print line
