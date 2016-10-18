#!/bin/bash

VERBOSE=false
REPORT=false

while [[ $# -gt 0 ]]
do
    key="$1"

	case $key in
    	-v|--verbose)
    		VERBOSE=true
    		shift # past argument
   		;;
    	-r|--report)
    		REPORT=true
    		shift # past argument
   		;;

    	*)
		;;
	esac
done

SCRIPT_PATH=/home/mepla/projects/bordeaux/main.py
source /home/mepla/projects/virtualenvs/bordeaux/bin/activate

if [ $VERBOSE = true ];
then
	python "$SCRIPT_PATH" >> /var/log/bordeaux.log 2>&1
	tail -n 20 /var/log/bordeaux.log
else
    if [ $VERBOSE = true ];
    then
	    python "$SCRIPT_PATH" -r >> /var/log/bordeaux.log 2>&1
	fi
fi
