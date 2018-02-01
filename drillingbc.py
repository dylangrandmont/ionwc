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
from utilities import conformBCOGCLatLon, writeDrillingFile
from utilities import writeAugmentedLicenceFile
from constants import MONTH_DICT, BC_WELL_NAME_TO_OPERATOR_MAP, UNKNOWN, IONWC_HOME

def addBCDrillingToDataBase(drillingFileAll, verbose = False):
  """ Query for all BC well spuds, parse them into a common format and add to database (csv) """
  files = []
  province = "BC"

  for (dirpath, dirnames, filenames) in os.walk(IONWC_HOME + '/data/spud/bc/'):
      files.extend(filenames)
      break

  for file in files:
    fileContents = ''.join(open(IONWC_HOME + '/data/spud/bc/' + file).readlines())
    spuds = re.findall('[0-9]+.+[\s]+[0-9]+[A-Z]+[0-9]+[\s]+[\w]+[\s]+[a-zA-z]+[\s]+[0-9]+', fileContents)
    for spud in spuds:
      licnum = re.findall('[0-9]+\s+', spud)[0]
      wellname = re.split('[0-9]+[A-Z]+[0-9]+', spud)[0].replace(licnum, '')

      #Create Licensee name using the well name
      licencee = UNKNOWN
      for key in BC_WELL_NAME_TO_OPERATOR_MAP:
        if key in wellname.lower():
          licencee = BC_WELL_NAME_TO_OPERATOR_MAP[key]

      try:
        uwi = re.findall('[0-9]+[A-Z][0-9]+[A-Z][0-9]+[A-Z][0-9]+', spud)[0]
        lat, lon = uwiToLatLng.convert(uwi, grid = "NTS")
      except:
        uwi = re.findall('[0-9]+W[0-9]+', spud)[0]
        uwi = "00/" + uwi[3:5] + "-" + uwi[5:7] + "-" + uwi[7:10] + "-" + uwi[10:14] + "/0"     
        lat, lon = uwiToLatLng.convert(uwi)

      drillDate = re.findall('[0-9]{4}[A-Z]{3}[0-9]+', spud)[0]
      year = drillDate[0:4]
      month = MONTH_DICT[drillDate[4:7]]
      day = drillDate[7:9]

      driller = re.findall('[a-zA-Z]+', spud)[-1]
      rig = re.findall('[0-9]+', spud)[-1]

      random.seed( int(re.sub('[^0-9]', '', licnum)) )
      lat += random.uniform(-0.0005, 0.0005)
      lon += random.uniform(-0.0005, 0.0005)

      writeDrillingFile(drillingFileAll, licencee, wellname, licnum, uwi, year, month, day, driller, rig, lat, lon, province)
