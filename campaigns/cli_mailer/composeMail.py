#!/usr/bin/python
import ConfigParser
import MySQLdb
import sys
import fileinput
import os
from datetime import date, timedelta
from shutil import copyfile


##############################################################
# 
# if called as: python ./pymail.py 1 all_role6 msgFileName
# This program is only going to pull email and first name from db and send message in msgFileName to all emails returned from db
# then call emailer program thus: python ./emailser.py joseph.showunmi@linuxjobber.com joseph
#   For testing, use python ./pymail.py 1 test msgFileName
#   For yesterdays registrants use ./python 1 yesterdays yesterdays
#
# if called as: python ./pymail.py 1 unfit4job 7 (where 7 is classcode)
# This program will find all applicants who are unfit for jobs 
# and populate table:matchjobs
##############################################################


CONFIG_FILE = '/home/linuxjobber/tools/config.ini'
parser = ConfigParser.SafeConfigParser()
parser.read( CONFIG_FILE)


if len(sys.argv)  == 1:
    print( "Enter a numeric argument")
    exit()
elif sys.argv[1] == "show":
    print( "1 -> linuxjobber","2 -> noobaid")
    print( "1 a -> get lj trainings","2 b -> get nb users","2 c -> expert searches")
    exit()

##################################################################################
def setMsgFile(fileToEdit, msgFile, temp):
    for line in fileinput.input( fileToEdit, inplace=True):
        #remove all extra characters including new line
        line= line.rstrip().replace(temp, msgFile)
        #add new line
        print line

#whatever the second argument is, let emailer use it as message file. In the event emailer MSGS_FILE screws up, default is below
#from MSGS_FILE import MSG
#from MSGS_FILE import TITLE
#if sys.argv[2] == "test":
setMsgFile( 'emailer.py', 'messages.'+sys.argv[3],'MSGS_FILE')
#else:
#    setMsgFile( 'messages.'+sys.argv[2],'MSGS_FILE')

#if you wish to add extra message to mail, after msg, store it in extra_msg string
extra_msg_desc=" "

if sys.argv[1] == "1":
    # send email to all role 6 (only 2 arguments)
    if sys.argv[2] == "all_role6":
        today = date.today()
        #a = str("call getYesterdaysRegistrants('2018-02-01','2018-02-11')")
        #a = str("call getYesterdaysRegistrants('2017-06-24','2017-09-08')")
        a = str("call getYesterdaysRegistrants('2016-11-01', '%s')" % (today,))

    if sys.argv[2] == "all_role4":
        today = date.today()
        a = str("select distinct(email),full_name,username from users where role=4 AND email NOT IN (SELECT * FROM do_not_send) GROUP BY email;")

    if sys.argv[2] == "job_applicants":
        a = str("select distinct(email),fname,lname,email from jobs where email<>'' AND email NOT IN (SELECT * FROM do_not_send) GROUP BY email;")

    if sys.argv[2] == "group_class_payment_reminder":
        a = str("select distinct(email),full_name,email,user_id,is_paid,transaction_id from group_course_registers where courseId=14 and transaction_id IS NULL AND email NOT IN (SELECT * FROM do_not_send) GROUP by email;")

    if sys.argv[2] == "internship_needed":
        a = str("select email,fname,lname,classcode,created from jobs AND email NOT IN (SELECT * FROM do_not_send)")

    if sys.argv[2] == "nigerian_internship":
        a = str("select email,full_name,course_title from internships where email NOT IN (SELECT emails FROM do_not_send) ")
        #a = str("select email,full_name,course_title from internships where email NOT IN (SELECT * FROM do_not_send) group by email ")

    if sys.argv[2] == "switch_career":
        a = str("select email, fullname as full_name, old_career, new_career_id, application_date from home_careerswitchapplication where email NOT IN (SELECT email FROM home_unsubscriber) ")

    if sys.argv[2] == "yesterdays_switch_career":
        a = str("select email, fullname as full_name, old_career, new_career_id, application_date from home_careerswitchapplication where email NOT IN (SELECT email FROM home_unsubscriber) AND application_date >= DATE_SUB(NOW(), INTERVAL 45 HOUR) ")

    if sys.argv[2] == "all_full_time_job_applicants":
        a = str("select email, fullname as full_name, phone, position_id, interest, application_date from home_job where email NOT IN (SELECT email FROM home_unsubscriber) ")

    if sys.argv[2] == "interested_full_time_job_applicants":
        a = str("select email, fullname as full_name, phone, position_id, interest, application_date from home_job where email NOT IN (SELECT email FROM home_unsubscriber) and interest='interested' ")

    if sys.argv[2] == "yesterdays_interested_job_applicants":
        a = str("select email, fullname as full_name, phone, position_id, interest, application_date from home_job where email NOT IN (SELECT email FROM home_unsubscriber) and interest='interested' AND application_date >= DATE_SUB(NOW(), INTERVAL 45 HOUR) ")

    if sys.argv[2] == "marketing_internship":
        a = str("select email,full_name,course_title from internships where email NOT IN (SELECT * FROM do_not_send) group by email ")

    if sys.argv[2] == "congratVideoFinishers":
        # you can enter a date in the argument if you want to send congratulations message to video finisher for that specific date
        #a = str("call getVideoFinishers('2017-09-02')")
        # if a date is not supplied, getVideoFinishers will send congratulations message to all yesterdays finishers
        a = str("call getVideoFinishers(NULL)")
        extra_msg_desc = "-- Video modules completed --"

    if sys.argv[2] == "congratQuizPassers":
        a = str("call getQuizPassers(NULL)")
        extra_msg_desc = "-- Quiz Completed --"

    if sys.argv[2] == "yesterdays":
        yesterday = date.today() - timedelta(1)
        a = str("SELECT DISTINCT(u.email),u.full_name,u.username,u.id,u.role,u.created,pg.user_id,pg.page  FROM users as u left join page_logs as pg on u.id=pg.user_id where u.created > '%s' and u.role=6" % (yesterday,))

    if sys.argv[2] == "likelyToSubscribe":
        a = str("call getLikelyToSubscribe(NULL)")

    # send email for testing (only 2 arguments, second argument must be 'test')
    if sys.argv[2] == "test":
        setMsgFile( 'emailer.py','messages.'+sys.argv[3],'MSGS_FILE')
        #TEST_EMAIL='noobaidmail@gmail.com'
        TEST_EMAIL='showpopulous@gmail.com'
        TESTER='noob'
        if sys.argv[3] == "yesterdays":
            yesterday = date.today() - timedelta(1)
            a = str("SELECT DISTINCT(u.email),u.full_name,u.username,u.id,u.role,u.created,pg.user_id,pg.page  FROM users as u left join page_logs as pg on u.id=pg.user_id where u.created > '%s'" % (yesterday,))
        elif sys.argv[3] == "likelyToSubscribe":
            a = str("call getLikelyToSubscribe(NULL)")
        else:
            a = str("SELECT DISTINCT(u.email),u.full_name,u.username,u.id,u.role,u.created  FROM users as u where username='%s'" % ("joseph",))

    # send email entries in matchjobs where skill_fit is 0 (3 arguments, last argument is classcode)
    if sys.argv[2] == "unfit4job":
        a = str("call unfit4job (%s)" % (sys.argv[3],))


if sys.argv[1] == "2":
    if sys.argv[2] == "b":
        a = str("select id,fname,lname,username,created from users")
    elif sys.argv[2] == "c":
        a = str("select * from expertsearch")


#if sys.argv[1] == "1":
#    connection = MySQLdb.connect (host = "localhost", user = "houseboy", passwd = "H56ouse.yob", db = "linuxjobber");
#elif sys.argv[1] == "2":
#    connection = MySQLdb.connect (host = "localhost", user = "houseboy", passwd = "H56ouse.yob", db = "noobaid");

if sys.argv[1] == "1":
    connection = MySQLdb.connect (host=parser.get('linuxjobber','host'),user=parser.get('linuxjobber','user'),passwd=parser.get('linuxjobber','passwd'),db=parser.get('linuxjobber','db'));
elif sys.argv[1] == "2":
    connection = MySQLdb.connect (host=parser.get('noobaid','host'),user=parser.get('noobaid','user'),passwd=parser.get('noobaid','passwd'),db=parser.get('noobaid','db'));



cursor = connection.cursor ()

# execute the SQL query using execute() method.
cursor.execute (a)

if sys.argv[2] != "insert":
    # fetch all of the rows from the query
    results = cursor.fetchall ()

    widths = []
    columns = []
    tavnit = '|'
    separator = '+' 

    for cd in cursor.description:
        widths.append(max(cd[2], len(cd[0])))
        columns.append(cd[0])

    for w in widths:
        tavnit += " %-"+"%ss |" % (w,)
        separator += '-'*w + '--+'

    for row in results:
        full_name = row[1].replace(" ","__")
        print( full_name+' : '+row[2])

        #empty extra_msg means that we are sending extra messages. However, we deliberately put whitespace so that argument is a  character otherwise, python complains
        if extra_msg_desc == " ":
            extra_msg = extra_msg_desc.replace(" ","__")
        else:
            day_of_completion = str.split( str( row[7]))
            raw_msg = extra_msg_desc+' linebreak On '+day_of_completion[0]+': '+row[2]
            extra_msg = raw_msg.replace(" ","__")

        if sys.argv[2] == "test":
            if sys.argv[3] == "yesterdays":
                #replace temporary strings
                copyfile( 'yesterdays.orig', 'yesterdays.edit')
                setMsgFile( 'yesterdays.edit', str( row[7]),'PUT_SKILL')
                copyfile( 'yesterdays.edit', 'messages/yesterdays.py')
            os.system('python emailer.py %s %s %s' % (TEST_EMAIL, TESTER, extra_msg))
        else:
            os.system('python emailer.py %s %s %s' % (row[0], full_name, extra_msg))
            #after emailing unfit4jobs, be sure to set the value of do_no_send to 1 in matchjobs. Otherwise, you'll get complains

cursor.close ()

# close the connection
connection.close ()

#whatever the second argument is, let emailer use it as message file. In the event emailer MSGS_FILE screws up, default is below
#from MSGS_FILE import MSG
#from MSGS_FILE import TITLE
#if sys.argv[2] == "test":
setMsgFile( 'emailer.py', 'MSGS_FILE','messages.'+sys.argv[3])
#else:
#    setMsgFile( 'MSGS_FILE','messages.'+sys.argv[2])

# exit the program
sys.exit()
