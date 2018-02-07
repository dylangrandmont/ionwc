# Copyright (C) 2016-2018, Dylan Grandmont

import glob
import re
import numpy as np

from coordinatemapping import uwiToLatLng
from constants import KML_TEMPLATE, MONTH_DICT, IONWC_HOME
from utilities import writePostingResultDataBaseFile, writePostingResultAggregateDataBaseFile

PROVINCE = 'MB'
CONTRACT_TYPE = 'Lease'
TRACT_NUMBER = 1
TOP_ZONE = 'Surface'
TOP_QUALIFIER = 'From'
BASE_ZONE = 'Basement'
BASE_QUALIFIER = 'To'
TOP_AGE = 0
BASE_AGE = 9999

def postingUWIToKmlPolygon(uwi):
    kmlPolygon = ""

    sec = uwi[0]
    twp = uwi[1]
    rng = uwi[2]
    mer = uwi[3]

    allSections = re.findall('All [0-9]+', sec)

    quarterSections = []
    halfSections = []
    lsdString = []
    lsdNumbers = []

    aggregateLatitudes = []
    aggregateLongitudes = []

    try:
        section = re.findall('of [0-9]+', sec)[0].split()[1]
        quarterSections = re.findall('[A-Z][A-Z]\xc2\xbc', sec)
        halfSections = re.findall('[A-Z]\xc2\xbd', sec)
        lsdString = re.findall('Lsd.\'s .+ of', sec)
        if len(lsdString) > 0:
            lsdNumbers = re.findall('[0-9]+', lsdString[0])
    except:
    	section =  allSections[0].split()[1]

    for allSection in allSections:
        se_uwi = '01' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
        sw_uwi = '04' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
        nw_uwi = '13' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
        ne_uwi = '16' + '-' + section + '-' + twp + '-' + rng + 'W' + mer

        se_lat, se_lng = uwiToLatLng.convert(se_uwi, position = "se")
        sw_lat, sw_lng = uwiToLatLng.convert(sw_uwi, position = "sw")
        nw_lat, nw_lng = uwiToLatLng.convert(nw_uwi, position = "nw")
        ne_lat, ne_lng = uwiToLatLng.convert(ne_uwi, position = "ne")

        kmlPolygon += KML_TEMPLATE % (se_lng, se_lat, sw_lng, sw_lat, nw_lng, nw_lat, ne_lng, ne_lat)
        aggregateLatitudes.append( (se_lat + nw_lat) / 2.0)
        aggregateLongitudes.append( (se_lng + nw_lng) / 2.0)

    for quarterSection in quarterSections:
        if 'NE' in quarterSection: 
            se_uwi = '09' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            sw_uwi = '10' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            nw_uwi = '15' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            ne_uwi = '16' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
        elif 'NW' in quarterSection: 
            se_uwi = '11' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            sw_uwi = '12' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            nw_uwi = '13' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            ne_uwi = '14' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
        elif 'SE' in quarterSection: 
            se_uwi = '01' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            sw_uwi = '02' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            nw_uwi = '07' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            ne_uwi = '08' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
        elif 'SW' in quarterSection: 
            se_uwi = '03' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            sw_uwi = '04' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            nw_uwi = '05' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            ne_uwi = '06' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
        else:
            print "ERROR: invalid uwi found: ", uwi

        se_lat, se_lng = uwiToLatLng.convert(se_uwi, position = "se")
        sw_lat, sw_lng = uwiToLatLng.convert(sw_uwi, position = "sw")
        nw_lat, nw_lng = uwiToLatLng.convert(nw_uwi, position = "nw")
        ne_lat, ne_lng = uwiToLatLng.convert(ne_uwi, position = "ne")

        kmlPolygon += KML_TEMPLATE % (se_lng, se_lat, sw_lng, sw_lat, nw_lng, nw_lat, ne_lng, ne_lat)
        aggregateLatitudes.append( (se_lat + nw_lat) / 2.0)
        aggregateLongitudes.append( (se_lng + nw_lng) / 2.0)

    for halfSection in halfSections:
        if 'N' in halfSection: 
            se_uwi = '09' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            sw_uwi = '12' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            nw_uwi = '13' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            ne_uwi = '16' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
        elif 'E' in halfSection: 
            se_uwi = '01' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            sw_uwi = '02' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            nw_uwi = '15' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            ne_uwi = '16' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
        elif 'S' in halfSection: 
            se_uwi = '01' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            sw_uwi = '04' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            nw_uwi = '05' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            ne_uwi = '08' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
        elif 'W' in halfSection: 
            se_uwi = '03' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            sw_uwi = '04' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            nw_uwi = '13' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            ne_uwi = '14' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
        else:
            print "ERROR: invalid uwi found: ", uwi

        se_lat, se_lng = uwiToLatLng.convert(se_uwi, position = "se")
        sw_lat, sw_lng = uwiToLatLng.convert(sw_uwi, position = "sw")
        nw_lat, nw_lng = uwiToLatLng.convert(nw_uwi, position = "nw")
        ne_lat, ne_lng = uwiToLatLng.convert(ne_uwi, position = "ne")

        kmlPolygon += KML_TEMPLATE % (se_lng, se_lat, sw_lng, sw_lat, nw_lng, nw_lat, ne_lng, ne_lat)

        aggregateLatitudes.append( (se_lat + nw_lat) / 2.0)
        aggregateLongitudes.append( (se_lng + nw_lng) / 2.0)

    for lsdNumber in lsdNumbers:
        lsdNumber = '%02d' % int(lsdNumber)
        uwiLSD = lsdNumber + '-' + section + '-' + twp + '-' + rng + 'W' + mer

        se_lat, se_lng = uwiToLatLng.convert(uwiLSD, position = "se")
        sw_lat, sw_lng = uwiToLatLng.convert(uwiLSD, position = "sw")
        nw_lat, nw_lng = uwiToLatLng.convert(uwiLSD, position = "nw")
        ne_lat, ne_lng = uwiToLatLng.convert(uwiLSD, position = "ne")

        kmlPolygon += KML_TEMPLATE % (se_lng, se_lat, sw_lng, sw_lat, nw_lng, nw_lat, ne_lng, ne_lat)
        aggregateLatitudes.append( (se_lat + nw_lat) / 2.0)
        aggregateLongitudes.append( (se_lng + nw_lng) / 2.0)

    try:
        aggregateLatitude = sum(aggregateLatitudes) / len(aggregateLatitudes)
        aggregateLongitude = sum(aggregateLongitudes) / len(aggregateLongitudes)
    except:
        print 'ERROR: unable to find averages of lat / lng from uwi ', uwi
        aggregateLatitude = 0
        aggregateLongitude = 0

    return kmlPolygon, aggregateLatitude, aggregateLongitude

def getSaleDate(fileContents):

    closingDate = re.findall('[\w]+ [0-9]+\, [0-9][0-9][0-9][0-9]', fileContents)[0]

    year = closingDate.split()[2]
    day = '%02d' % int(closingDate.split()[1].replace(',', ''))
    month = MONTH_DICT[closingDate.split()[0].upper()]

    return year + '.' + month + '.' + day

def addMBOfferingsToDataBase(ponDataBaseFile, ponAggregateDataBaseFile):
    mbOfferingFiles = glob.glob(IONWC_HOME + '/data/postings/mb/*sale.txt')

    for mbOfferingFile in mbOfferingFiles:
        fileContents = ''.join(open(mbOfferingFile).readlines())

        saleDate = getSaleDate(fileContents)

        postings = re.findall('\n[\s]+[\w]+[\s]+\*?.+[0-9]+\s+[0-9]+\s+[\w]+\s+[0-9]+', fileContents)
        for posting in postings:
            posting = posting.replace('*', '')
            posting = posting.replace('\n\n', '')
            postingArray = re.split('\s\s\s\s+', posting)
            parcelNumber = postingArray[0].strip()
            sec = postingArray[1]
            twp = '%03d' % int(postingArray[2])
            rng = '%02d' % int(postingArray[3])
            mer = postingArray[4]
            if mer == 'WPM':
                mer = '1'

            uwi = twp + '-' + rng + 'W' + mer
            kmlPolygon, aggregateLatitude, aggregateLongitude = postingUWIToKmlPolygon([sec, twp, rng, mer])

            hectares = postingArray[5]

            ponDataBaseFile.write(saleDate + ':' + CONTRACT_TYPE + ':' + str(parcelNumber) + ':' + hectares + ':' + str(TRACT_NUMBER) + ':' + uwi + ':' + TOP_QUALIFIER + ' ' + TOP_ZONE + ':' + BASE_QUALIFIER + ' ' + BASE_ZONE + ':' + str(TOP_AGE) + ':' + str(BASE_AGE) + ':' + kmlPolygon + ':' + PROVINCE + '\n')
            ponAggregateDataBaseFile.write(saleDate + ':' + CONTRACT_TYPE + ':' + str(parcelNumber) + ':' + hectares + ':' + str(aggregateLatitude) + ':' + str(aggregateLongitude) + ':' + PROVINCE + '\n')


def addMBResultsToDataBase(psrDataBaseFile, psrAggregateDataBaseFile, ponDataBaseFile, ponAggregateDataBaseFile):
    ponDataBase = np.loadtxt(ponDataBaseFile, delimiter=':', dtype=str)
    ponAggregateDataBase = np.loadtxt(ponAggregateDataBaseFile, delimiter=':', dtype=str)

    mbResultsFiles = glob.glob(IONWC_HOME + '/data/postings/mb/*results.txt')

    for mbResultsFile in mbResultsFiles:
        fileContents = ''.join(open(mbResultsFile).readlines())

        saleDate = getSaleDate(fileContents)

        postings = re.findall('[\w]+[\s]+[0-9]+[\s]+[0-9]+[\s]+.{0,50}[0-9].+\.[0-9]+', fileContents)
        for posting in postings:
            contractNumber = posting.split()[0]
            posting.split()[-1]
            bonus = posting.split()[-5]
            dollarPerHectare = posting.split()[-4]

            aggregateContractIndeces = [i for i, x in enumerate(ponAggregateDataBase[:,2]) if (x==contractNumber and ponAggregateDataBase[i, 6] == PROVINCE and ponAggregateDataBase[i,0] == saleDate)]
            if len(aggregateContractIndeces) == 1:
                aggregateContractIndex = aggregateContractIndeces[0]
                aggregateLatitude = ponAggregateDataBase[aggregateContractIndex][4]
                aggregateLongitude = ponAggregateDataBase[aggregateContractIndex][5]
            else:
                print 'ERROR: invalid indeces of aggregate contracts found: ', len(aggregateContractIndeces), ' for contract ', contractNumber
                aggregateLatitude = '0'
                aggregateLongitude = '0'

            contractIndeces = [i for i, x in enumerate(ponDataBase[:,2]) if (x == contractNumber and ponDataBase[i,11] == PROVINCE and ponDataBase[i,0] == saleDate)]

            for index in contractIndeces:
                contractType = ponDataBase[index][1]
                hectares = ponDataBase[index][3]
                tractNo = ponDataBase[index][4]
                uwi = ponDataBase[index][5]
                topZone = ponDataBase[index][6]
                baseZone = ponDataBase[index][7]
                topAge = ponDataBase[index][8]
                baseAge = ponDataBase[index][9]
                geometry = ponDataBase[index][10]

            if 'No Acceptable Bid' in posting:
                status = 'No Acceptable Offers'
                clientDescription = ''
            else:
                status = 'Accepted'
                clientDescription = re.split('\s\s\s+', posting)[5] + ' 100%'

            writePostingResultDataBaseFile(psrDataBaseFile, saleDate, status, bonus, dollarPerHectare, clientDescription, contractType, contractNumber, hectares, tractNo, uwi, topZone, baseZone, topAge, baseAge, geometry, PROVINCE)
            writePostingResultAggregateDataBaseFile(psrAggregateDataBaseFile, saleDate, status, bonus, dollarPerHectare, clientDescription, contractType, contractNumber, hectares, str(aggregateLatitude), str(aggregateLongitude), PROVINCE)
