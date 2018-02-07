# Copyright (C) 2016-2018, Dylan Grandmont

import xml.etree.ElementTree as ET
import numpy as np
import locale
import glob

from coordinatemapping import uwiToLatLng
from constants import FORMATION_AGE_DICT, KML_TEMPLATE, IONWC_HOME
from utilities import writePostingResultDataBaseFile, writePostingResultAggregateDataBaseFile, writePostingOfferingDataBaseFile

PROVINCE = 'AB'

def postingUWIToKmlPolygon(uwi, lsd, sec, twp, rng, mer):
    if lsd=='NE': 
        se_uwi = '09' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
        sw_uwi = '10' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
        nw_uwi = '15' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
        ne_uwi = '16' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
    elif lsd=='NW': 
        se_uwi = '11' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
        sw_uwi = '12' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
        nw_uwi = '13' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
        ne_uwi = '14' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
    elif lsd=='SE': 
        se_uwi = '01' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
        sw_uwi = '02' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
        nw_uwi = '07' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
        ne_uwi = '08' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
    elif lsd=='SW': 
        se_uwi = '03' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
        sw_uwi = '04' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
        nw_uwi = '05' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
        ne_uwi = '06' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
    elif lsd=='  ': 
        se_uwi = '01' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
        sw_uwi = '04' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
        nw_uwi = '13' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
        ne_uwi = '16' + '-' + sec + '-' + twp + '-' + rng + 'W' + mer
    else:
        se_uwi = uwi
        sw_uwi = uwi
        nw_uwi = uwi
        ne_uwi = uwi

    se_lat, se_lng = uwiToLatLng.convert(se_uwi, position = "se")
    sw_lat, sw_lng = uwiToLatLng.convert(sw_uwi, position = "sw")
    nw_lat, nw_lng = uwiToLatLng.convert(nw_uwi, position = "nw")
    ne_lat, ne_lng = uwiToLatLng.convert(ne_uwi, position = "ne")

    kmlPolygon = KML_TEMPLATE % (se_lng, se_lat, sw_lng, sw_lat, nw_lng, nw_lat, ne_lng, ne_lat)

    centerLatitude = (se_lat + nw_lat) / 2.0
    centerLongitude = (se_lng + nw_lng) / 2.0

    return kmlPolygon, centerLatitude, centerLongitude

def addABOfferingsToDataBase(outKmlFile, ponAggregateDataBaseFile):
    """ Parse Public Offering Notice into a File of Postings """

    ponFiles = glob.glob(IONWC_HOME + '/data/postings/ab/*PON.xml')
    for AER_POSTING_FILE in ponFiles:
        tree = ET.parse(AER_POSTING_FILE)
        root = tree.getroot()

        namespace = "{http://tempuri.org/PON.xsd}"
        saleDate = root.find(".//" + namespace + "SaleDate").text.replace('-','.')
        schedules = root.findall(".//" + namespace + "Schedule")

        for schedule in schedules:
            contractType = schedule.find(".//" + namespace + "ContractType").text.title()
            contracts = schedule.findall(".//" + namespace + "Contract")

            for contract in contracts:
                contractNo = contract.find(".//" + namespace + "ContractNo").text
                hectares = contract.find(".//" + namespace + "Hectares").text
                tracts = contract.findall(".//" + namespace + "Tract")

                aggregateLatitudes = []
                aggregateLongitudes = []

                for tract in tracts:
                    tractNo = tract.find(".//" + namespace + "TractNo").text
                    lands = tract.findall(".//" + namespace + "Land")
                    baseZone = ''
                    topZone = ''
                    lines = tract.findall(".//" + namespace + "Line")
                    topQualifier = lines[0].find(".//" + namespace + "Qualifier").text.title()
                    topZone = lines[0].find(".//" + namespace + "ZoneName").text.title()
                    baseQualifier = lines[1].find(".//" + namespace + "Qualifier").text.title()
                    baseZone = lines[1].find(".//" + namespace + "ZoneName").text.title()

                    for land in lands:
                        landKey = land.find(".//" + namespace + "LandKey").text
                        landKey += '       '
                        mer = landKey[0]
                        rng = landKey[1:3]
                        twp = landKey[3:6]
                        sec = landKey[6:8]
                        lsd = landKey[8:10]
                        uwi =  lsd + '-' + sec + '-' + twp + '-' + rng + 'W' + mer

                        kmlPolygon, centerLatitude, centerLongitude = postingUWIToKmlPolygon(uwi, lsd, sec, twp, rng, mer)
                        aggregateLatitudes.append(centerLatitude)
                        aggregateLongitudes.append(centerLongitude)

                        try:
                            topAge = FORMATION_AGE_DICT[topZone.lower().replace(' fm', '').replace(' sd', '').replace(' grp', '').replace(' mbr', '').replace(' ss', '').replace('zone', '').strip()]
                            baseAge = FORMATION_AGE_DICT[baseZone.lower().replace(' fm', '').replace(' sd', '').replace(' grp', '').replace(' mbr', '').replace(' ss', '').replace('zone', '').strip()]
                        except:
                            raise Exception('No entry found in FORMATION_AGE_DICT for ', topZone, baseZone)

                        writePostingOfferingDataBaseFile(outKmlFile, saleDate, contractType, contractNo, hectares, tractNo, uwi, topQualifier + ' ' + topZone, baseQualifier + ' ' + baseZone, str(topAge), str(baseAge), kmlPolygon, PROVINCE)

                aggregateLatitude = sum(aggregateLatitudes) / len(aggregateLatitudes)
                aggregateLongitude = sum(aggregateLongitudes) / len(aggregateLongitudes)
                ponAggregateDataBaseFile.write(saleDate + ':' + contractType + ':' + contractNo + ':' + hectares + ':' + str(aggregateLatitude) + ':' + str(aggregateLongitude) + ':' + PROVINCE + '\n')


def addABResultsToDataBase(psrDataBaseFile, psrAggregateDataBaseFile, ponDataBaseFile, ponAggregateDataBaseFile):
    """ Parse Public Results Notice into a File of Postings """
    ponDataBase = np.loadtxt(ponDataBaseFile, delimiter = ':', dtype = str)
    ponAggregateDataBase = np.loadtxt(ponAggregateDataBaseFile, delimiter=':', dtype=str)

    psrFiles = glob.glob(IONWC_HOME + '/data/postings/ab/*PSR.xml')
    for psrPostingFile in psrFiles:
        tree = ET.parse(psrPostingFile)
        root = tree.getroot()
        
        locale.setlocale(locale.LC_ALL, '')

        namespace = ''
        saleDate = root.find(".//" + namespace + "SaleDate").text.replace('/','.')
        parcels = root.findall(".//" + namespace + "Parcel")
        for parcel in parcels:
            parcelNumber = parcel.find(".//" + namespace + "ParcelNumber").text
            contractFlag = parcel.find(".//" + namespace + "ContractFlag").text
            contractNumber = contractFlag + parcelNumber

            status = parcel.find(".//" + namespace + "Status").text.title()
            bonus = ''
            dollarPerHectare = ''
            if status == 'Accepted':
                bonus = locale.currency( float( parcel.find(".//" + namespace + "Bonus").text ), grouping = True)
                dollarPerHectare = locale.currency( float( parcel.find(".//" + namespace + "DollarPerHectare").text ), grouping=True)
            
            clientDescription = ''
            clients = parcel.findall(".//" + namespace + "Clients")
            for client in clients:
                try:
                    clientName = client.find(".//" + namespace + "ClientName").text.title()
                    percentage = '%d' % float(client.find(".//" + namespace + "Percentage").text) + '%'
                    clientDescription += clientName + " " + percentage + " "
                except: 
                    pass


            aggregateContractIndeces = [i for i, x in enumerate(ponAggregateDataBase[:,2]) if (x==contractNumber and ponAggregateDataBase[i, 6] == PROVINCE and ponAggregateDataBase[i,0] == saleDate)]
            if len(aggregateContractIndeces) == 1:
                aggregateContractIndex = aggregateContractIndeces[0]
                aggregateLatitude = ponAggregateDataBase[aggregateContractIndex][4]
                aggregateLongitude = ponAggregateDataBase[aggregateContractIndex][5]
            else:
                print 'ERROR: invalid indeces of aggregate contracts found: ', len(aggregateContractIndeces), ' for contract ', contractNumber
                aggregateLatitude = '0'
                aggregateLongitude = '0'

            contractIndeces = [i for i, x in enumerate(ponDataBase[:,2]) if (x==contractNumber and ponDataBase[i,11] == PROVINCE and ponDataBase[i,0] == saleDate)]
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

                writePostingResultDataBaseFile(psrDataBaseFile, saleDate, status, bonus, dollarPerHectare, clientDescription, contractType, contractNumber, hectares, tractNo, uwi, topZone, baseZone, topAge, baseAge, geometry, PROVINCE)
               
            writePostingResultAggregateDataBaseFile(psrAggregateDataBaseFile, saleDate, status, bonus, dollarPerHectare, clientDescription, contractType, contractNumber, hectares, str(aggregateLatitude), str(aggregateLongitude), PROVINCE)
