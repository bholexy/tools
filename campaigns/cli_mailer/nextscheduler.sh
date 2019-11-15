#!/usr/bin/bash	

#########################################################
#
# To run a test,  type the following at 
#   the bottom of the file and run it
#   cd $HOME && ./composeMail.py 1 test two_15pm_sundays
# To run this script with default ROLE and MSG, 
#   just use: ./scheduler.py
#   To pass the ROLE & MSG as arguments, 
#   use: ./scheduler.py switch_career select_mode_of_learning
#
#########################################################

###### SECTION 1: Modify this section before sending
###### MSG_FILE is the file that is holding the message to send
if [ ! -z "$1" ] && [ ! -z "$2" ];
then
    ROLE=$1
    MSG='groups/switch_career/select_learning_mode.py'
else
    ROLE='all_role6'
    #ROLE='nigerian_internship'
    #ROLE='part_time_fresh_grads'

    MSG='internship_angular_begins_tomorrow'
    #MSG='nigerian_remote_internship_starting'
    #MSG='internship_starts_today'
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
