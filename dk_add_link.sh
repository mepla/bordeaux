#!/bin/bash

SCRIPT_PATH=/home/mepla/projects/bordeaux/dk_link_manager.py
source /home/mepla/projects/virtualenvs/bordeaux/bin/activate

python "$SCRIPT_PATH" "$@"

read -p "Do you want to run bordeaux now? (Y/n)" yn
yn=${yn:-y}
if [ $yn == 'n' ] || [ $yn == 'N' ]; then
    exit 0
else
    bordeaux
fi