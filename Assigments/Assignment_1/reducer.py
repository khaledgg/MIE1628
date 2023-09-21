#!/usr/bin/env python3

import sys

total_count = 0

for line in sys.stdin:
    _, count = line.split('\t', 1)
    total_count += int(count)

print('%s\t%s' % ("line", total_count))

#C:\Users\Khaled\Documents\University\Years\Masters\MIE1628\Assigments\Assignment_1\shakespeare.txt
"""
hadoop jar C:\hadoop-3.3.0\share\hadoop\tools\lib\hadoop-streaming-3.3.0.jar -file C:\Users\Khaled\Documents\University\Years\Masters\MIE1628\Assigments\Assignment_1\mapper.py -mapper "C:\Users\Khaled\AppData\Local\Microsoft\WindowsApps\python3.exe C:\Users\Khaled\Documents\University\Years\Masters\MIE1628\Assigments\Assignment_1\mapper.py" -file C:\Users\Khaled\Documents\University\Years\Masters\MIE1628\Assigments\Assignment_1\reducer.py -reducer "C:\Users\Khaled\AppData\Local\Microsoft\WindowsApps\python3.exe C:\Users\Khaled\Documents\University\Years\Masters\MIE1628\Assigments\Assignment_1\reducer.py" -input inputtext -output wordcount   

"""