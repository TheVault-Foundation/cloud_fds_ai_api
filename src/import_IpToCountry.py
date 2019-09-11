import sys
import csv
import time

from mongoengine import connect
from mongoengine.connection import _get_db

from models import IpToCountry, IpToCountryTmp

def importFile(filePath):
    f = open(filePath, "r", encoding = "ISO-8859-1")

    db = _get_db()
    if 'ipToCountry_tmp' in db.collection_names(False):
        db.drop_collection('ipToCountry_tmp')

    i = 0
    for line in f:
        if line[0] == '#':
            continue

        r = list(csv.reader([line]) )[0]
        
        doc = IpToCountryTmp(
                    ipFrom = int(r[0]),
                    ipTo = int(r[1]),
                    registry = r[2],
                    assigned = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(r[3]))),
                    ctry = r[4],
                    cntry = r[5],
                    country = r[6],
        )

        doc.save()

        # if i==10:
        #     break
        # i += 1

    f.close()
    
    if 'ipToCountry_bak' in db.collection_names(False):
        db.drop_collection('ipToCountry_bak')
    if 'ipToCountry' in db.collection_names(False):
        db["ipToCountry"].rename("ipToCountry_bak")
    db["ipToCountry_tmp"].rename("ipToCountry")



if __name__ == "__main__":
    if len(sys.argv) == 2:
        importFile(sys.argv[1])
    else:
        print("Usage import_file.py data_file")
