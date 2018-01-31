#!/bin/bash

##################################################################
# Copyright (C) 2016, Eye on Western Canada
#
# Methods for parsing BC land postings
#
##################################################################

import re
import numpy as np
import glob

from coordinatemapping import uwiToLatLng
from constants import MONTH_DICT, FORMATION_AGE_DICT, BCPostingDatesToSaleDateMap, KML_TEMPLATE
from constants import IONWC_HOME
from utilities import writePostingResultDataBaseFile, writePostingResultAggregateDataBaseFile

PROVINCE = 'BC'

PAGE_HEADER_STRING = 'PAGE\s+[0-9]+.+\nDRILLING LICENCE.+\n.+\n.+\n.+\n.+'
TRACT_STRING = 'TRACT\s+[0-9]+'
TRACT_1_STRING = '([0-9]+\s+TRACT\s+1\s+[0-9]+)'

def findZoneRights(tract):
  if len(re.findall('BELOW BASE OF', tract)) != 0:
    zoneRights = re.findall('BELOW BASE OF [0-9].+', tract)[0].strip()
    topQualifier = 'From The Base Of The'    
    topZone = re.split(' [(].+', re.split('BELOW BASE OF [0-9]+ ', zoneRights)[1])[0]
    baseQualifier = 'To'
    baseZone = 'Basement'

  elif len(re.findall('ALL ZONES', tract)) != 0:
    topQualifier = 'From'
    topZone = 'Surface'
    baseQualifier = 'To'
    baseZone = 'Basement'

  elif len(re.findall('IN\s+[0-9]+\s+[A-Z]+', tract)) != 0:
    topQualifier = 'From The Top Of The'
    topZone = re.findall('IN\s+[0-9]+\s+[A-Z]+', tract)[0].split()[-1]
    baseQualifier = 'To The Base Of The'
    baseZone = topZone

  elif len(re.findall('DOWN TO BASE OF.+', tract)) != 0:
    zoneRights = re.findall('DOWN TO BASE OF.+', tract)[0].strip()
    topQualifier = 'From'
    topZone = 'Surface'
    baseQualifier = 'To The Base Of The'
    baseZone = re.split(' [(].+', re.split('DOWN TO BASE OF [0-9]+ ', zoneRights)[1])[0]

  else:
    raise Exception('No subsurface rights found for tract', tract)

  topZone = topZone.title()
  baseZone = baseZone.title()
  return topQualifier, topZone, baseQualifier, baseZone

def postingUWIToKmlPolygon(uwi, grid='dls'):

  if grid == 'dls':
    sec = uwi[0]
    sec = ("%02d" % int(''.join(re.findall('[0-9]+', sec)))) + ''.join(re.findall('[A-Z]+', sec))
    sec = sec.strip()
    twp = uwi[1]
    rng = uwi[2]
    mer = uwi[3]

    if 'NE' in sec: 
      se_uwi = '09' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      sw_uwi = '10' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      nw_uwi = '15' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      ne_uwi = '16' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
    elif 'NW' in sec: 
      se_uwi = '11' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      sw_uwi = '12' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      nw_uwi = '13' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      ne_uwi = '14' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
    elif 'SE' in sec: 
      se_uwi = '01' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      sw_uwi = '02' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      nw_uwi = '07' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      ne_uwi = '08' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
    elif 'SW' in sec: 
      se_uwi = '03' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      sw_uwi = '04' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      nw_uwi = '05' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      ne_uwi = '06' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
    elif (len(sec) == 3) and (sec[2] == 'N'):
      se_uwi = '09' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      sw_uwi = '12' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      nw_uwi = '13' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      ne_uwi = '16' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
    elif (len(sec) == 3) and (sec[2] == 'E'):
      se_uwi = '01' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      sw_uwi = '02' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      nw_uwi = '15' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      ne_uwi = '16' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
    elif (len(sec) == 3) and (sec[2] == 'W'):
      se_uwi = '03' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      sw_uwi = '04' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      nw_uwi = '13' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      ne_uwi = '14' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
    elif (len(sec) == 3) and (sec[2] == 'S'):
      se_uwi = '01' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      sw_uwi = '04' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      nw_uwi = '05' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      ne_uwi = '08' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer

    elif sec.isdigit(): 
      se_uwi = '01' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      sw_uwi = '04' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      nw_uwi = '13' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      ne_uwi = '16' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
    else:
      print "ERROR: invalid section used ", sec, twp, rng, mer
      sec = re.findall(r'\d+', sec)[0]
      se_uwi = '01' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      sw_uwi = '04' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      nw_uwi = '13' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer
      ne_uwi = '16' + '-' + sec[0:2] + '-' + twp + '-' + rng + 'W' + mer

    se_lat, se_lng = uwiToLatLng.convert(se_uwi, position = "se")
    sw_lat, sw_lng = uwiToLatLng.convert(sw_uwi, position = "sw")
    nw_lat, nw_lng = uwiToLatLng.convert(nw_uwi, position = "nw")
    ne_lat, ne_lng = uwiToLatLng.convert(ne_uwi, position = "ne")

  elif grid == 'nts':

    if ("F" in uwi[0]):
      print "ERROR: unsupported uwi found: ", uwi
      uwi[0] = uwi[0].replace("F", "")

    unit = str("%03d" % int(uwi[0]))
    block = uwi[1]
    series = uwi[2]
    sheetLetter = uwi[3]
    sheetNumber = uwi[4]

    se_uwi = '100A' + unit + block + series + sheetLetter + sheetNumber + '00'
    sw_uwi = '100B' + unit + block + series + sheetLetter + sheetNumber + '00'
    nw_uwi = '100C' + unit + block + series + sheetLetter + sheetNumber + '00'
    ne_uwi = '100D' + unit + block + series + sheetLetter + sheetNumber + '00'

    se_lat, se_lng = uwiToLatLng.convert(se_uwi, position = "se", grid = "NTS")
    sw_lat, sw_lng = uwiToLatLng.convert(sw_uwi, position = "sw", grid = "NTS")
    nw_lat, nw_lng = uwiToLatLng.convert(nw_uwi, position = "nw", grid = "NTS")
    ne_lat, ne_lng = uwiToLatLng.convert(ne_uwi, position = "ne", grid = "NTS")

  kmlPolygon = KML_TEMPLATE % (se_lng, se_lat, sw_lng, sw_lat, nw_lng, nw_lat, ne_lng, ne_lat)

  centerLatitude = (se_lat + nw_lat) / 2.0
  centerLongitude = (se_lng + nw_lng) / 2.0

  return kmlPolygon, centerLatitude, centerLongitude

def addBCOfferingsToDataBase(ponDataBaseFile, ponAggregateDataBaseFile):
  bcOfferingFiles = glob.glob(IONWC_HOME + '/data/postings/bc/*sal.rpt')

  for bcOfferingFile in bcOfferingFiles:
    assert len(bcOfferingFiles[0].split('/')[-1]) == 12

    month = MONTH_DICT[bcOfferingFile.split('/')[-1][:3].upper()]
    year = bcOfferingFile.split('/')[-1][3:5]
    saleDate = '20' + year + '.' + month
    saleDate = BCPostingDatesToSaleDateMap[saleDate]

    lines = open(bcOfferingFile).readlines()
    allLines = ''.join(lines)
    allLines = re.sub(PAGE_HEADER_STRING, '', allLines)

    licenceIndexEnd = allLines.find('PETROLEUM AND NATURAL GAS LEASE')
    allLicences = allLines[0:licenceIndexEnd]
    allLeases = allLines[licenceIndexEnd:]

    contractType = "Licence"
    for parcels in [allLicences, allLeases]:
      allParcels = re.compile(TRACT_1_STRING).split(parcels)
      del allParcels[0]
      parcelHeaders = allParcels[0::2]
      parcelContents = allParcels[1::2]

      index = 0
      for parcelContent in parcelContents:
        parcelNumber = re.split('\s+', parcelHeaders[index])[0]
        hectares = re.split('\s+', parcelHeaders[index])[3]

        aggregateLatitudes = []
        aggregateLongitudes = []

        tracts = re.split(TRACT_STRING, parcelContent)
        tractNo = 1
        for tract in tracts:
          topQualifier, topZone, baseQualifier, baseZone = findZoneRights(tract)
          try:
            topAge = FORMATION_AGE_DICT[topZone.lower().strip()]
          except:
            raise Exception('No entry found in FORMATION_AGE_DICT for ' + topZone)
          try:
            baseAge = FORMATION_AGE_DICT[baseZone.lower().strip()]
          except:
            raise Exception('No entry found in FORMATION_AGE_DICT for ' + baseZone) 

          dlsUWIs = re.findall('TWP .+', tract)
          ntsUWIs = re.findall('NTS .[0-9]+.+', tract)
          multigeometryContents = ""
          for uwi in dlsUWIs:
            uwi = uwi.strip()
            uwiSplit = uwi.split()
            mer = '6'
            twp = uwiSplit[1]
            rng = uwiSplit[3]
            secs = uwiSplit[6:]

            for sec in secs:
              if '-' in sec:
                startSec = int( sec.split('-')[0] )
                endSec = int( sec.split('-')[1] )
                secRange = range(startSec, endSec + 1)
                for seci in secRange:
                  seci = str(seci)
                  kmlPolygon, centerLatitude, centerLongitude = postingUWIToKmlPolygon([seci, twp, rng, mer], grid='dls')
                  aggregateLatitudes.append(centerLatitude)
                  aggregateLongitudes.append(centerLongitude)
                  ponDataBaseFile.write(saleDate + ':' + contractType + ':' + str(parcelNumber) + ':' + hectares + ':' + str(tractNo) + ':' + uwi + ':' + topQualifier + ' ' + topZone + ':' + baseQualifier + ' ' + baseZone + ':' + str(topAge) + ':' + str(baseAge) + ':' + kmlPolygon + ':' + PROVINCE + '\n')
              else:
                kmlPolygon, centerLatitude, centerLongitude = postingUWIToKmlPolygon([sec, twp, rng, mer], grid='dls')
                aggregateLatitudes.append(centerLatitude)
                aggregateLongitudes.append(centerLongitude)
                ponDataBaseFile.write(saleDate + ':' + contractType + ':' + str(parcelNumber) + ':' + hectares + ':' + str(tractNo) + ':' + uwi + ':' + topQualifier + ' ' + topZone + ':' + baseQualifier + ' ' + baseZone + ':' + str(topAge) + ':' + str(baseAge) + ':' + kmlPolygon + ':' + PROVINCE + '\n')
               
          for uwi in ntsUWIs:
            uwi = uwi.strip()
            uwiNoUnits = re.findall(r"[A-Z]+.[0-9]+-[A-Z]-[0-9]+ BLK [A-Z] UNITS ", uwi)[0]
            units = uwi.replace(uwiNoUnits, '')
            units = units.split()

            uwiNoUnits = re.findall(r"[\w']+", uwiNoUnits)
            sheetNumber = uwiNoUnits[3]
            sheetLetter = uwiNoUnits[2]
            series = uwiNoUnits[1]
            block = uwiNoUnits[5]

            for unit in units:
              if '-' in unit:
                startUnit = int( unit.split('-')[0] )
                endUnit = int( unit.split('-')[1] )
                unitRange = range(startUnit, endUnit + 1)
                for uniti in unitRange:
                  uniti = str(uniti)
                  kmlPolygon, centerLatitude, centerLongitude = postingUWIToKmlPolygon([uniti, block, series, sheetLetter, sheetNumber], grid='nts')
                  aggregateLatitudes.append(centerLatitude)
                  aggregateLongitudes.append(centerLongitude)
                  uwi = 'Unit ' + uniti + '; Block ' + block + '; Series ' + series + '; Sheet ' + sheetLetter + sheetNumber
                  ponDataBaseFile.write(saleDate + ':' + contractType + ':' + str(parcelNumber) + ':' + hectares + ':' + str(tractNo) + ':' + uwi + ':' + topQualifier + ' ' + topZone + ':' + baseQualifier + ' ' + baseZone + ':' + str(topAge) + ':' + str(baseAge) + ':' + kmlPolygon + ':' + PROVINCE + '\n')
              else:
                kmlPolygon, centerLatitude, centerLongitude = postingUWIToKmlPolygon([unit, block, series, sheetLetter, sheetNumber], grid='nts')
                aggregateLatitudes.append(centerLatitude)
                aggregateLongitudes.append(centerLongitude)
                uwi = 'Unit ' + unit + '; Block ' + block + '; Series ' + series + '; Sheet ' + sheetLetter + sheetNumber
                ponDataBaseFile.write(saleDate + ':' + contractType + ':' + str(parcelNumber) + ':' + hectares + ':' + str(tractNo) + ':' + uwi + ':' + topQualifier + ' ' + topZone + ':' + baseQualifier + ' ' + baseZone + ':' + str(topAge) + ':' + str(baseAge) + ':' + kmlPolygon + ':' + PROVINCE + '\n')

          tractNo += 1

        aggregateLatitude = sum(aggregateLatitudes) / len(aggregateLatitudes)
        aggregateLongitude = sum(aggregateLongitudes) / len(aggregateLongitudes)
        ponAggregateDataBaseFile.write(saleDate + ':' + contractType + ':' + parcelNumber + ':' + hectares + ':' + str(aggregateLatitude) + ':' + str(aggregateLongitude) + ':' + PROVINCE + '\n')
        index += 1
      contractType = "Lease"

def addBCResultsToDataBase(psrDataBaseFile, psrAggregateDataBaseFile, ponDataBaseFile, ponAggregateDataBaseFile):
  ponDataBase = np.loadtxt(ponDataBaseFile, delimiter=':', dtype=str)
  ponAggregateDataBase = np.loadtxt(ponAggregateDataBaseFile, delimiter=':', dtype=str)

  bcResultFiles = glob.glob(IONWC_HOME + '/data/postings/bc/*res.rpt')
  for psrPostingFile in bcResultFiles:
    resultsFileContents = ''.join(open(psrPostingFile).readlines())
    results = re.findall('[a-zA-Z].+[0-9]+[\s]+[0-9]+.+[a-zA-Z].+[0-9].+\$.+', resultsFileContents)

    for result in results:
      resultDelimited = re.split('\s\s+', result)
      contractNumber = resultDelimited[1]
      hectares = resultDelimited[2]
      client = resultDelimited[3].title()
      workingInterest = resultDelimited[4]
      dollarPerHectare = resultDelimited[5]
      bonus = resultDelimited[6]

      clientDescription = client + ' ' + '%d' % float(workingInterest) + '%'

      status = ''
      if 'no bids or no acceptable bids' in re.split('\s\s+', result)[3].lower():
        status = 'No Offers'
      else:
        status = 'Accepted'

      aggregateContractIndeces = [i for i, x in enumerate(ponAggregateDataBase[:,2]) if (x==contractNumber and ponAggregateDataBase[i, 6] == PROVINCE)]
      if len(aggregateContractIndeces) == 1:
        aggregateContractIndex = aggregateContractIndeces[0]
        aggregateLatitude = ponAggregateDataBase[aggregateContractIndex][4]
        aggregateLongitude = ponAggregateDataBase[aggregateContractIndex][5]
      else:
        raise Exception('invalid indeces of aggregate contracts found: ', len(aggregateContractIndeces), ' for contract ', contractNumber, result, psrPostingFile)
        aggregateLatitude = '0'
        aggregateLongitude = '0'

      contractIndeces = [i for i, x in enumerate(ponDataBase[:,2]) if (x==contractNumber and ponDataBase[i,11 ] == PROVINCE)]
      firstContract = True;

      for index in contractIndeces:
        saleDate = ponDataBase[index][0]
        contractType = ponDataBase[index][1]
        hectares = ponDataBase[index][3]
        tractNo = ponDataBase[index][4]
        uwi = ponDataBase[index][5]
        topZone = ponDataBase[index][6]
        baseZone = ponDataBase[index][7]
        topAge = ponDataBase[index][8]
        baseAge = ponDataBase[index][9]
        geometry = ponDataBase[index][10]
        writePostingResultDataBaseFile(psrDataBaseFile, saleDate, status, bonus, dollarPerHectare, clientDescription, contractType, contractNumber, hectares, tractNo, uwi, topZone, baseZone, topAge, baseAge, geometry, PROVINCE)

        if firstContract:
           writePostingResultAggregateDataBaseFile(psrAggregateDataBaseFile, saleDate, status, bonus, dollarPerHectare, clientDescription, contractType, contractNumber, hectares, str(aggregateLatitude), str(aggregateLongitude), PROVINCE)

        firstContract = False
