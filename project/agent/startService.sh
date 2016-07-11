#!/bin/bash

echo "----------------------------------------------------------------"
echo "|		                 WSO2 IOT Sample				          "
echo "|		                      Agent				              "
echo "|	                     ----------------				          "
echo "|                ....initializing startup-script	              "
echo "----------------------------------------------------------------"

currentDir=$PWD

for f in ./deviceConfig.properties; do
    ## Check if the glob gets expanded to existing files.
    ## If not, f here will be exactly the pattern above
    ## and the exists test will evaluate to false.
    if [ -e "$f" ]; then
    	echo "Configuration file found......"
    else
    	echo "'deviceConfig.properties' file does not exist in current path. \nExiting installation...";
    	exit;
    fi
    ## This is all we needed to know, so we can break after the first iteration
    break
done

#install mqtt dependency
git clone git://git.eclipse.org/gitroot/paho/org.eclipse.paho.mqtt.python.git
cd org.eclipse.paho.mqtt.python
sudo python setup.py install

cd $currentDir

#while true; do
read -p "Whats the time-interval (in seconds) between successive Data-Pushes to the WSO2-DC (ex: '60' indicates 1 minute) > " input
if [ $input -eq $input 2>/dev/null ]
then
   echo "Setting data-push interval to $input seconds."
else
   echo "Input needs to be an integer indicating the number seconds between successive data-pushes. 15 will be taken as default value"
   $input=15
fi
#done
cp deviceConfig.properties ./src
chmod +x ./src/agent.py
./src/agent.py -i $input

if [ $? -ne 0 ]; then
	echo "Could not start the service..."
	exit;
fi

echo "--------------------------------------------------------------------------"
echo "|			Successfully Started		"
echo "|		   --------------------------	"
