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
from constants import MONTH_DICT, MB_WELL_NAME_TO_OPERATOR_MAP, UNKNOWN, IONWC_HOME

def addMBDrillingToDataBase(drillingFileAll, verbose = False):
  """ Query for all MB well spuds, parse them into a common format and add to database (csv) """
  files = []
  province = "MB"

  for (dirpath, dirnames, filenames) in os.walk(IONWC_HOME + '/data/activity/mb/'):
      files.extend(filenames)
      break

  mb_wells = 0

  for file in files:
      fi = open(IONWC_HOME + '/data/activity/mb/' + file)
      if verbose: print 'INFO:  Reading file ' + IONWC_HOME + '/data/activity/mb/' + file
      t = fi.read()
      t1 = t.split('Lic. No.:')
      wells = t1[1:]
      rig = UNKNOWN

      for well in wells:
          if 'spud date:' in well.lower():
              well = well.split('\n')
              licnum, wellname, licencee, uwi, driller = "", "", UNKNOWN, "", UNKNOWN
              licnum = well[0].strip().split(' ')[0]

              wellname = well[0].strip().replace(licnum,'').strip()
              try:
                  indexLicensee = [i for i, s in enumerate(well) if 'Licensee' in s][0]
                  licencee = well[indexLicensee].strip().split(':')[1].strip()
              except: 
                  #Create Licensee name using the well name
                  for key in MB_WELL_NAME_TO_OPERATOR_MAP:
                    if key in wellname.lower():
                      licencee = MB_WELL_NAME_TO_OPERATOR_MAP[key]
                  if licencee == UNKNOWN:
                    print "WARN: No Operator found for MB drilling well ", well

              try:
                  indexUWI = [i for i, s in enumerate(well) if 'UWI' in s][0]
                  uwi = well[indexUWI].strip().split(':')[1][0:22].strip()
              except:
                  print "WARN:  Assuming UWI is at second index"
                  uwi = well[1].strip()[0:22]
                  pass
              uwi = uwi.replace('.','/')
              lat, lon = uwiToLatLng.convert(uwi)

              random.seed(int(re.sub("[^0-9]","",licnum)))
              lat += random.uniform(-0.0005,0.0005)
              lon += random.uniform(-0.0005,0.0005)

              print well
              indexDate = [i for i, s in enumerate(well) if 'spud date:' in s.lower()][0]
              date = well[indexDate].strip().split(':')[1].strip().split('-')
              year = date[2]
              if int(year)>=2010:
                  month = date[1]
                  month = MONTH_DICT[month.upper()]
                  day = date[0]

                  try:
                      indexField = [i for i, s in enumerate(well) if 'Field' in s][0]
                      field = well[indexField].strip().split(':')[1].strip()
                  except: pass

                  try:
                      indexDriller = [i for i, s in enumerate(well) if 'Contractor' in s][0]
                      driller = well[indexDriller].strip().split(':')[1].strip()
                  except: pass

                  try: float(licnum)
                  except: print "ERROR: Non numerical licence number found"

                  mb_wells += 1
                  writeDrillingFile(drillingFileAll, licencee, wellname, 'MB' + licnum, uwi, year, month, day, driller, rig, lat, lon, province)

  print "INFO: Number of well spuds in Manitoba: ", mb_wells
