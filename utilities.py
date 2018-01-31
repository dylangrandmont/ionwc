#!/bin/bash

import locale
import math

def getSubCode(substance):
    substance = substance.lower()
    if   'oil'     in substance:   substanceCode = '0'
    elif 'gas'     in substance:   substanceCode = '1'
    elif 'methane' in substance:   substanceCode = '1'
    elif 'bitum'   in substance:   substanceCode = '2'
    elif 'water'   in substance:   substanceCode = '3'
    else:                          substanceCode = '4'
    return substanceCode

def conformSub(substance):
    if substance == "0":                  substance = "Unknown"
    elif 'gas'   in substance.lower():    substance = "Gas"
    elif 'oil'   in substance.lower():    substance = "Crude Oil"
    return substance

def conformBCOGCLatLon(latitude, longitude):
    latitude = latitude.strip().split()
    longitude = longitude.strip().split()
    latitude =         float(latitude[0]) + float(latitude[1]) / 60.0 + float(latitude[2]) / 3600.0
    longitude = -1.0 * (float(longitude[0]) + float(longitude[1]) / 60.0 + float(longitude[2]) / 3600.0)
    return latitude, longitude

def formatDollars(dollarString):
  if dollarString != '':
    dollarString = dollarString.replace('$', '')
    dollarString = dollarString.replace(',', '')
    locale.setlocale(locale.LC_ALL, '')
    dollarString = locale.currency(float(dollarString), grouping = True)
  return dollarString

def kmPerDegreeLatLng(lat):
  # determine distance between degrees of latitude (const), using spheroid paramters
  e2 = 0.00669437999014
  a = 6378.1370
  pi = math.pi
  kmPerDegreeLat = pi * a * (1 - e2) / (180.0 * (1.0 - e2 * (math.sin(lat * pi / 180.0)**2)**(3.0/2.0)))
  kmPerDegreeLng = (pi*a* math.cos(lat*pi/180.0)) / (180.0 * (1.0-e2*(math.sin(lat*pi/180.0)**2))**0.5 )

  return kmPerDegreeLat, kmPerDegreeLng


def writeLicenseFile(licenseFile, licensee, wellname, licnum, uwi, year, month, day, field, zone, 
                    direct, sub, subcode, lat, lon, province):
    licenseFile.write(licensee.replace(',','').title().strip() + ","
                      + wellname.replace(',','').upper().strip() + ","
                      + licnum.replace(',','').strip() + ","
                      + uwi.replace(',','').strip() + ","
                      + year + "." + month + "." + day + ","
                      + year + "/" + month + ","
                      + field.replace(',','').title().strip() + ","
                      + zone.replace(',','').title().strip() + ","
                      + direct.replace(',','').title().strip() + ","
                      + sub.replace(',','').title().strip() + ","
                      + subcode + ","
                      + str(lat) + ","
                      + str(lon) + ","
                      + province + "\n")

def writeDrillingFile(drillingFile, licensee, wellname, licnum, uwi, year, month, day, 
                      driller, rig, lat, lon, province):
  drillingFile.write(licensee.title().strip() + ","
                    + wellname.strip() + ","
                    + licnum.strip() + ","
                    + uwi.strip() + ","
                    + year + "." + month + "." + day + ","
                    + year + "/" + month + ","
                    + driller.title().strip() + ","
                    + rig.strip() + ","
                    + str(lat) + ","
                    + str(lon) + ","
                    + province + "\n")

def writeAugmentedLicenceFile(augmentedLicencesFile, licensee, wellname, licnum, uwi, drilldate, drilldatemonth,
                              contract, rig, licdate, field, zone, orient, sub, subcode, lat, lng, province):
  augmentedLicencesFile.write(licensee + "," 
                              + wellname + "," 
                              + licnum + "," 
                              + uwi + "," 
                              + drilldate + "," 
                              + drilldatemonth + ","
                              + contract + "," 
                              + rig + "," 
                              + licdate + "," 
                              + field + "," 
                              + zone + "," 
                              + orient + "," 
                              + sub + "," 
                              + subcode + "," 
                              + str(lat) + "," 
                              + str(lng) + ","
                              + province + "\n")

def writePostingOfferingDataBaseFile(outKmlFile, saleDate, contractType, contractNo, hectares, tractNo, uwi,
                                     topQualifiedZone, baseQualifiedZone, topAge, baseAge, kmlPolygon, province):
  outKmlFile.write(saleDate + ':'
                   + contractType + ':'
                   + contractNo + ':'
                   + hectares + ':'
                   + tractNo + ':'
                   + uwi + ':'
                   + topQualifiedZone +':'
                   + baseQualifiedZone + ':'
                   + topAge + ':'
                   + baseAge + ':'
                   + kmlPolygon + ':'
                   + province + '\n')

def writePostingOfferingAggregateDataBaseFile(ponAggregateDataBaseFile, saleDate, contractType, contractNo, hectares,
                                              aggregateLatitude, aggregateLongitude, province):
  ponAggregateDataBaseFile.write(saleDate + ':'
                                 + contractType + ':'
                                 + contractNo + ':'
                                 + hectares + ':'
                                 + str(aggregateLatitude) + ':'
                                 + str(aggregateLongitude) + ':'
                                 + province + '\n')

def writePostingResultDataBaseFile(psrDataBaseFile, saleDate, status, bonus, dollarPerHectare, clientDescription, 
                                   contractType, contractNumber, hectares, tractNo, uwi, topZone, baseZone, topAge, 
                                   baseAge, geometry, province):
  psrDataBaseFile.write(saleDate + ':' 
                        + status + ':' 
                        + formatDollars(bonus) + ':' 
                        + formatDollars(dollarPerHectare) + ':' 
                        + clientDescription.title() + ':' 
                        + contractType + ':' 
                        + contractNumber + ':' 
                        + str(hectares) + ':' 
                        + tractNo + ':' 
                        + uwi + ':' 
                        + topZone + ':' 
                        + baseZone + ':' 
                        + str(topAge) + ':' 
                        + str(baseAge) + ':' 
                        + geometry + ':' 
                        + province + '\n')

def writePostingResultAggregateDataBaseFile(psrAggregateDataBaseFile, saleDate, status, bonus, dollarPerHectare, clientDescription, 
                                   contractType, contractNumber, hectares, aggregateLatitude, aggregateLongitude, province):
  psrAggregateDataBaseFile.write(saleDate + ':' 
                                + status + ':' 
                                + formatDollars(bonus) + ':' 
                                + formatDollars(dollarPerHectare) + ':' 
                                + clientDescription.title() + ':' 
                                + contractType + ':'
                                + contractNumber + ':'
                                + str(hectares) + ':'
                                + str(aggregateLatitude) + ':'
                                + str(aggregateLongitude) + ':'
                                + province + '\n')

  def writeFaciltiesFile(facilitiesFileAll, facilityId, facilityType, organization, lat, lng):
    facilitiesFileAll.write(facilitiesFileAll + ':' 
                                + facilityId + ':' 
                                + facilityType + ':' 
                                + organization + ':' 
                                + lat + ':' 
                                + lng + '\n')