#!/bin/bash

# pull and email fundamentals and proficiency lab reports for students with ISA
cd /tools/tool/reports && ./email_lab_reports.py >> /tmp/daily_report.log

# pull and email report for currently active Work Experience people with ISA
cd /tools/tool/workexp && ./wepeople.py showperson brief | mutt -s 'WE Report for ISA people' -- showpopulous@gmail.com

# pull and email report for wepeople roles so that we can determine quickly who needs to give us paystub
cd /tools/tool/workexp && ./wepeople.py checkstatus check_roles | mutt -s 'Report for WE People Roles' -- showpopulous@gmail.com

# send email to yesterday's switch_career registrants
cd /tools/tool/campaigns/cli_mailer && ./scheduler.sh yesterdays_switch_career messages/groups/yesterdays/yesterdays_switch_career_registrants.py

# send email to yesterday's job registrants
cd /tools/tool/campaigns/cli_mailer && ./scheduler.sh yesterdays_interested_job_applicants messages/groups/yesterdays/yesterdays_interested_job_applicants.py

# clear TFT daily
cd /tools/tool/CS && /usr/bin/python3.6 ClearDT.py > /tmp/TFTreturn.log

# daily db backup
cd /mnt && sudo ./backup_linux.sh >> /tmp/backups.log
