#!/bin/bash

##################################################################
# Copyright (C) 2016, Eye on Western Canada
#
# Methods for parsing SK land postings
#
##################################################################

import re
import glob
import numpy as np

from coordinatemapping import uwiToLatLng
from constants import FORMATION_AGE_DICT, SK_POSTING_NUMBER_TO_SALE_DATE, KML_TEMPLATE
from constants import IONWC_HOME
from utilities import writePostingResultDataBaseFile, writePostingResultAggregateDataBaseFile

PROVINCE = 'SK'
TOP_QUALIFIER = 'From'
BASE_QUALIFIER = 'To'
CONTRACT_TYPE = "Licence"

def postingUWIToKmlPolygon(coordinates):
    mer = coordinates[-1] 
    rng = '%02d' % int(coordinates[-2])
    twp = '%03d' % int(coordinates[-3])

    if len(coordinates) == 5:
        sec = coordinates[-4]

        if coordinates[0] == 'NE':
            uwi = 'NE' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
            se_uwi = '09' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
            sw_uwi = '10' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
            nw_uwi = '15' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
            ne_uwi = '16' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
        elif coordinates[0] == 'NW':
            uwi = 'NW' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
            se_uwi = '11' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
            sw_uwi = '12' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
            nw_uwi = '13' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
            ne_uwi = '14' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
        elif coordinates[0] == 'SE':
            uwi = 'SE' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
            se_uwi = '01' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
            sw_uwi = '02' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
            nw_uwi = '07' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
            ne_uwi = '08' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
        elif coordinates[0] == 'SW':
            uwi = 'SW' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
            se_uwi = '03' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
            sw_uwi = '04' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
            nw_uwi = '05' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
            ne_uwi = '06' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
        else:
            lsd = coordinates[0]
            uwi = lsd + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
            se_uwi = uwi
            sw_uwi = uwi
            nw_uwi = uwi
            ne_uwi = uwi

    elif len(coordinates) == 4:
        sec = coordinates[-4]
        uwi = sec + '-' + twp + '-' + rng + 'W' + mer
        se_uwi = '01' + '-' + uwi
        sw_uwi = '04' + '-' +uwi
        nw_uwi = '13' + '-' +uwi
        ne_uwi = '16' + '-' +uwi

    elif len(coordinates) == 3:
        uwi = twp + '-' + rng + 'W' + mer
        se_uwi = '01' + '-' + '01' + '-' + uwi
        sw_uwi = '04' + '-' + '06' + '-' + uwi
        nw_uwi = '13' + '-' + '31' + '-' + uwi
        ne_uwi = '16' + '-' + '36' + '-' + uwi
    else: 
        print 'ERROR: invalid SK uwi found: ', coordinates, file

    se_lat, se_lng = uwiToLatLng.convert(se_uwi, position = "se")
    sw_lat, sw_lng = uwiToLatLng.convert(sw_uwi, position = "sw")
    nw_lat, nw_lng = uwiToLatLng.convert(nw_uwi, position = "nw")
    ne_lat, ne_lng = uwiToLatLng.convert(ne_uwi, position = "ne")

    kmlPolygon = KML_TEMPLATE % (se_lng, se_lat, sw_lng, sw_lat, nw_lng, nw_lat, ne_lng, ne_lat)

    centerLatitude = (se_lat + nw_lat) / 2.0
    centerLongitude = (se_lng + nw_lng) / 2.0

    return kmlPolygon, uwi, centerLatitude, centerLongitude

def addSKOfferingsToDataBase(ponDataBaseFile, ponAggregateDataBaseFile):
    """ Add all land offerings into database """
    files = glob.glob(IONWC_HOME + '/data/postings/sk/*otice*.txt')

    # Store all aggregate entries and add to database at the end
    aggregatePONEntries = []

    for file in files:
        print file
        fileContents = ''.join(open(file).readlines())

        licences = re.split('Petroleum and Natural Gas Exploration Licence', fileContents)
        if len(licences) > 1:
            leases = re.split('Petroleum and Natural Gas Lease', licences[1])[1]
            licences = ''.join(re.split('Petroleum and Natural Gas Lease', licences[1])[0])
        else:
            licences = ''
            leases = re.split('Petroleum and Natural Gas Lease', fileContents)[1]

        saleNumber = re.findall('PUBLIC NOTICE [0-9]+', fileContents)[0].split()[2]
        saleDate = SK_POSTING_NUMBER_TO_SALE_DATE[saleNumber]
        entries = re.findall('.+[0-9]+.[0-9]+\s+Oil and Gas+.+', fileContents)

        parcelNumber = 1
        contractType = ''

        for entry in entries:

            if entry in licences:
                contractType = 'Licence'
            elif entry in leases:
                contractType = 'Lease'
            else:
                print 'ERROR: no valid contract type found for entry ', entry

            coordinates = re.findall('[\w]+', re.split('[0-9]+\.[0-9]+', entry)[0])

            # Check if new parcel has been reached
            if entry[0:3].strip().isdigit():
                parcelNumber = entry[0:3].strip()
                coordinates = coordinates[1:]
                tractNo = 1
                aggregatePONEntries.append([saleDate, contractType, parcelNumber, 0, 0, 0, PROVINCE])

            if coordinates[0] == 'PTN': 
                coordinates = coordinates[1:]
            elif coordinates[0] == 'FRAC':
                coordinates = coordinates[1:]

            hectares = re.findall('[0-9]+\.[0-9]+',entry)[0]
            aggregatePONEntries[-1][3] += float(hectares)

            topZone = re.split('\s\s+', re.split('Oil and Gas', entry)[1])[1].title()
            baseZone = re.split('\s\s+', re.split('Oil and Gas', entry)[1])[2].title()

            topAge = FORMATION_AGE_DICT[topZone.lower()]
            baseAge = FORMATION_AGE_DICT[baseZone.lower()]

            kmlPolygon, uwi, centerLatitude, centerLongitude = postingUWIToKmlPolygon(coordinates)

            aggregatePONEntries[-1][4] *= (tractNo - 1) / float(tractNo)
            aggregatePONEntries[-1][5] *= (tractNo - 1) / float(tractNo)

            aggregatePONEntries[-1][4] += ((1.0) / float(tractNo)) * centerLatitude
            aggregatePONEntries[-1][5] += ((1.0) / float(tractNo)) * centerLongitude

            ponDataBaseFile.write(saleDate + ':' + contractType + ':' + str(parcelNumber) + ':' + hectares + ':' + str(tractNo) + ':' + uwi + ':' + TOP_QUALIFIER + ' ' + topZone + ':' + BASE_QUALIFIER + ' ' + baseZone + ':' + str(topAge) + ':' + str(baseAge) + ':' + kmlPolygon + ':' + PROVINCE + '\n')
            tractNo += 1

    for aggregatePONEntry in aggregatePONEntries:
        line = ''
        for i in aggregatePONEntry:
            line += str(i) + ':'
        line = line[0:-1]
        line += '\n'
        ponAggregateDataBaseFile.write(line)

def addSKResultsToDataBase(psrDataBaseFile, psrAggregateDataBaseFile, ponDataBaseFile, ponAggregateDataBaseFile):
    ponDataBase = np.loadtxt(ponDataBaseFile, delimiter=':', dtype=str)
    ponAggregateDataBase = np.loadtxt(ponAggregateDataBaseFile, delimiter=':', dtype=str)

    files = glob.glob(IONWC_HOME + '/data/postings/sk/*result*.txt')
    for file in files:
        print file

        fileContents = ''.join(open(file).readlines()).replace(',', '')

        saleNumberLine = re.findall('Sale [0-9]+', fileContents)

        if len(saleNumberLine) < 1:
            saleNumberLine = re.findall('Public Offering [0-9]+', fileContents)  

        saleNumber = re.findall('[0-9]+', saleNumberLine[0])[0]
        saleDate = SK_POSTING_NUMBER_TO_SALE_DATE[saleNumber]

        noSubmittedBids = re.findall('.+No Bids Submitted', fileContents)
        noAcceptableBids = re.findall('.+No Acceptable Bids', fileContents)
        acceptedBidsMultipleInterests = re.findall('\n[0-9]+[\s]+[\w]+.+[0-9]+[\s]+[0-9]+.[0-9]+[\s]+[0-9]+.[0-9]+\n                       [a-zA-Z].+               [0-9]+.[0-9]+', fileContents)
        acceptedBidsOneInterests = re.findall('\n[0-9]+[\s]+[\w]+.+100[\s]+[0-9]+.[0-9]+[\s]+[0-9]+\.[0-9]+[\s]+[0-9]+\.[0-9]+', fileContents)

        for noAcceptableBid in noAcceptableBids:
            status = 'No Acceptable Offers'
            bonus = ''
            dollarPerHectare = ''
            clientDescription = ''
            contractNumber = noAcceptableBid.split()[0]

            aggregateContractIndeces = [i for i, x in enumerate(ponAggregateDataBase[:,2]) if (x==contractNumber and ponAggregateDataBase[i, 6] == PROVINCE and ponAggregateDataBase[i,0] == saleDate)]
            if len(aggregateContractIndeces) == 1:
              aggregateContractIndex = aggregateContractIndeces[0]
              aggregateLatitude = ponAggregateDataBase[aggregateContractIndex][4]
              aggregateLongitude = ponAggregateDataBase[aggregateContractIndex][5]
            else:
              print 'ERROR: invalid indeces of aggregate contracts found: ', len(aggregateContractIndeces), ' for contract ', contractNumber
              aggregateLatitude = '0'
              aggregateLongitude = '0'

            contractIndeces = [i for i, x in enumerate(ponDataBase[:,2]) if (x==contractNumber and ponDataBase[i,11]==PROVINCE and ponDataBase[i,0] == saleDate)]
            totalHectares = 0

            for index in contractIndeces:
                contractType = ponDataBase[index][1]
                hectares = ponDataBase[index][3]
                totalHectares += float(hectares)
                tractNo = ponDataBase[index][4]
                uwi = ponDataBase[index][5]
                topZone = ponDataBase[index][6]
                baseZone = ponDataBase[index][7]
                topAge = ponDataBase[index][8]
                baseAge = ponDataBase[index][9]
                geometry = ponDataBase[index][10]

                writePostingResultDataBaseFile(psrDataBaseFile, saleDate, status, bonus, dollarPerHectare, clientDescription, contractType, contractNumber, hectares, tractNo, uwi, topZone, baseZone, topAge, baseAge, geometry, PROVINCE)

            if len(contractIndeces) > 0:
                writePostingResultAggregateDataBaseFile(psrAggregateDataBaseFile, saleDate, status, bonus, dollarPerHectare, clientDescription, contractType, contractNumber, totalHectares, str(aggregateLatitude), str(aggregateLongitude), PROVINCE)

        for noSubmittedBid in noSubmittedBids:
            status =  'No Offers'
            bonus = ''
            dollarPerHectare = ''
            clientDescription = ''
            contractNumber = noSubmittedBid.split()[0]

            aggregateContractIndeces = [i for i, x in enumerate(ponAggregateDataBase[:,2]) if (x==contractNumber and ponAggregateDataBase[i, 6] == PROVINCE and ponAggregateDataBase[i,0] == saleDate)]
            if len(aggregateContractIndeces) == 1:
              aggregateContractIndex = aggregateContractIndeces[0]
              aggregateLatitude = ponAggregateDataBase[aggregateContractIndex][4]
              aggregateLongitude = ponAggregateDataBase[aggregateContractIndex][5]
            else:
              print 'ERROR: invalid indeces of aggregate contracts found: ', len(aggregateContractIndeces), ' for contract ', contractNumber
              aggregateLatitude = '0'
              aggregateLongitude = '0'

            contractIndeces = [i for i, x in enumerate(ponDataBase[:,2]) if (x==contractNumber and ponDataBase[i,11]==PROVINCE and ponDataBase[i,0] == saleDate)]
            totalHectares = 0

            for index in contractIndeces:
                contractType = ponDataBase[index][1]
                hectares = ponDataBase[index][3]
                totalHectares += float(hectares)
                tractNo = ponDataBase[index][4]
                uwi = ponDataBase[index][5]
                topZone = ponDataBase[index][6]
                baseZone = ponDataBase[index][7]
                topAge = ponDataBase[index][8]
                baseAge = ponDataBase[index][9]
                geometry = ponDataBase[index][10]

                writePostingResultDataBaseFile(psrDataBaseFile, saleDate, status, bonus, dollarPerHectare, clientDescription, contractType, contractNumber, hectares, tractNo, uwi, topZone, baseZone, topAge, baseAge, geometry, PROVINCE)

            if len(contractIndeces) > 0:
                writePostingResultAggregateDataBaseFile(psrAggregateDataBaseFile, saleDate, status, bonus, dollarPerHectare, clientDescription, contractType, contractNumber, totalHectares, str(aggregateLatitude), str(aggregateLongitude), PROVINCE)


        for acceptedBidsMultipleInterest in acceptedBidsMultipleInterests:
            status = 'Accepted'
            numbers = re.findall('[^\s][0-9]+[^\s]+[0-9]+[^\s]', acceptedBidsMultipleInterest)
            bonus = numbers[-4]
            dollarPerHectare = numbers[-2]
            clientArray = re.split('[\s][\s]+', acceptedBidsMultipleInterest)
            clientDescription = clientArray[2] + ' ' + clientArray[3] + '%'
            clientDescription += clientArray[7] + ' '+ clientArray[8] + '%'
            
            contractNumber = acceptedBidsMultipleInterest.split()[0]

            aggregateContractIndeces = [i for i, x in enumerate(ponAggregateDataBase[:,2]) if (x==contractNumber and ponAggregateDataBase[i, 6] == PROVINCE and ponAggregateDataBase[i,0] == saleDate)]
            if len(aggregateContractIndeces) == 1:
              aggregateContractIndex = aggregateContractIndeces[0]
              aggregateLatitude = ponAggregateDataBase[aggregateContractIndex][4]
              aggregateLongitude = ponAggregateDataBase[aggregateContractIndex][5]
            else:
              print 'ERROR: invalid indeces of aggregate contracts found: ', len(aggregateContractIndeces), ' for contract ', contractNumber
              aggregateLatitude = '0'
              aggregateLongitude = '0'

            contractIndeces = [i for i, x in enumerate(ponDataBase[:,2]) if (x==contractNumber and ponDataBase[i,11]==PROVINCE and ponDataBase[i,0] == saleDate)]
            totalHectares = 0

            for index in contractIndeces:
                contractType = ponDataBase[index][1]
                hectares = ponDataBase[index][3]
                totalHectares += float(hectares)
                tractNo = ponDataBase[index][4]
                uwi = ponDataBase[index][5]
                topZone = ponDataBase[index][6]
                baseZone = ponDataBase[index][7]
                topAge = ponDataBase[index][8]
                baseAge = ponDataBase[index][9]
                geometry = ponDataBase[index][10]

                writePostingResultDataBaseFile(psrDataBaseFile, saleDate, status, bonus, dollarPerHectare, clientDescription, contractType, contractNumber, hectares, tractNo, uwi, topZone, baseZone, topAge, baseAge, geometry, PROVINCE)

            if len(contractIndeces) > 0:
                writePostingResultAggregateDataBaseFile(psrAggregateDataBaseFile, saleDate, status, bonus, dollarPerHectare, clientDescription, contractType, contractNumber, totalHectares, str(aggregateLatitude), str(aggregateLongitude), PROVINCE)


        for acceptedBidsOneInterest in acceptedBidsOneInterests:
            status = 'Accepted'
            decimals = re.findall('[^\s][0-9]*\.+[0-9]*[^\s]', acceptedBidsOneInterest)
            bonus = decimals[-3]
            dollarPerHectare = decimals[-1]
            client = re.split('[\s][\s]+', acceptedBidsOneInterest)[2]
            workingInterest = re.split('[\s][\s]+', acceptedBidsOneInterest)[3]
            clientDescription = client + ' ' + workingInterest + '% '
            contractNumber = acceptedBidsOneInterest.split()[0]

            aggregateContractIndeces = [i for i, x in enumerate(ponAggregateDataBase[:,2]) if (x==contractNumber and ponAggregateDataBase[i, 6] == PROVINCE and ponAggregateDataBase[i,0] == saleDate)]
            if len(aggregateContractIndeces) == 1:
              aggregateContractIndex = aggregateContractIndeces[0]
              aggregateLatitude = ponAggregateDataBase[aggregateContractIndex][4]
              aggregateLongitude = ponAggregateDataBase[aggregateContractIndex][5]
            else:
              print contractNumber, saleDate
              print 'ERROR: invalid indeces of aggregate contracts found: ', len(aggregateContractIndeces), ' for contract ', contractNumber
              aggregateLatitude = '0'
              aggregateLongitude = '0'

            contractIndeces = [i for i, x in enumerate(ponDataBase[:,2]) if (x==contractNumber and ponDataBase[i,11]==PROVINCE and ponDataBase[i,0] == saleDate)]
            totalHectares = 0

            for index in contractIndeces:
                contractType = ponDataBase[index][1]
                hectares = ponDataBase[index][3]
                totalHectares += float(hectares)
                tractNo = ponDataBase[index][4]
                uwi = ponDataBase[index][5]
                topZone = ponDataBase[index][6]
                baseZone = ponDataBase[index][7]
                topAge = ponDataBase[index][8]
                baseAge = ponDataBase[index][9]
                geometry = ponDataBase[index][10]

                writePostingResultDataBaseFile(psrDataBaseFile, saleDate, status, bonus, dollarPerHectare, clientDescription, contractType, contractNumber, hectares, tractNo, uwi, topZone, baseZone, topAge, baseAge, geometry, PROVINCE)

            if len(contractIndeces) > 0:
                writePostingResultAggregateDataBaseFile(psrAggregateDataBaseFile, saleDate, status, bonus, dollarPerHectare, clientDescription, contractType, contractNumber, totalHectares, str(aggregateLatitude), str(aggregateLongitude), PROVINCE)


