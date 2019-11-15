#!/bin/bash

cd /home/sshowunmi/spool/mail/ && /home/sshowunmi/.local/bin/aws s3 mv --recursive s3://ljallmails .  
for i in $(ls /home/sshowunmi/spool/mail/)
do 
    echo 'moving' $i
    /tools/sortMails/sortEmail.py $i
    #sudo movePersonMails.py elenae@noobaid.com /home/sshowunmi/.local/share/evolution/mail/local/elenae_noobaid/new/

#    sudo mv /home/sshowunmi/spool/mail/$i /home/sshowunmi/.local/share/evolution/mail/local/new
done
 
#cd /tools/sortMails/ && ./sortEmail.py 2>&1
