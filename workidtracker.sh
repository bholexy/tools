#!/bin/bash
linuxjobber=/home/linuxjobber/linuxjobber2/tracker.yml
chatscrum=/home/linuxjobber/scrumastr/tracker.yml
linux=/home/linuxjobber/linuxjobber2
chat=/home/linuxjobber/scrumastr

echo "Enter workid: "
read workid


cd $linux
git fetch --all > fe.txt
git branch -r > branches.txt
latest=$(sed -n '2p' < branches.txt)
echo "${latest:9}" > ljb.txt
ne=$(cat ljb.txt)


cd $chat
git fetch --all > fe2.txt
git branch -r > branches2.txt
latest2=$(sed -n '2p' < branches2.txt)
echo "${latest2:9}" > ljb2.txt
ne2=$(cat ljb2.txt)

cd $linux
if grep -q -w int "ljb.txt"; then

	git checkout int
	git pull origin int
	#echo "workid not found" > int.txt
else
#	rm -rf int.txt
	git checkout $ne
	git pull origin $ne
	echo "##########################" > int.txt
   echo "      INT ENVIRONMENT" >> int.txt
   echo "##########################" >> int.txt
   echo "Workid $workid not found" >> int.txt
fi	

cd $chat
if grep -q -w integration "ljb2.txt"; then
	git checkout integration
	git pull origin integration
else
	git checkout $ne2
	git pull origin $ne2
fi	

echo
echo
clear

if grep -q -w $workid "$linuxjobber" "$chatscrum"; then
  clear
  cd $linux
  echo "#############################" > int.txt
  echo "       INT ENVIRONMENT" >> int.txt
  echo "#############################" >> int.txt
  echo "Workid $workid is present" >> int.txt
  cd $linux 
 # echo " commit Date and Time is" >> int.txt
 # git log -1 --format=%cd --date=local --grep=$workid >> int.txt
 # cd $chat
 # git log -1 --format=%cd --date=local --grep=$workid >> $linux/int.txt
  cat $linux/int.txt
else
	
   clear
   echo "##########################" > int.txt
   echo "      INT ENVIRONMENT" >> int.txt
   echo "##########################" >> int.txt
   echo "Workid $workid not found" >> int.txt
   cat $linux/int.txt
fi
echo
echo
cd $linux
git checkout int
git pull origin int
cd $chat
git checkout integration
git pull origin integration
cd $linux
if grep -q -w $workid "$linuxjobber" "$chatscrum"; then
  clear
  echo "#############################" > stage.txt
  echo "       STAGE ENVIRONMENT" >> stage.txt
  echo "#############################" >> stage.txt
  echo "Workid $workid is present" >> stage.txt
  cd $linux 
#  echo " commit Date and Time is" >> stage.txt
#  git log -1 --format=%cd --date=local --grep=$workid >> stage.txt
#  cd $chat
#  git log -1 --format=%cd --date=local --grep=$workid >> $linux/stage.txt
  cat $linux/stage.txt
else
	
   clear
   echo "##########################" > stage.txt
   echo "      STAGE ENVIRONMENT" >> stage.txt
   echo "##########################" >> stage.txt
   echo "Workid $workid not found" >> stage.txt
   cat $linux/stage.txt
fi
echo
echo
cd $linux
git checkout master
git pull origin master
cd $chat
git checkout master
git pull origin master
cd $linux
if grep -q -w $workid "$linuxjobber" "$chatscrum"; then
  clear
  echo "#############################" > live.txt
  echo "       LIVE ENVIRONMENT" >> live.txt
  echo "#############################" >> live.txt
  echo "Workid $workid is present" >> live.txt
  cd $linux 
#  echo " commit Date and Time is" >> live.txt
#  git log -1 --format=%cd --date=local --grep=$workid >> live.txt
#  cd $chat
#  git log -1 --format=%cd --date=local --grep=$workid >> $linux/live.txt
  cat $linux/live.txt
else
	
   clear
   echo "##########################" > live.txt
   echo "      LIVE ENVIRONMENT" >> live.txt
   echo "##########################" >> live.txt
   echo "Workid $workid not found" >> live.txt
   #cat $linux/live.txt
fi
clear
cat $linux/int.txt
echo
cat $linux/stage.txt
echo
cat $linux/live.txt
echo
echo
