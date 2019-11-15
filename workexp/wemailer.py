#!/usr/bin/python
import ConfigParser
import MySQLdb
import sys
import os
import smtplib
import datetime

sys.path.append('/var/www/html/linuxjobber.local/ai/chuck/wepeoples/messages')
#from MSGS_FILE import MSG
#from MSGS_FILE import TITLE

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

################################
# Call this prgm like this: python ./emailsender.py joseph.showunmi@linuxjobber.com joseph
#
################################

#SITE_LOGO_ADDRESS='http://linuxjobber.com/img/linuxjobber_logo.png'
#SITE_ALT='http://www.linuxjobber.com'

##SENDER = '"Elena Edwards" <elenae@noobaid.com>'
#SENDER = '"Elena Edwards" <elena.edwards@linuxjobber.com>'
#RECIPIENT = sys.argv[1] #"noobaidmail@gmail.com"
##SENDER = '"Joseph Showunmi" <joseph.showunmi@linuxjobber.com>'
##RECIPIENT = "noobaidmail@gmail.com"

#CONFIG_FILE = '/tools/tool/config.ini'

CONFIG_FILE = '/home/linuxjobber/tools/config.ini'
parser = ConfigParser.SafeConfigParser()
parser.read( CONFIG_FILE)

#SITE_LOGO_ADDRESS=parser.get('chuck','SITE_LOGO_ADDRESS')
SITE_LOGO_ADDRESS='https://www.linuxjobber.com/static/home/images/logo.png'
SITE_ALT=parser.get('chuck','SITE_ALT')
SENDER=parser.get('chuck','SENDER')
RECIPIENT = sys.argv[1] #"noobaidmail@gmail.com"
TITLE = sys.argv[4].replace('_',' ')

AWS_ACCESS_KEY=parser.get('linuxjobber','AWS_ACCESS_KEY')
AWS_SECRET_KEY=parser.get('linuxjobber','AWS_SECRET_KEY')

msg = MIMEMultipart('alternative')
msg['Subject'] = TITLE
#msg['Subject'] = sys.argv[3]
msg['From'] = SENDER
msg['To'] = RECIPIENT
MSGE=sys.argv[5].replace("_","<br />")
FNAME = sys.argv[2].replace("__"," ")
typemes = sys.argv[6]
date = sys.argv[3]


TEXT="Hi, "+sys.argv[2]+MSGE

#
# Build email template
#

if typemes == '1':
  print("yes")
  HTML = """\
     <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
     <html xmlns="http://www.w3.org/1999/xhtml">
     <head>
       <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
         <title>Pymail</title>
       <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
     </head>

     <body style="margin: 0; padding: 0;">
       <table  align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse;">
         <tr>
           <td bgcolor="#ffffff" style="padding: 30px 20px 30px 20px; background-color: #f6f6f6;">
             <table  cellpadding="10" cellspacing="10" width="100%" style="background-color: #ffffff; border: 1px solid #e4e4e4; font-size: 17px; line-height: 25px; font-family: georgia; color: #696969">
               <tr>
                 <td>
                   <table><tr><td><img src="""+SITE_LOGO_ADDRESS+""" alt="""+SITE_ALT+""" /></td></tr><tr><td>&nbsp;&nbsp;</td></tr></table>
                   <p>Hi """+FNAME+""",<br /><br />
                     """+MSGE+"""<br>"""+date+"""
                   </p>
                  
                   <p>
                     Let me know if you have any questions. <br /><br />
                     Thank you,<br />
                     Elena Edwards <br />
                     Resource Specialist <br />
                     Email: elena.edwards@linuxjobber.com <br />
                     Url: <a href="http://www.linuxjobber.com">https://www.linuxjobber.com</a><br />
                  </p>
                 </td>
               </tr>
               <tr><td style="font-size:10px;">If you wish to unsubscribe, please reply with unsubscribe in subject line</td></tr>
             </table>
           </td>
         </tr>
       </table>
     </body>
     </html>
  """
else:
  HTML = """\
     <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
     <html xmlns="http://www.w3.org/1999/xhtml">
     <head>
       <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
         <title>Pymail</title>
       <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
     </head>

     <body style="margin: 0; padding: 0;">
       <table  align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse;">
         <tr>
           <td bgcolor="#ffffff" style="padding: 30px 20px 30px 20px; background-color: #f6f6f6;">
             <table  cellpadding="10" cellspacing="10" width="100%" style="background-color: #ffffff; border: 1px solid #e4e4e4; font-size: 17px; line-height: 25px; font-family: georgia; color: #696969">
               <tr>
                 <td>
                   <table><tr><td><img src="""+SITE_LOGO_ADDRESS+""" alt="""+SITE_ALT+""" /></td></tr><tr><td>&nbsp;&nbsp;</td></tr></table>
                   <p>Hi """+FNAME+""",<br /><br />
                     """+MSGE+"""
                   </p>
                  
                   <p>
                     Let me know if you have any questions. <br /><br />
                     Thank you,<br />
                     Elena Edwards <br />
                     Resource Specialist <br />
                     Email: elena.edwards@linuxjobber.com <br />
                     Url: <a href="http://www.linuxjobber.com">https://www.linuxjobber.com</a><br />
                  </p>
                 </td>
               </tr>
               <tr><td style="font-size:10px;">If you wish to unsubscribe, please reply with unsubscribe in subject line</td></tr>
             </table>
           </td>
         </tr>
       </table>
     </body>
     </html>
  """

part1 = MIMEText(TEXT, 'plain')
part2 = MIMEText(HTML, 'html')

msg.attach(part1)
msg.attach(part2)

#keep copies of sent mails so that admin can view via url
today=datetime.datetime.today().strftime('%Y-%m-%d')
directory = 'copy_of_sent_email/%s' % (today,)
if not os.path.exists( directory):
    print( directory + ' does not exist. Now creating .....')
    os.makedirs( directory)
    print ( 'done, now writing file to directory: '+ directory)
else:
    print( 'now writing file to directory: ' + directory)

viewable=open(directory+'/'+FNAME+'.html','w')
viewable.write( msg.as_string())
viewable.close

#print( msg.as_string())

smtpObj = smtplib.SMTP('email-smtp.us-west-2.amazonaws.com',587)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login(AWS_ACCESS_KEY,AWS_SECRET_KEY)

smtpObj.sendmail( SENDER, RECIPIENT, msg.as_string())
smtpObj.quit()
