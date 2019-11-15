#!/usr/bin/python
import ConfigParser
import MySQLdb
import sys
import fileinput
import os
import weneeds
import composeMessage
import persons
import datetime
from prettytable import PrettyTable
from datetime import date, timedelta
from shutil import copyfile

##############################################################
#
##############################################################

#CONFIG_FILE = '/tools/tool/config.ini'
parser = ConfigParser.SafeConfigParser()

CONFIG_FILE = '/home/linuxjobber/tools/config.ini'
parser.read( CONFIG_FILE)

def main():
    db_conn = get_db_object( parser)
    if len(sys.argv)  == 1:
        print( "add action as argument: addperson, showperson, updateperson, checkstatus etc")
        exit()

    elif sys.argv[1] == "addperson":        
        if len(sys.argv)  <= 2:
            print( "More arguments needed. trainee, student or graduant ")
        else: 
            weperson = persons.person()
            if sys.argv[2] == 'trainee':
                weperson.get_details( 'trainee', get_valid_roles(), get_valid_types())
            elif sys.argv[2] == 'student':
                weperson.get_details( 'student', get_valid_roles(), get_valid_types())
            else:
                weperson.get_details( 'graduant', get_valid_roles(), get_valid_types())
            person_user_id = get_user_id( db_conn, weperson.get_email())
            if( store_person( db_conn, weperson, person_user_id)):
                print( weperson.get_first_name() + " successfully added")

    elif sys.argv[1] == "checkstatus":
        if len(sys.argv)  <= 2:
            print( "check status of what? Enter income_verification, graduation_reminder [y/n], check_roles etc ")
        else:
            weperson = persons.person()
            active_users = get_active_users( db_conn)
            i = 1
            for user in active_users:
                weperson.set_user( user)
                print("\n" + str(i) + ". Checking " + weperson.gett_first_name() + " " + weperson.gett_last_name())
                i += 1
                user_needs = weneeds.needs()

                if sys.argv[2] == 'check_roles':
                    if user_needs.needs_role_change( weperson.gett_last_verification(),weperson.gett_graduation_date(), weperson.gett_role()):
                        print("Changing user role to: graduated")

                if sys.argv[2] == 'graduation_reminder' and user_needs.graduation_reminder( weperson.gett_graduation_date()):
                    msg = composeMessage.compose('graduation_reminder')
                    if len(sys.argv)  >= 4:
                        if sys.argv[3] == 'y':
                            status = msg.sendMessageGrad( weperson.gett_email(), weperson.gett_first_name(), weperson.gett_graduation_date())
                            print( status)
                        else:
                            print( "Not really sending the email")
                if sys.argv[2] == 'income_verification' and user_needs.income_verification( weperson.gett_last_verification(),weperson.gett_graduation_date(), weperson.gett_role()):
                    print("---" + weperson.gett_first_name() + " " + weperson.gett_last_name() + " " + "needs income verification")
                    print("...sending " + weperson.gett_first_name()
                     + " an email to verify income")
                    msg = composeMessage.compose('income_verification')
                    status = msg.sendMessage( weperson.gett_email(), weperson.gett_first_name(), weperson.gett_last_verification())
                    inform_admin( msg, weperson.gett_first_name()+" "+weperson.gett_last_name(), weperson.gett_last_verification())
                    print(status)
                print("person is type: " + weperson.gett_role())

    elif sys.argv[1] == "showperson":
        if len(sys.argv)  <= 2:
            print( "Either enter a persons name, all, tasks or brief")
        else: 
            if sys.argv[2] == 'all':
                weperson = persons.person()
                list_all_persons( db_conn)
            elif sys.argv[2] == "brief":
                active_users = get_active_users_brief( db_conn)
                x = PrettyTable()
                for user in active_users:
                    print( x.add_row( user))
                print( x)
            elif sys.argv[2] == "tasks":
                if len(sys.argv)  <= 3:
                    print( "Either enter the name of the user whose tasks you wish to see before tasks")
                
            else:
                if len(sys.argv)  == 2:
                    weperson = persons.person()
                    get_person( db_conn, sys.argv[2])
                if len(sys.argv)  == 3:
                    weperson = persons.person()
                    get_person( db_conn, sys.argv[2])
                elif len(sys.argv)  == 4:
                    if sys.argv[3] == "tasks":
                        user_tasks = get_tasks( db_conn, sys.argv[2])
                        for tasks in user_tasks:
                            print( tasks)
                
                

    elif sys.argv[1] == "updateperson":        
        if len(sys.argv)  <= 2:
            print( "You must enter the name of the person who's info you wish to change")
        else: 
            if len( sys.argv) <= 3:
                print( "You must enter the info you wish to change. role, graduation_date, last_verification?")
            else:
                roles = ['graduated', 'verified', 'trainee', 'breach', 'student', 'resigned']
                weperson = persons.person()
                person_to_change = sys.argv[2]
                info_to_change = sys.argv[3]
                users = get_person( db_conn, person_to_change)
                for user in users:
                    weperson.set_user( user)
                    if info_to_change == 'role':
                        print("Valid roles: graduated, verified, trainee, breach, student, resigned, or x to exit")
                        oldInfo = weperson.gett_role()

                    elif info_to_change == 'graduation_date':
                        oldInfo = weperson.gett_graduation_date().strftime('%Y-%m-%d')

                    elif info_to_change == 'last_verification':
                        oldInfo = weperson.gett_last_verification().strftime('%Y-%m-%d')

                    else:
                        print ( info_to_change + " is not a valid option. It will not correspond to a column in the database")

                    newInfo = raw_input("Enter new "+info_to_change+" for: " + weperson.gett_first_name() + " " + weperson.gett_last_name() + ". Hit enter to ignore person: ")
                    if isValidRole( newInfo, get_valid_roles()) or isValidDate( newInfo): 
                        print( "Okay, changing " + info_to_change + " from " + str( oldInfo) + " to " + newInfo) 
                        update_person( db_conn, weperson.gett_first_name(), weperson.gett_last_name(), info_to_change, newInfo)
                    else:
                        print( "Okay, not making changes for " + weperson.gett_first_name() + " " + weperson.gett_last_name())

                    print ("==========================")


    elif sys.argv[1] == "status":
        weperson = persons.person()
        all_users = get_all_users( db_conn)
        i = 1
        for user in all_users:
            weperson.set_user( user)

            print("\n" + str(i) + ". Checking " + weperson.gett_first_name() + " " + weperson.gett_last_name())
            user_needs = weneeds.needs()
            i += 1
            user_needs.status(weperson.gett_graduation_date(),weperson.gett_last_verification())

def isValidRole( role, validRoles):
    if role in validRoles:
        return True
    else:
        return False

def isValidDate( date_string):
    date_format = '%Y-%m-%d'
    try:
        date_obj = datetime.datetime.strptime(date_string, date_format)
        print(date_obj)
        return True
    except ValueError:
        print("Incorrect data format, should be YYYY-MM-DD")
        return False

def get_valid_roles():
    validRoles = ['graduated', 'verified', 'trainee', 'breach', 'student', 'resigned']
    return validRoles

def get_valid_types():
    validTypes = ['DevOps', 'Linux Administrator', 'AWS Architect', 'Python Developer', 'Quality Assurance', 'Cyber Security']
    return validTypes

def inform_admin( msg, person_name, dummydate):
    adminMail = parser.get('wepeoples','admin_email')
    status = msg.sendMessage( adminMail, person_name, dummydate)
    print( "Informed admin")
    #print( "Name: "+person_name+" , DummyDate: "+str( dummydate))

################## Business Logic #########################

def update_person( conn, fname, lname, column, newInfo):
    cursor = conn.cursor()
    
    if column == 'role':
        column='h.person_id'
        newInfo_qry = """select id from home_werole where roles=%s"""
        cursor.execute(( newInfo_qry), ( newInfo, ))
        cursor._executed
        result = cursor.fetchall()
        newInfo = int( result[0][0])

    qry = """UPDATE home_wepeoples as h left join users_customuser as u on h.user_id=u.id left join home_wetype as p on h.types_id=p.id left join home_werole as r on h.person_id=r.id SET """+column+"""=%s WHERE u.first_name=%s AND u.last_name=%s"""
    cursor.execute((qry), ( newInfo, fname, lname))
    cursor._executed
    conn.commit()
    conn.close()

def get_user_id( conn, person_email):
    cursor = conn.cursor()
    qry = """select id from users_customuser where email=%s"""
    cursor.execute( (qry), ( person_email, ) )
    cursor._executed
    result = cursor.fetchall()
    try:
        userID = result[0][0]
        return userID
    except IndexError:
        print("This user does not exist in database")
        return None

def get_all_users( conn):
    cursor = conn.cursor()
    qry = """ SELECT h.id, u.first_name, u.last_name, u.email, p.types, h.current_position, h.state, h.income, h.relocation, h.last_verification, h.start_date, h.graduation_date, r.roles  FROM home_wepeoples as h left join users_customuser as u on h.user_id=u.id left join home_wetype as p on h.types_id=p.id left join home_werole as r on h.person_id=r.id"""
    cursor.execute(qry)
    cursor._executed
    result = cursor.fetchall()
#    conn.commit()
    conn.close()
    return result

def get_active_users( conn):
    cursor = conn.cursor()
    qry = """ SELECT h.id, u.first_name, u.last_name, u.email, p.types, h.current_position, h.state, h.income, h.relocation, h.last_verification, h.start_date, h.graduation_date, r.roles  FROM home_wepeoples as h left join users_customuser as u on h.user_id=u.id left join home_wetype as p on h.types_id=p.id left join home_werole as r on h.person_id=r.id WHERE h.person_id<>4"""
    cursor.execute(qry)
    cursor._executed
    result = cursor.fetchall()
    conn.commit()
#    conn.close()
    return result

def get_active_users_brief( conn):
    cursor = conn.cursor()
    qry = """SELECT  u.first_name, u.email, r.roles, h.start_date, h.graduation_date FROM home_wepeoples as h left join users_customuser as u on h.user_id=u.id left join home_wetype as p on h.types_id=p.id left join home_werole as r on h.person_id=r.id WHERE r.roles<>'resigned' order by h.graduation_date DESC"""
    cursor.execute(qry)
    cursor._executed
    result = cursor.fetchall()
    conn.commit()
#    conn.close()
    return result

def get_tasks( conn, name):
    cursor = conn.cursor()
    qry = """SELECT k.task_id, u.first_name, u.last_name, t.task, h.person_id, k.status FROM home_wepeoples as h left join users_customuser as u on h.user_id=u.id left join home_wetype as p on h.types_id=p.id left join home_werole as r on h.person_id=r.id left join home_wework as k on h.id=k.we_people_id left join home_wetask as t on t.id=k.task_id WHERE u.first_name like %s OR u.last_name like %s"""
    cursor.execute((qry), (name, name))
    cursor._executed
    result = cursor.fetchall()
    conn.commit()
#    conn.close()
    return result

def list_all_persons( conn):
    cursor = conn.cursor()
    qry = """ SELECT u.first_name, u.last_name FROM home_wepeoples left join users_customuser as u on home_wepeoples.user_id=u.id"""
    cursor.execute(qry)
    #cursor._executed
    result = cursor.fetchall()
    for x in result:
        print(x)
#    conn.commit()
    conn.close()

def get_person( conn, name):
    cursor = conn.cursor() 
    qry = """ SELECT h.id, u.first_name, u.last_name, u.email, p.types, h.current_position, h.state, h.income, h.relocation, h.last_verification, h.start_date, h.graduation_date, r.roles FROM home_wepeoples as h left join users_customuser as u on h.user_id=u.id left join home_wetype as p on h.types_id=p.id left join home_werole as r on h.person_id=r.id WHERE u.first_name like %s OR u.last_name like %s """
    cursor.execute((qry), ( name, name))
    keys = ('ID','First Name','Last Name','Email','person_id','Current Position','State','Current Salary','Will Relocate','Last Income Verification','Date Started','Graduation Date','Person Type')
    result = cursor.fetchall()
    for x in result:
        i = 0
        #print(x)
        for y in x:
            print(keys[i], y)
            i += 1 
    conn.commit()
#    conn.close()
    return result

def store_person( conn, trainee, person_user_id):

    cursor = conn.cursor() 

    #qry = """ INSERT INTO home_wepeoples(first_name,last_name,email,trainee_position,current_position,state,income,relocation,last_verification,start_date,graduation_date,type) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    qry = """ INSERT INTO home_wepeoples( profile_picture, current_position, state, income, relocation, Paystub, last_verification, start_date, graduation_date, types_id, user_id, person_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    cursor.execute(( qry) , (trainee.get_profile_picture(), 
                             trainee.get_current_position(),
                             trainee.get_state(),
                             trainee.get_income(),
                             trainee.get_relocation(),
                             trainee.get_paystub(),
                             trainee.get_last_verification(),
                             trainee.get_start_date(),
                             trainee.get_graduation_date(),
                             trainee.get_type(),
                             person_user_id,
                             trainee.get_person_id()
                             ))
    result = cursor.fetchall()
    for x in result:
        print(x)
    conn.commit()
#    conn.close()

def get_db_object( parser):
    connection = MySQLdb.connect (host=parser.get('linuxjobber','host'),user=parser.get('linuxjobber','user'),passwd=parser.get('linuxjobber','passwd'),db=parser.get('linuxjobber','db'))
    return connection

if __name__ == "__main__":
    main()
