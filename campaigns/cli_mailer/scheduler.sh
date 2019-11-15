#!/usr/bin/bash	

#########################################################
#
# To run a test,  type the following at 
#   the bottom of the file and run it
#   cd $HOME && ./composeMail.py 1 test two_15pm_sundays
#
#########################################################

###### SECTION 1:
###### MSG_FILE is the file that is holding the message to send

if [[ -z $1  || -z $2 ]]; then
    ###### Modify this section before sending
    ###### This part is used if this script is ran manually without arguments

    ##MSG_FILE='groups/combine_training/combine_linux_n_work_experience_program.py'
    ##MSG_FILE='groups/referral/linux_referral.py'
    #MSG_FILE='groups/congrats/congrats_niyi.py'
    ##MSG_FILE='groups/switch_career/select_learning_mode.py'

    ##MSG_FILE='groups/trainee/devops_trainee_needed.py'
    ##ROLE='all_role6'

    ##MSG_FILE='groups/internship/nigerian_remote_designer_internship.py'
    ##MSG_FILE='groups/trainee/linux_trainee_needed_starting_this_week.py'
    ##ROLE='switch_career'
    #ROLE='all_full_time_job_applicants'
    ######## YESTERDAYS
    ROLE='yesterdays_switch_career'
    MSG_FILE='groups/yesterdays/yesterdays_switch_career_registrants.py'
    #ROLE='yesterdays_interested_job_applicants'
    #MSG_FILE='groups/yesterdays/yesterdays_interested_job_applicants.py'
else
    ###### This part is used if this script is called from another script with arguments
    ROLE=$1
    MSG_FILE=$2
fi

###########################################################
###### SECTION 2: DO NOT EDIT BELOW THIS LINE #######

HOME='/tools/tool/campaigns/cli_mailer'
cd $HOME/messages

hour=$(date +%H)
if [ "$hour" -ge 15 ]; then
    LINK1='five_15pm_sundays.py'
    MSG='five_15pm_sundays'
elif  [ "$hour" -lt 15 ]; then
    LINK1='two_15pm_sundays.py'
    MSG='two_15pm_sundays'
fi

#remove next two lines. They are for testing only
#LINK1='five_15pm_sundays.py'
#MSG='five_15pm_sundays'

if [ -L $HOME/messages/$LINK1 ]; then
    rm $HOME/messages/$LINK1
fi

ln -s $HOME/messages/$MSG_FILE $HOME/messages/$LINK1
#echo $LINK1
#cd $HOME && echo $HOME && echo $ROLE && echo $MSG
cd $HOME && ./composeMail.py 1 $ROLE $MSG
