# Copyright (C) 2016, Eye on Western Canada
#
# 

import os
import re
import sys
import math
import random
import csv
import numpy as np

from coordinatemapping import uwiToLatLng
from utilities import writeDrillingFile
from constants import UNKNOWN, IONWC_HOME

def skParseSpudFile(file):
    """ parse SASK drilling report """
    lines = open(file).read().splitlines()
    lines = lines[1:]
    descript, surfuwi = [], []

    for line in lines:
        try:
            line = line.split(",")
            uwi = line[1][1:-1]
            surfuwi.append(uwi)
            descript.append(line)
        except:
            print 'ERROR: Skipping SK spud line of ', line

    return descript, surfuwi

def addSKDrillingToDataBase(drillingFileAll, verbose = False):
  """ Query for all SK well spuds, parse them into a common format and add to database (csv) """
  files = []
  province = "SK"
  for (dirpath, dirnames, filenames) in os.walk(IONWC_HOME + '/data/spud/sask/'):
    files.extend(filenames)
    break

  wellname = UNKNOWN
  rig = UNKNOWN

  for file in files:
    if verbose: print 'INFO:  Reading file ' + IONWC_HOME + '/data/spud/sask/' + file
    descript, surfuwi = skParseSpudFile(IONWC_HOME + '/data/spud/sask/' + file)

    for i in range(len(surfuwi)):
      try:
        uwi = surfuwi[i]
        lat,lon = uwiToLatLng.convert("00/"+ uwi +"/0")
        licencee = descript[i][14][1:-1].replace(',','')
        licnum = descript[i][12][1:-1]
        uwi = descript[i][1][1:-1]
        driller = descript[i][16][1:-1].replace(',','')
        year = file[-14:-10]
        month = file[-9:-7]
        day  = file[-6:-4]

        random.seed(int(re.sub("[^0-9]","",licnum)))
        lat += random.uniform(-0.0005,0.0005)
        lon += random.uniform(-0.0005,0.0005)

        writeDrillingFile(drillingFileAll, licencee, wellname, licnum, uwi, year, month, day, driller, rig, lat, lon, province)

      except: 
        print 'WARN: Skipping SK spud of well uwi ', uwi, ' description: ', descript[i]

