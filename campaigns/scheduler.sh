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

    ROLE='all_role6'
    #ROLE='nigerian_internship'
    #ROLE='part_time_fresh_grads'

    MSG='congrats_niyi'
    #MSG='nigerian_remote_internship_starting'
    #MSG='internship_starts_today'
else
    ###### This part is used if this script is called from another script with arguments
    ROLE=$1
    MSG=$2
fi


###########################################################
###### SECTION 2: DO NOT EDIT BELOW THIS LINE #######

HOME='/tools/tool/campaigns'
cd $HOME/messages

hour=$(date +%H)
if [ "$hour" -ge 15 ]; then
    LINK1='five_15pm_sundays.py'
    #MSG='five_15pm_sundays'
elif  [ "$hour" -lt 15 ]; then
    LINK1='two_15pm_sundays.py'
    #MSG='two_15pm_sundays'
fi

if [ -f $LINK1 ] ; then
    rm $LINK1
fi

#ln -s $HOME/messages/$MSG_FILE $HOME/messages/$LINK1
#echo $LINK1
#cd $HOME && echo $HOME && ./composeMail.py 1 $ROLE $MSG
cd $HOME && ./composeMail.py 1 $ROLE $MSG
