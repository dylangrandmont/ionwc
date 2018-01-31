# Copyright (C) 2016, Eye on Western Canada
#
# 

import os
import re
import random

from coordinatemapping import uwiToLatLng
from utilities import writeDrillingFile
from constants import UNKNOWN, IONWC_HOME

def aerParseSpudFile(file): 
    """ Open Spud file and return array of data """
    out = []         
    inf = open(file)
    lines = inf.readlines()
    if lines != []:
        lines = filter(lambda x: not re.match(r'^\s*$', x), lines)
        inf.close()
        
        #Determine from the header which columns contain what data
        header = lines[5].split()
        headsp = [[0,len(header[0])]]
        for i in range(1, len(header)): headsp.append([1+headsp[i-1][1], 1+headsp[i-1][1] + len(header[i])])
        
        #Break apart string of data for each well based on header columns 
        nwells = int(lines[-2].split()[-1])

        for i in range(nwells):
            well = lines[6+i]
            Well = []
            for j in headsp: 
                Well.append(well[j[0]:j[1]])      
            out.append(Well)
    return out

def addABDrillingToDataBase(drillingFileAll, verbose = False):
  """ Query for all AB well spuds, parse them into a common format and add to database (csv) """
  province = "AB"

  for year in ['2017', '2016','2015','2014','2013','2012','2011']:
      files = []
      for (dirpath, dirnames, filenames) in os.walk(IONWC_HOME + '/data/spud/' + year + '/'):
          files.extend(filenames)
          break
      
      for file in files:
          wells = aerParseSpudFile(IONWC_HOME + '/data/spud/' + year + '/' + file)
          if verbose: print 'INFO:  Reading file ' + IONWC_HOME + '/data/spud/' + year + '/' + file
          for i in range(len(wells)):
              try:
                  uwi=wells[i][0]
                  lat,lon = uwiToLatLng.convert(uwi)
                  licencee = wells[i][9].replace(',','')
                  wellname = wells[i][1].replace(',','')
                  licnum   = wells[i][2]
                  uwi      = wells[i][0]
                  driller  = wells[i][4].replace(',','')
                  rig      = wells[i][5]
                  month = file[-8:-6]
                  day   = file[-6:-4]

                  random.seed(int(re.sub("[^0-9]","",licnum)))
                  lat += random.uniform(-0.0005,0.0005)
                  lon += random.uniform(-0.0005,0.0005)

                  writeDrillingFile(drillingFileAll, licencee, wellname, licnum, uwi, year, month, day, driller, rig, lat, lon, province)
              except:
                  print "WARN: skipping AER spud of well", wells[i]

