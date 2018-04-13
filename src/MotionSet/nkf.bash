#!/bin/bash
cd /home/pi/Program/servo/parameter/
nkf -Lu --overwrite *.csv
cd ./Ahead/
nkf -Lu --overwrite *.csv

