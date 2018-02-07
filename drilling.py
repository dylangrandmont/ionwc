# Copyright (C) 2016, Eye on Western Canada
#
# 

import os
import re
import sys
import math
import random
import datetime
import csv
import numpy as np

from coordinatemapping import uwiToLatLng
from utilities import writeDrillingFile
from constants import UNKNOWN, IONWC_HOME, MONTH_DICT, BC_WELL_NAME_TO_OPERATOR_MAP, MB_WELL_NAME_TO_OPERATOR_MAP


def add_bc_drilling_to_database(drillingFileAll, verbose = False):
    """ Query for all BC well spuds, parse them into a common format and add to database (csv) """
    files = []
    province = "BC"

    for (dirpath, dirnames, filenames) in os.walk(IONWC_HOME + '/data/spud/bc/'):
        files.extend(filenames)
        break

    for file in files:
        file_contents = ''.join(open(IONWC_HOME + '/data/spud/bc/' + file).readlines())
        spuds = re.findall('[0-9]+.+[\s]+[0-9]+[A-Z]+[0-9]+[\s]+[\w]+[\s]+[a-zA-z]+[\s]+[0-9]+', file_contents)
        for spud in spuds:
            licence_number = re.findall('[0-9]+\s+', spud)[0]
            well_name = re.split('[0-9]+[A-Z]+[0-9]+', spud)[0].replace(licence_number, '')

            #Create Licensee name using the well name
            licencee = UNKNOWN
            for key in BC_WELL_NAME_TO_OPERATOR_MAP:
                if key in well_name.lower():
                    licencee = BC_WELL_NAME_TO_OPERATOR_MAP[key]

            try:
                uwi = re.findall('[0-9]+[A-Z][0-9]+[A-Z][0-9]+[A-Z][0-9]+', spud)[0]
                lat, lon = uwiToLatLng.convert(uwi, grid = "NTS")
            except:
                uwi = re.findall('[0-9]+W[0-9]+', spud)[0]
                uwi = "00/" + uwi[3:5] + "-" + uwi[5:7] + "-" + uwi[7:10] + "-" + uwi[10:14] + "/0"     
                lat, lon = uwiToLatLng.convert(uwi)

            drill_date = re.findall('[0-9]{4}[A-Z]{3}[0-9]+', spud)[0]
            year = drill_date[0:4]
            month = MONTH_DICT[drill_date[4:7]]
            day = drill_date[7:9]

            driller = re.findall('[a-zA-Z]+', spud)[-1]
            rig = re.findall('[0-9]+', spud)[-1]

            random.seed( int(re.sub('[^0-9]', '', licence_number)) )
            lat += random.uniform(-0.0005, 0.0005)
            lon += random.uniform(-0.0005, 0.0005)

            writeDrillingFile(drillingFileAll, licencee, well_name, licence_number, uwi, year, month, day, driller, rig, lat, lon, province)


def _aer_parse_spud_file(file): 
    """ Open Spud file and return array of data """
    spud = []         
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
            spud.append(Well)
    return spud

def add_ab_drilling_to_database(drillingFileAll, verbose = False):
  """ Query for all AB well spuds, parse them into a common format and add to database (csv) """
  province = "AB"

  for year in range(2011, datetime.datetime.now().year + 1):
      files = []
      for (dirpath, dirnames, filenames) in os.walk(IONWC_HOME + '/data/spud/' + str(year) + '/'):
          files.extend(filenames)
          break
      
      for file in files:
          wells = _aer_parse_spud_file(IONWC_HOME + '/data/spud/' + str(year) + '/' + file)
          if verbose: print 'INFO:  Reading file ' + IONWC_HOME + '/data/spud/' + str(year) + '/' + file
          for i in range(len(wells)):
              try:
                  uwi = wells[i][0]
                  lat, lon = uwiToLatLng.convert(uwi)
                  licencee = wells[i][9].replace(',','')
                  well_name = wells[i][1].replace(',','')
                  licence_number   = wells[i][2]
                  uwi      = wells[i][0]
                  driller  = wells[i][4].replace(',','')
                  rig      = wells[i][5]
                  month = file[-8:-6]
                  day   = file[-6:-4]

                  random.seed(int(re.sub("[^0-9]","",licence_number)))
                  lat += random.uniform(-0.0005,0.0005)
                  lon += random.uniform(-0.0005,0.0005)

                  writeDrillingFile(drillingFileAll, licencee, well_name, licence_number, uwi, str(year), month, day, driller, rig, lat, lon, province)
              except:
                  print "WARN: skipping AER spud of well", wells[i]

def _sk_parse_spud_file(file):
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

def add_sk_drilling_to_database(drillingFileAll, verbose = False):
    """ Query for all SK well spuds, parse them into a common format and add to database (csv) """
    files = []
    province = "SK"
    for (dirpath, dirnames, filenames) in os.walk(IONWC_HOME + '/data/spud/sask/'):
        files.extend(filenames)
        break

    well_name = UNKNOWN
    rig = UNKNOWN

    for file in files:
        if verbose: print 'INFO:  Reading file ' + IONWC_HOME + '/data/spud/sask/' + file

        descript, surfuwi = _sk_parse_spud_file(IONWC_HOME + '/data/spud/sask/' + file)

        for i in range(len(surfuwi)):
            try:
                uwi = surfuwi[i]
                lat, lon = uwiToLatLng.convert("00/"+ uwi +"/0")
                licencee = descript[i][14][1:-1].replace(',','')
                licence_number = descript[i][12][1:-1]
                uwi = descript[i][1][1:-1]
                driller = descript[i][16][1:-1].replace(',','')
                year = file[-14:-10]
                month = file[-9:-7]
                day  = file[-6:-4]

                random.seed(int(re.sub("[^0-9]","",licence_number)))
                lat += random.uniform(-0.0005,0.0005)
                lon += random.uniform(-0.0005,0.0005)

                writeDrillingFile(drillingFileAll, licencee, well_name, licence_number, uwi, year, month, day, driller, rig, lat, lon, province)

            except: 
                print 'WARN: Skipping SK spud of well uwi ', uwi, ' description: ', descript[i]

def add_mb_drilling_to_database(drillingFileAll, verbose = False):
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
                licence_number, well_name, licencee, uwi, driller = "", "", UNKNOWN, "", UNKNOWN
                licence_number = well[0].strip().split(' ')[0]

                well_name = well[0].strip().replace(licence_number,'').strip()
                try:
                    indexLicensee = [i for i, s in enumerate(well) if 'Licensee' in s][0]
                    licencee = well[indexLicensee].strip().split(':')[1].strip()
                except: 
                    #Create Licensee name using the well name
                    for key in MB_WELL_NAME_TO_OPERATOR_MAP:
                        if key in well_name.lower():
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

                random.seed(int(re.sub("[^0-9]","",licence_number)))
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

                    try: float(licence_number)
                    except: print "ERROR: Non numerical licence number found"

                    mb_wells += 1
                    writeDrillingFile(drillingFileAll, licencee, well_name, 'MB' + licence_number, uwi, year, month, day, driller, rig, lat, lon, province)

    print "INFO: Number of well spuds in Manitoba: ", mb_wells
