#!/usr/bin/python
import ConfigParser
import MySQLdb
import sys
import subprocess
import datetime

#CONFIG_FILE = '/home/showpopulous/config/pyconfg.cfg'
CONFIG_FILE = '/home/linuxjobber/tools/config.ini'
def addToList( instance):
    instance_list = open("aws_instance_list", "a")
    items = instance.split("'")
    for item in items:
        if 'instance_ip' in item:
            ip_only=item.replace("instance_ip=", "")
            instance_list.write( str( ip_only) + "\n")
    instance_list.close()

if len(sys.argv)  == 1:
    print( "Enter a numeric argument")
    exit()
elif sys.argv[1] == "show":
    print( "1 -> linuxjobber","2 -> noobaid")
    print( "1 a -> get lj trainings","2 b -> get nb users","2 c -> expert searches")
    exit()

queries = list()
if sys.argv[1] == "1":
    if sys.argv[2] == "a":
        a = str("call getPageLogs()")
        queries.append( a)
    if sys.argv[2] == "b":
        a = str("select id,full_name,email,created from users ")
        queries.append( a)
    if sys.argv[2] == "c":
        a = str("select aw.id,aw.user_id,u.full_name, u.username, aw.access_Key_id, aw.secret_access_key, aw.created from aws_settings as aw join users as u on u.id=aw.user_id")
        queries.append( a)
    if sys.argv[2] == "d":
        a = str("select * from users where role=3")
        queries.append( a)
    if sys.argv[2] == "e":
        a = str("select * from do_not_send")
        queries.append( a)
    if sys.argv[2] == "f":
        if len(sys.argv) == 3:
            a = str("select id,fname,lname,email,classcode,created from jobs")
        elif len(sys.argv) == 5:
            a = str("select id,fname,email,resume from jobs where classcode=%s and id=%s" % (sys.argv[3],sys.argv[4]))
        elif len(sys.argv) == 4:
            if int(sys.argv[3]) < 20:
                a = str("select id,fname,lname,email,classcode,created from jobs where classcode=%s" % (sys.argv[3],))
            else:
                a = str("select resume from jobs where id=%s" % (sys.argv[3],))
        queries.append( a)
    if sys.argv[2] == "g":
        if len(sys.argv) == 4:
            a = str("call getUserDossier(%s)" % (sys.argv[3],))
        else:
            a = str("select sc.user_id,sc.day,sc.time,sc.day_2,sc.time_2,sc.mode,sc.mode_2,sc.phone,u.full_name from schedules as sc left join users as u on sc.user_id=u.id")
        queries.append( a)

    if sys.argv[2] == "h":
        if len(sys.argv)  == 3:
            a = str("call getVideoWatchers(NULL)")
        elif sys.argv[3] == "today":
            today=datetime.datetime.now().strftime("%Y-%m-%d")
            a = str("call getVideoWatchers('%s')" % (today,))
        #if len(sys.argv) == 4:
        #    # to find video finishers for a specific day, enter the date as argument. e.g ~/daily 1 h 2017-08-22
        #    a = str("call getVideoWatchers('%s')" % (sys.argv[3],))
        else:
             a = str("call getVideoWatchers('%s')" % (sys.argv[3],))
        #    a = str("call getVideoWatchers(NULL)")
        queries.append( a)

    if sys.argv[2] == "i":
        if len(sys.argv) == 4:
            # to find video likely subscribers for a specific day, enter the date as argument. e.g ~/daily 1 i 2017-08-22
            #a = str("call getLikelyToSubscribe('%s'  - INTERVAL 1 DAY)" % (sys.argv[3],))
            a = str("call getLikelyToSubscribe('%s')" % (sys.argv[3],))
        else:
            a = str("call getLikelyToSubscribe(NULL)")
        queries.append( a)

    if sys.argv[2] == "j":
        a = str("select u.full_name,ui.city,ui.country_name,ui.coursename,ui.created from users as u right join user_interests as ui on u.id=ui.user_id")
        queries.append( a)

    if sys.argv[2] == "k":
        if len(sys.argv)  == 3:
            a = str("select u.username,lr.user_id,lr.lab_name,lr.labmap_id,lr.labmap_id,lr.task_id,lr.lab_result,lr.lab_date from lab_reports as  lr left join users as u on u.id=lr.user_id WHERE DATE(lr.lab_date) = (CURDATE() - INTERVAL 1 DAY);")
        elif sys.argv[3] == "all":
            a = str("select u.username,lr.user_id,lr.lab_name,lr.labmap_id,lr.labmap_id,lr.task_id,lr.lab_result,lr.lab_date from lab_reports as  lr left join users as u on u.id=lr.user_id;")
        elif sys.argv[3] == "info":
            a = str("select u.username,lr.user_id,lr.lab_name,lr.labmap_id,lr.labmap_id,lr.task_id,lr.lab_result,lr.lab_date,u.email from lab_reports as  lr left join users as u on u.id=lr.user_id;")
        elif sys.argv[3] == "today":
            a = str("select u.username,lr.user_id,lr.lab_name,lr.labmap_id,lr.labmap_id,lr.task_id,lr.lab_result,lr.lab_date from lab_reports as  lr left join users as u on u.id=lr.user_id WHERE DATE(lr.lab_date) = CURDATE();")
        queries.append( a)

    if sys.argv[2] == "l":
        a = str("select distinct(email),full_name,amount user_id,created from group_course_registers where 1 group by email order by created asc")
        queries.append( a)
 
    if sys.argv[2] == "m":
        a = str("select full_name,email,phone_number,home_address,course_title, created from internships")
        queries.append( a)

    if sys.argv[2] == "s":
        a = str("select  COUNT( id) from users where created > TIMESTAMP( DATE_SUB( NOW(), INTERVAL 6 day))")
        queries.append( a)
        a = str("select DAYNAME(created), COUNT( id) from users where created > TIMESTAMP( DATE_SUB( NOW(), INTERVAL 7 day)) AND DAYNAME(created)='Sunday'")
        queries.append( a)
        a = str("select DAYNAME(created), COUNT( id) from users where created > TIMESTAMP( DATE_SUB( NOW(), INTERVAL 6 day)) AND DAYNAME(created)='Monday'")
        queries.append( a)
        a = str("select DAYNAME(created), COUNT( id) from users where created > TIMESTAMP( DATE_SUB( NOW(), INTERVAL 6 day)) AND DAYNAME(created)='Tuesday'")
        queries.append( a)
        a = str("select DAYNAME(created), COUNT( id) from users where created > TIMESTAMP( DATE_SUB( NOW(), INTERVAL 6 day)) AND DAYNAME(created)='Wednesday'")
        queries.append( a)
        a = str("select DAYNAME(created), COUNT( id) from users where created > TIMESTAMP( DATE_SUB( NOW(), INTERVAL 6 day)) AND DAYNAME(created)='Thursday'")
        queries.append( a)
        a = str("select DAYNAME(created), COUNT( id) from users where created > TIMESTAMP( DATE_SUB( NOW(), INTERVAL 6 day)) AND DAYNAME(created)='Friday'")
        queries.append( a)
        a = str("select DAYNAME(created), COUNT( id) from users where created > TIMESTAMP( DATE_SUB( NOW(), INTERVAL 6 day)) AND DAYNAME(created)='Saturday'")
        queries.append( a)

    if sys.argv[2] == "t":
        a = str("select u.full_name, u.username, aw.access_Key_id, aw.secret_access_key from aws_settings as aw left join users as u on u.id=aw.user_id")
        queries.append( a)

if sys.argv[1] == "2":
    if sys.argv[2] == "b":
        a = str("select id,fname,lname,username,created from users")
    elif sys.argv[2] == "c":
        a = str("select * from expertsearch")

parser = ConfigParser.SafeConfigParser()
parser.read( CONFIG_FILE)

if sys.argv[1] == "1":
    connection = MySQLdb.connect (host=parser.get('linuxjobber','host'),user=parser.get('linuxjobber','user'),passwd=parser.get('linuxjobber','passwd'),db=parser.get('linuxjobber','db'));
elif sys.argv[1] == "2":
    connection = MySQLdb.connect (host=parser.get('noobaid','host'),user=parser.get('noobaid','user'),passwd=parser.get('noobaid','passwd'),db=parser.get('noobaid','db'));

def runAndPrint( connection, a):

    cursor = connection.cursor ()

    # execute the SQL query using execute() method.
    cursor.execute (a)


    if sys.argv[2] == "t":
        # fetch all of the rows from the query
        results = cursor.fetchall ()
        #empty running machines list in this directory
        open('aws_instance_list', 'w').close()
        for aws_user in results:
            try:
                aws_output = subprocess.check_output('python /var/www/html/cake2/app/webroot/python/s3_sample.py %s %s instance_running' % (aws_user[2],aws_user[3]), shell=True).split('\n')
                for line in aws_output:
                    if 'instance_ip' in line:
                        print( str(aws_user[0])+" --------------> "+ line)
                        # update running machines list
                        addToList( line)
            except subprocess.CalledProcessError as cpe:
                print ( str(aws_user[0])+'----- AWS account error')

    elif sys.argv[2] != "insert":
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

        print(separator)
        print(tavnit % tuple(columns))
        print(separator)
        for row in results:
            print(tavnit % row)
        print(separator)

    cursor.close ()

for qry in queries:
    runAndPrint( connection, qry)

# close the connection
connection.close ()

# exit the program
sys.exit()
