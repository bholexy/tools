#import pdfkit 
import os
import fileinput
import shutil
import yagmail
import string
import random
from configparser import ConfigParser
from PIL import Image
import zipfile
import base64
#import mysql.connector
#from python_mysql_dbconfig import read_db_config
from mysql.connector import MySQLConnection, Error
#from python_mysql_dbconfig import read_db_config
from weasyprint import HTML, CSS

config_url = "/home/linuxjobber/config/pyconfig.cfg"

#shutil.copy2('./certificate_angular.html','new_acert.html')
shutil.copy2('./certificate_django.html','new_dcert.html')

#def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
#   return ''.join(random.choice(chars) for _ in range(size))

##mysql dbconfig

from configparser import ConfigParser


def read_db_config(filename=config_url, section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db



def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

gid = randomStringDigits(6)

parser = ConfigParser()
parser.read(config_url)

name = input("Enter Graduate Name: ")
gname = name
#gid = input("Enter Graduate's Id: ")
date = input("Enter Graduation Date in the format dd/mm/yyyy: ")
course = input("Enter Technology Learned, Django, Angular, Linux: ")
email = input("Enter Graduate's Email Address: ")
img = input("Enter path to Graduate image: ")
nimg = img
aemail=parser.get('mail', 'username')
reps=parser.get('mail', 'recipients')
ntrainer=parser.get('cert', 'trainer')

print('******************************************')
print('The certificate is being generated...............')
print('******************************************')

if course == "Django":
    shutil.copy2('./certificate_django.html','new_dcert.html')

    for line in fileinput.input("new_dcert.html", inplace=True):
	    # inside this loop the STDOUT will be redirected to the file
	    # the comma after each print statement is needed to avoid double line breaks
	    print(line.replace("John Doe", name), end="")

    for line in fileinput.input("new_dcert.html", inplace=True):
	    # inside this loop the STDOUT will be redirected to the file
	    # the comma after each print statement is needed to avoid double line breaks
	    print(line.replace("eGQX78y", gid), end="")

    for line in fileinput.input("new_dcert.html", inplace=True):
	    # inside this loop the STDOUT will be redirected to the file
	    # the comma after each print statement is needed to avoid double line breaks
	    print(line.replace("01/02/2019", date), end="")

    for line in fileinput.input("new_dcert.html", inplace=True):
            # inside this loop the STDOUT will be redirected to the file
            # the comma after each print statement is needed to avoid double line breaks
            print(line.replace("images/userimage.png", img), end="")

    for line in fileinput.input("new_dcert.html", inplace=True):
            # inside this loop the STDOUT will be redirected to the file
            # the comma after each print statement is needed to avoid double line breaks
            print(line.replace("Jane Schoolfiled", ntrainer), end="")            

	#pdfkit.from_file('./new_dcert.html', './certificate.pdf')    
elif course == "Angular":
    shutil.copy2('./certificate_angular.html','new_dcert.html')
    for line in fileinput.input("new_dcert.html", inplace=True):
	    # inside this loop the STDOUT will be redirected to the file
	    # the comma after each print statement is needed to avoid double line breaks
	    print(line.replace("John Doe", name), end="")

    for line in fileinput.input("new_dcert.html", inplace=True):
	    # inside this loop the STDOUT will be redirected to the file
	    # the comma after each print statement is needed to avoid double line breaks
	    print(line.replace("eGQX78y", gid), end="")

    for line in fileinput.input("new_dcert.html", inplace=True):
	    # inside this loop the STDOUT will be redirected to the file
	    # the comma after each print statement is needed to avoid double line breaks
	    print(line.replace("01/02/2019", date), end="")

    for line in fileinput.input("new_dcert.html", inplace=True):
            # inside this loop the STDOUT will be redirected to the file
            # the comma after each print statement is needed to avoid double line breaks
            print(line.replace("images/userimage.png", img), end="")

    for line in fileinput.input("new_dcert.html", inplace=True):
            # inside this loop the STDOUT will be redirected to the file
            # the comma after each print statement is needed to avoid double line breaks
            print(line.replace("Jane Schoolfiled", ntrainer), end="")              	

	#pdfkit.from_file('./new_acert.html', './certificate.pdf')
######Linux Cert

elif course == "Linux":
    shutil.copy2('./certificate_linux.html','new_dcert.html')
    for line in fileinput.input("new_dcert.html", inplace=True):
        # inside this loop the STDOUT will be redirected to the file
        # the comma after each print statement is needed to avoid double line breaks
        print(line.replace("John Doe", name), end="")

    for line in fileinput.input("new_dcert.html", inplace=True):
        # inside this loop the STDOUT will be redirected to the file
        # the comma after each print statement is needed to avoid double line breaks
        print(line.replace("eGQX78y", gid), end="")

    for line in fileinput.input("new_dcert.html", inplace=True):
        # inside this loop the STDOUT will be redirected to the file
        # the comma after each print statement is needed to avoid double line breaks
        print(line.replace("01/02/2019", date), end="")

    for line in fileinput.input("new_dcert.html", inplace=True):
            # inside this loop the STDOUT will be redirected to the file
            # the comma after each print statement is needed to avoid double line breaks
            print(line.replace("images/userimage.png", img), end="")

    for line in fileinput.input("new_dcert.html", inplace=True):
            # inside this loop the STDOUT will be redirected to the file
            # the comma after each print statement is needed to avoid double line breaks
            print(line.replace("Jane Schoolfiled", ntrainer), end="") 

else:
    print('Certificate Template not Available.')


html = HTML('./new_dcert.html')

css = CSS(string='@page { size: A3; width: 40cm; align: center; margin-left: 2cm; margin-right: 0 }')

html.write_pdf(
    './certificate.pdf', stylesheets=[css]
    )

from wand.image import Image as wi
pdf = wi(filename="./certificate.pdf", resolution=300)
pdfimage = pdf.convert("jpeg")
i=1
for img in pdfimage.sequence:
    page = wi(image=img)
    page.save(filename='certificate.jpg')
    i +=1    

img = Image.open('certificate.jpg')
img.save('certificate.png')

  
zip_file = zipfile.ZipFile('certificate.zip', 'w')
zip_file.write('certificate.png', compress_type=zipfile.ZIP_DEFLATED)
zip_file.close()


types=parser.get('cert', 'type')

if types == "pdf":
    certy = './certificate.pdf'

else:
    certy = './certificate.zip'


#echo "PDF Created"
#echo " Email sending ........"
print('The Certificate has been Created.')
print('.')
print('.')
print('Email Sending to Admin and Graduate.......')
print('################################')


parser = ConfigParser()
parser.read(config_url)
#parser = get_parser()

username=parser.get('mail', 'username')
password=parser.get('mail', 'password')
SUBJECT = 'Certificate of Completion'
TEXT = name + ', Congratulations on Completing your Internship'
pdf = certy

yag = yagmail.SMTP(username, password, host='smtp.linuxjobber.com', port=587, smtp_starttls=True, smtp_ssl=False)
yag.send(email, SUBJECT, TEXT, pdf)
yag.send(aemail, SUBJECT, TEXT, pdf)
for name in [reps]:
    target = '{}'.format(name)
    yag.send(target.split(','), SUBJECT, TEXT, pdf)


#echo "Email Sent"
print('Email has been Sent to both Admin and Graduate.')

if os.path.exists("new_dcert.html"):
  os.remove("new_dcert.html")
else:
  print(".")

if os.path.exists("certificate.pdf"):
  os.remove("certificate.pdf")
else:
  print(".")

if os.path.exists("certificate.jpg"):
  os.remove("certificate.jpg")
else:
  print(".")  

if os.path.exists("certificate.zip"):
  os.remove("certificate.zip")
else:
  print(".")    

if os.path.exists("certificate.png"):
  os.remove("certificate.png")
else:
  print(".")      


print('#########################')
print('.')
print('.')
print('.')


def connect():
    """ Connect to MySQL database """

    db_config = read_db_config()

    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print('################################')
            print('.')
            print('.')
            print('.')
            print('connection has been established to the database.')
            mySql_insert_query = "INSERT INTO home_certificates (graduate_id, graduate_name, graduate_email, graduation_date, technology_learnt, image) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (gid, gname, email, date, course, nimg)
                 
            cursor = conn.cursor()
            result = cursor.execute(mySql_insert_query, val)
            conn.commit()
            print('######################################')
            print("Graduate Record added to the database successfully")
            cursor.close()




		
        else:
            print('connection failed.')

    except Error as error:
        print(error)

    finally:
        conn.close()
        print('Connection closed.')


if __name__ == '__main__':
    connect()
