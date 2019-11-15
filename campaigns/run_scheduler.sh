#!/bin/bash

#
# call this script like this #run_scheduler.sh MSG_FILE SLUG
#

#send to all_role6 on oldtools 
# this uses message file location
cd /oldtools/campaign && ./scheduler.sh all_role6 groups/full_training/making_less_than_110k.py 

#send to all_role6 on new tools/campaigns 
# this uses slugs to find message
cd /tools/tool/campaigns && ./scheduler.sh all_role6 making_less_than_110k

#send to part_time_fresh_grads on new tools/campaigns 
# this uses slugs to find message
cd /tools/tool/campaigns && ./scheduler.sh part_time_fresh_grads making_less_than_110k 

#send to switch_careers on new tools/campaigns 
# this uses message file location
cd /tools/tool/campaigns/cli_mailer && ./scheduler.sh switch_career groups/full_training/making_less_than_110k.py 

#send to all_full_time_job_applicants on new tools/campaigns 
# this uses message file location
cd /tools/tool/campaigns/cli_mailer && ./scheduler.sh all_full_time_job_applicants groups/full_training/making_less_than_110k.py

#cd /tools/tool/cam
