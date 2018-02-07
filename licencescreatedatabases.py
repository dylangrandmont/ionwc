# Copyright (C) 2016-2018, Dylan Grandmont

import os
import numpy as np

import drilling
from utilities import writeAugmentedLicenceFile
from constants import UNKNOWN, IONWC_HOME

def augmentLicencesToDrilling(spuds, licences, augmentedLicsAll):
  """ Augment the Drilling (spuds) database with licensing information """
  nsuccess = 0
  nskips = 0

  for lic in licences:
     lic[2] = lic[2].replace(' ','').lstrip('0').replace('\xa0','') 

  licencesList = list(licences[:,2])

  for spud in spuds:
     licensee = spud[0]
     wellname = spud[1]
     uwi = spud[3]
     drilldate = spud[4]
     drilldatemonth = spud[5]
     contract = spud[6]
     rig = spud[7]
     lat = spud[8]
     lng = spud[9]
     province = spud[10]
     licnum = spud[2].replace(' ','').lstrip('0').replace('\xa0','')
     try:
        index = licencesList.index(licnum)

        entry = licences[index]
        licensee = entry[0]
        #wellname=entry[1]
        #licnum  =entry[2]
        #uwi     =entry[3]
        licdate = entry[4]
        field = entry[6]
        zone = entry[7]
        orient = entry[8]
        sub = entry[9]
        subcode = entry[10]
        lat = entry[11]
        lng = entry[12]
        writeAugmentedLicenceFile(augmentedLicsAll, licensee, wellname, licnum, uwi, drilldate, drilldatemonth,
                              contract, rig, licdate, field, zone, orient, sub, subcode, lat, lng, province)
        nsuccess+=1

     except:
        licdate, field, zone, orient, sub = "", UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN
        subcode = '4'
        writeAugmentedLicenceFile(augmentedLicsAll, licensee, wellname, licnum, uwi, drilldate, drilldatemonth,
                              contract, rig, licdate, field, zone, orient, sub, subcode, lat, lng, province)
        nskips+=1

  print "INFO: Skipped Augmenting Licensing Info for ", nskips, " entries out of a total of ", nsuccess

def run():
  drillingFileAll = open(IONWC_HOME + '/dbs/spuddb.csv','w')
  drillingFileAll.write("Licensee,Well Name,License Number,UWI,Date,DateMonth,Contractor,Rig,latitude,longitude,province\n")

  drilling.add_bc_drilling_to_database(drillingFileAll)
  drilling.add_ab_drilling_to_database(drillingFileAll)
  drilling.add_sk_drilling_to_database(drillingFileAll)
  drilling.add_mb_drilling_to_database(drillingFileAll)

  drillingFileAll.close()

  spuds = np.genfromtxt(IONWC_HOME + '/dbs/spuddb.csv', delimiter=",",dtype=None,invalid_raise=False,skiprows=1,comments=None)
  lics = np.genfromtxt(IONWC_HOME + '/dbs/licenceDBAll.csv', delimiter=",",dtype=None,invalid_raise=False,comments=None)

  augmentedLicencesAll = open(IONWC_HOME + '/dbs/AUGlicdb.csv','w')
  augmentedLicencesAll.write("Licensee,Well Name,License Number,UWI,DrillDate,DrillDateMonth,Contractor,Rig,LicenseDate,Field/Pool,TerminatingZone,Orientation,Substance,SubstanceCode,latitude,longitude,province\n")

  augmentLicencesToDrilling(spuds, lics, augmentedLicencesAll)