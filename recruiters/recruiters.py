#!/usr/bin/python
import ConfigParser
import MySQLdb
import sys
import fileinput
import os
#import weneeds
#import composeMessage
#import persons
import datetime
from datetime import date, timedelta
from shutil import copyfile



##############################################################
#
##############################################################


#CONFIG_FILE = '/tools/tool/config.ini'
CONFIG_FILE = '/home/linuxjobber/tools/config.ini'
parser = ConfigParser.SafeConfigParser()
parser.read( CONFIG_FILE)

def main():
    db_conn = get_db_object( parser)
    if len(sys.argv)  == 1:
        print( "add action as argument: addrecruiter, showrecruiter, updaterecruiter, checkstatus etc")
        exit()

    elif sys.argv[1] == "addrecruiter":        
        full_name = raw_input("Enter recruiters full name: ")
        phone = raw_input("Enter recruiters phone number: ")
        email = raw_input("Enter recruiters email address: ")
 
        insert_recruiter( db_conn, full_name, phone, email)

        print("Name: %s, phone: %s, email: %s") % ( full_name, phone, email)


###################### Business Logic #######################

def insert_recruiter( conn, fullname, phone, email):
    cursor = conn.cursor() 

    qry = """ INSERT INTO recruiters( full_name, phone, email) VALUES(%s,%s,%s)"""

    cursor.execute(( qry) , ( fullname, 
                              phone,
                              email
                             ))
    result = cursor.fetchall()
    for x in result:
        print(x)
    conn.commit()
#    conn.close()

###################### Database Section #######################

def get_db_object( parser):
    connection = MySQLdb.connect (host=parser.get('linuxjobber','host'),user=parser.get('linuxjobber','user'),passwd=parser.get('linuxjobber','passwd'),db=parser.get('linuxjobber','db'))
    return connection

if __name__ == "__main__":
    main()

