import os
import re
import sys
import math
import random
import csv
import numpy as np

from coordinatemapping import uwiToLatLng
from utilities import getSubCode, conformSub, conformBCOGCLatLon, writeLicenseFile, writeDrillingFile
from constants import UNKNOWN

IONWC_HOME = os.environ["IONWC_HOME"]

def conform_uwi(uwi):
    if "/" in uwi:
        grid = "NTS"
    else:
        grid = "DLS"

    if grid=="NTS":
        uwi = "200" + uwi.replace("/", "").replace("-", "") + "00"
    else:
        uwi = uwi.split("-")
        uwi = "00/" + uwi[0] + '-' + uwi[1] + '-' + uwi[2] + "W6/0"

    return uwi

def addBCFacilitiesToDataBase(facilitiesFileAll):
    """ Query for all BC facilities, parse them into a common format and add to database (csv) """
    bcfacilties = 0

    allBCLics = open(IONWC_HOME + "/data/facilities/bc/facilities.csv")
    reader = csv.reader(allBCLics)

    # Skip header (first row)
    next(reader)

    for row in reader:
        facilityId = row[1]
        facilityType = row[2]
        objectType = row[3]
        activity = row[4]
        organization = row[5]
        location = row[6]     # B-023-E/094-A-14 --> 200B077D094H0300  or 06-06-086-13
        approvalDate = row[7]
        constructionStartDate = row[8]
        pressureTestDate = row[9]
        leaveToOpenDate = row[10]
        asBuiltDate = row[11]
        tenureFileNumber = row[12]
        legalSurveyApprovalDate = row[13]
        facilityStatus = row[14]

        uwi = conform_uwi(location)
                       
        lat, lon = uwiToLatLng.convert(uwi)                                                                          
        random.seed(int(re.sub("[^0-9]","", facilityId)))
        lat += random.uniform(-0.0005,0.0005)
        lon += random.uniform(-0.0005,0.0005)

        writeFaciltiesFile(facilitiesFileAll, facilityId, facilityType, organization, lat, lng)
        bcfacilties += 1                                                                                                 
                                                                                        
    print "INFO:  Found", bcfacilties, " facilities for BC"   
