import sys 
sys.path.append('../')  # for config module

import config
import json

from datetime import datetime

from model import *

import csv

print(config.API_VERSION)

with open('../../datafiles/blacklist.csv', newline='', encoding = "ISO-8859-1") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        print(', '.join(row)) # address,addressType,status,reason

        blacklist = Blacklist(userId=ObjectId('5d75c245daf67e862aabb904'), address=row[0], currency=row[1], status=row[2]=='1', reason=row[3])
        # blacklist.save()