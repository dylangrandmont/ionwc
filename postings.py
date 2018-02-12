# Copyright (C) 2016-2018, Dylan Grandmont

from coordinatemapping import uwiToLatLng
from constants import FORMATION_AGE_DICT
from constants import KML_TEMPLATE
from constants import IONWC_HOME
from constants import UNKNOWN
from constants import MONTH_DICT
from constants import BC_POSTING_DATES_TO_SALE_DATE_MAP
from constants import SK_POSTING_NUMBER_TO_SALE_DATE
from utilities import writePostingOfferingDataBaseFile
from utilities import writePostingOfferingAggregateDataBaseFile
from utilities import writePostingResultDataBaseFile
from utilities import writePostingResultAggregateDataBaseFile
import xml.etree.ElementTree as ET
import glob
import locale
import re

##################################################################
# Posting Databases
##################################################################

class Database:
    def __init__(self, csvDatabase, header):
        self.csvDatabase = open(csvDatabase, 'w+')
        self.csvDatabase.write(header)
        self.rows = []

    def add_row(self, row):
        self.rows.append(row)

    def close(self):
        self.csvDatabase.close()

class PostingsDatabase(Database):
    def __init__(self, csvDatabase):
        Database.__init__(self, csvDatabase, "saleDate:contractType:contractNo:hectares:tractNo:uwi:topZone:baseZone:topAge:baseAge:geometry:province\n")

    def write_to_csv(self):
        for row in self.rows:
            writePostingOfferingDataBaseFile(self.csvDatabase,
                                            row.sale_date,
                                            row.contract_type,
                                            row.contract_number,
                                            row.hectares,
                                            row.tract_no,
                                            row.uwi,
                                            row.top_qualified_zone,
                                            row.base_qualified_zone,
                                            row.top_age,
                                            row.base_age,
                                            row.kml_polygon,
                                            row.province)

class PostingsAggregateDatabase(Database):
    def __init__(self, csvDatabase):
        Database.__init__(self, csvDatabase, "saleDate:contractType:contractNo:hectares:centerLat:centerLng:province\n")

    def write_to_csv(self):
        for row in self.rows:
            writePostingOfferingAggregateDataBaseFile(self.csvDatabase,
                                                      row.sale_date,
                                                      row.contract_type,
                                                      row.contract_number,
                                                      row.hectares,
                                                      row.aggregate_latitude,
                                                      row.aggregate_longitude,
                                                      row.province)

class ResultsDatabase(Database):
    def __init__(self, csvDatabase):
        Database.__init__(self, csvDatabase, "saleDate:status:bonus:dollarPerHectare:ClientDescription:contractType:contractNo:hectares:tractNo:uwi:topZone:baseZone:topAge:baseAge:geometry:province\n")

    def write_to_csv(self):
        for row in self.rows:
            writePostingResultDataBaseFile(self.csvDatabase,
                                           row.sale_date,
                                           row.status,
                                           row.bonus,
                                           row.dollar_per_hect,
                                           row.client_desc,
                                           row.contract_type,
                                           row.contract_number,
                                           row.hectares,
                                           row.tract_no,
                                           row.uwi,
                                           row.top_qualified_zone,
                                           row.base_qualified_zone,
                                           row.top_age, 
                                           row.base_age,
                                           row.kml_polygon,
                                           row.province)

class ResultsAggregateDatabase(Database):
    def __init__(self, csvDatabase):
        Database.__init__(self, csvDatabase, "saleDate:status:bonus:dollarPerHectare:ClientDescription:contractType:contractNo:hectares:centerLat:centerLng:province\n")

    def write_to_csv(self):
        for row in self.rows:
            writePostingResultAggregateDataBaseFile(self.csvDatabase,
                                                    row.sale_date,
                                                    row.status,
                                                    row.bonus,
                                                    row.dollar_per_hect,
                                                    row.client_desc,
                                                    row.contract_type,
                                                    row.contract_number,
                                                    row.hectares,
                                                    row.aggregate_latitude,
                                                    row.aggregate_longitude,
                                                    row.province)


##################################################################
# Posting Objects
##################################################################

class Posting:
    def __init__(self, sale_date, contract_type, contract_number, hectares, tract_no, uwi, top_qualified_zone,
                 base_qualified_zone, top_age, base_age, kml_polygon, province):

        self.sale_date = sale_date
        self.contract_type = contract_type
        self.contract_number = contract_number
        self.hectares = hectares
        self.tract_no = tract_no
        self.uwi = uwi
        self.top_qualified_zone = top_qualified_zone
        self.base_qualified_zone = base_qualified_zone
        self.top_age = top_age
        self.base_age = base_age
        self.kml_polygon = kml_polygon
        self.province = province

class PostingAggregate:
    def __init__(self, sale_date, contract_type, contract_number, hectares, aggregate_latitude, aggregate_longitude, province):

        self.sale_date = sale_date
        self.contract_type = contract_type
        self.contract_number = contract_number
        self.hectares = hectares
        self.aggregate_latitude = aggregate_latitude
        self.aggregate_longitude = aggregate_longitude
        self.province = province

class Result:
    def __init__(self, sale_date, status, bonus, dollar_per_hect, client_desc, contract_type, contract_number, hectares, tract_no, uwi, top_qualified_zone,
                 base_qualified_zone, top_age, base_age, kml_polygon, province):

        self.sale_date = sale_date
        self.status = status
        self.bonus = bonus
        self.dollar_per_hect = dollar_per_hect
        self.client_desc = client_desc
        self.contract_type = contract_type
        self.contract_number = contract_number
        self.hectares = hectares
        self.tract_no = tract_no
        self.uwi = uwi
        self.top_qualified_zone = top_qualified_zone
        self.base_qualified_zone = base_qualified_zone
        self.top_age = top_age
        self.base_age = base_age
        self.kml_polygon = kml_polygon
        self.province = province

class ResultAggregate:
    def __init__(self,
                 sale_date,
                 status,
                 bonus,
                 dollar_per_hect,
                 client_desc,
                 contract_type,
                 contract_number,
                 hectares,
                 aggregate_latitude,
                 aggregate_longitude,
                 province):

        self.sale_date = sale_date
        self.status = status
        self.bonus = bonus
        self.dollar_per_hect = dollar_per_hect
        self.client_desc = client_desc
        self.contract_type = contract_type
        self.contract_number = contract_number
        self.hectares = hectares
        self.aggregate_latitude = aggregate_latitude
        self.aggregate_longitude = aggregate_longitude
        self.province = province


##################################################################
# Posting Managers
##################################################################

class PostingsManager:
    def __init__(self, posting_database, posting_aggregates_database, results_database, results_aggregates_database):
        self.posting_database = posting_database
        self.posting_aggregates_database = posting_aggregates_database
        self.results_database = results_database
        self.results_aggregates_database = results_aggregates_database



##################################################################
# BCPosting Manager

class BCPostingsManager(PostingsManager):
    """ Manage parsing and population of licence database for BC """
    PAGE_HEADER_STRING = 'PAGE\s+[0-9]+.+\nDRILLING LICENCE.+\n.+\n.+\n.+\n.+'
    TRACT_STRING = 'TRACT\s+[0-9]+'
    TRACT_1_STRING = '([0-9]+\s+TRACT\s+1\s+[0-9]+)'


    def populate_databases(self):
        self._populate_posting_database()
        self._populate_results_database()


    def _populate_posting_database(self):
        """ Add all postings to the offerings database """
        posting_files  = self._get_postings_files()
        for posting_file in posting_files:
            postings, posting_aggregates = self._get_postings_from_file(posting_file)

            for posting in postings:
                self.posting_database.add_row(posting)

            for posting_aggregate in posting_aggregates:
                self.posting_aggregates_database.add_row(posting_aggregate)


    def _populate_results_database(self):
        """ Add all results to the offerings database """
        results_files  = self._get_results_files()
        for results_file in results_files:
            results, results_aggregates = self._get_results_from_file(results_file)
            for result in results:
                self.results_database.add_row(result)

            for results_aggregate in results_aggregates:
                self.results_aggregates_database.add_row(results_aggregate)


    def _get_postings_files(self):
        """ Retreive all the BC posting files """
        return glob.glob(IONWC_HOME + '/data/postings/bc/*sal.rpt')


    def _get_results_files(self):
        return glob.glob(IONWC_HOME + '/data/postings/bc/*res.rpt')


    def _get_postings_from_file(self, file):
        """ Return postings and aggregates of postings for a single file """

        postings = []
        posting_aggregates = []

        month = MONTH_DICT[file.split('/')[-1][:3].upper()]
        year = file.split('/')[-1][3:5]
        sale_date = '20' + year + '.' + month
        sale_date = BC_POSTING_DATES_TO_SALE_DATE_MAP[sale_date]

        lines = open(file).readlines()
        all_lines = ''.join(lines)
        all_lines = re.sub(self.PAGE_HEADER_STRING, '', all_lines)

        licence_index_end = all_lines.find('PETROLEUM AND NATURAL GAS LEASE')
        all_licences = all_lines[0:licence_index_end]
        all_leases = all_lines[licence_index_end:]

        contractType = "Licence"
        for parcels in [all_licences, all_leases]:
            all_parcels = re.compile(self.TRACT_1_STRING).split(parcels)
            del all_parcels[0]
            parcel_headers = all_parcels[0::2]
            parcel_contents = all_parcels[1::2]

            index = 0
            for parcel_content in parcel_contents:
                parcel_number = re.split('\s+', parcel_headers[index])[0]
                hectares = re.split('\s+', parcel_headers[index])[3]

                aggregate_latitudes = []
                aggregate_longitudes = []

                tracts = re.split(self.TRACT_STRING, parcel_content)
                tractNo = 1
                for tract in tracts:
                    top_qualifier, top_zone, base_qualifier, base_zone = self._findZoneRights(tract)
                    try:
                        top_age = FORMATION_AGE_DICT[top_zone.lower().strip()]
                    except:
                        raise Exception('No entry found in FORMATION_AGE_DICT for ' + top_zone)
                    try:
                        base_age = FORMATION_AGE_DICT[base_zone.lower().strip()]
                    except:
                        raise Exception('No entry found in FORMATION_AGE_DICT for ' + base_zone) 

                    dls_uwis = re.findall('TWP .+', tract)
                    nts_uwis = re.findall('NTS .[0-9]+.+', tract)

                    for uwi in dls_uwis:
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
                                    kml_polygon, center_latitude, center_longitude = self._uwi_to_kml_polygon([seci, twp, rng, mer], grid='dls')
                                    aggregate_latitudes.append(center_latitude)
                                    aggregate_longitudes.append(center_longitude)
                                    posting = Posting(sale_date, contractType, str(parcel_number), hectares, str(tractNo), uwi, top_qualifier + ' ' + top_zone, base_qualifier + ' ' + base_zone, str(top_age), str(base_age), kml_polygon, 'BC')
                                    postings.append(posting)
                            else:
                                kml_polygon, center_latitude, center_longitude = self._uwi_to_kml_polygon([sec, twp, rng, mer], grid='dls')
                                aggregate_latitudes.append(center_latitude)
                                aggregate_longitudes.append(center_longitude)
                                posting = Posting(sale_date, contractType, str(parcel_number), hectares, str(tractNo), uwi, top_qualifier + ' ' + top_zone, base_qualifier + ' ' + base_zone, str(top_age), str(base_age), kml_polygon, 'BC')
                                postings.append(posting)

                    for uwi in nts_uwis:
                        uwi = uwi.strip()
                        uwi_no_units = re.findall(r"[A-Z]+.[0-9]+-[A-Z]-[0-9]+ BLK [A-Z] UNITS ", uwi)[0]
                        units = uwi.replace(uwi_no_units, '')
                        units = units.split()

                        uwi_no_units = re.findall(r"[\w']+", uwi_no_units)
                        sheetNumber = uwi_no_units[3]
                        sheetLetter = uwi_no_units[2]
                        series = uwi_no_units[1]
                        block = uwi_no_units[5]

                        for unit in units:
                            if '-' in unit:
                                start_unit = int( unit.split('-')[0] )
                                end_unit = int( unit.split('-')[1] )
                                for uniti in range(start_unit, end_unit + 1):
                                    uniti = str(uniti)
                                    kml_polygon, center_latitude, center_longitude = self._uwi_to_kml_polygon([uniti, block, series, sheetLetter, sheetNumber], grid='nts')
                                    aggregate_latitudes.append(center_latitude)
                                    aggregate_longitudes.append(center_longitude)
                                    uwi = 'Unit ' + uniti + '; Block ' + block + '; Series ' + series + '; Sheet ' + sheetLetter + sheetNumber

                                    posting = Posting(sale_date,
                                                      contractType,
                                                      str(parcel_number),
                                                      hectares,
                                                      str(tractNo),
                                                      uwi,
                                                      top_qualifier + ' ' + top_zone,
                                                      base_qualifier + ' ' + base_zone,
                                                      str(top_age),
                                                      str(base_age),
                                                      kml_polygon,
                                                      'BC')
                                    postings.append(posting)
                            else:
                                kml_polygon, center_latitude, center_longitude = self._uwi_to_kml_polygon([unit, block, series, sheetLetter, sheetNumber], grid='nts')
                                aggregate_latitudes.append(center_latitude)
                                aggregate_longitudes.append(center_longitude)
                                uwi = 'Unit ' + unit + '; Block ' + block + '; Series ' + series + '; Sheet ' + sheetLetter + sheetNumber

                                posting = Posting(sale_date, 
                                                  contractType,
                                                  str(parcel_number),
                                                  hectares,
                                                  str(tractNo),
                                                  uwi,
                                                  top_qualifier + ' ' + top_zone,
                                                  base_qualifier + ' ' + base_zone,
                                                  str(top_age),
                                                  str(base_age),
                                                  kml_polygon,
                                                  'BC')
                                postings.append(posting)

                    tractNo += 1

                aggregateLatitude = sum(aggregate_latitudes) / len(aggregate_latitudes)
                aggregateLongitude = sum(aggregate_longitudes) / len(aggregate_longitudes)
                posting_aggregate = PostingAggregate(sale_date, contractType, parcel_number, hectares, str(aggregateLatitude), str(aggregateLongitude), 'BC')
                posting_aggregates.append(posting_aggregate)
                index += 1
            contractType = "Lease"

        return postings, posting_aggregates


    def _get_results_from_file(self, file):

        results = []
        results_aggregates = []

        results_file_contents = ''.join(open(file).readlines())
        result_entries = re.findall('[a-zA-Z].+[0-9]+[\s]+[0-9]+.+[a-zA-Z].+[0-9].+\$.+', results_file_contents)

        for result_entry in result_entries:
            resultDelimited = re.split('\s\s+', result_entry)
            contract_number = resultDelimited[1]
            hectares = resultDelimited[2]
            client = resultDelimited[3].title()
            working_interest = resultDelimited[4]
            dollar_per_hect = resultDelimited[5]
            bonus = resultDelimited[6]

            client_desc = client + ' ' + '%d' % float(working_interest) + '%'

            if 'no bids or no acceptable bids' in re.split('\s\s+', result_entry)[3].lower():
                status = 'No Offers'
            else:
                status = 'Accepted'

            matching_offerings_aggregates = []
            for row in self.posting_aggregates_database.rows:
                if (contract_number == row.contract_number) and (row.province == 'BC'):
                    matching_offerings_aggregates.append(row)

            if len(matching_offerings_aggregates) == 1:
                aggregate_latitude = matching_offerings_aggregates[0].aggregate_latitude
                aggregate_longitude = matching_offerings_aggregates[0].aggregate_longitude
            else:
                raise Exception('No matching offering aggregates found for contract: ', contract_number, result_entry, file)

            matching_offerings = []

            for row in self.posting_database.rows:
                if (contract_number == row.contract_number) and (row.province == 'BC'):
                    matching_offerings.append(row)

            firstContract = True;
            for matching_offering in matching_offerings:
                sale_date = matching_offering.sale_date
                contract_type = matching_offering.contract_type
                hectares = matching_offering.hectares
                tract_number = matching_offering.tract_no
                uwi = matching_offering.uwi
                top_zone = matching_offering.top_qualified_zone
                base_zone = matching_offering.base_qualified_zone
                top_age = matching_offering.top_age
                base_age = matching_offering.base_age
                kml_polygon = matching_offering.kml_polygon

                result = Result(sale_date,
                                status,
                                bonus,
                                dollar_per_hect,
                                client_desc,
                                contract_type,
                                contract_number,
                                hectares,
                                tract_number,
                                uwi,
                                top_zone,
                                base_zone,
                                top_age,
                                base_age,
                                kml_polygon,
                                'BC')
                results.append(result)

                if firstContract:
                    result_aggregate = ResultAggregate(sale_date,
                                                       status,
                                                       bonus,
                                                       dollar_per_hect,
                                                       client_desc,
                                                       contract_type,
                                                       contract_number,
                                                       hectares,
                                                       str(aggregate_latitude),
                                                       str(aggregate_longitude),
                                                       'BC')
                    results_aggregates.append(result_aggregate)

                firstContract = False

        return results, results_aggregates


    def _findZoneRights(self, tract):
        if len(re.findall('BELOW BASE OF', tract)) != 0:
            zone_rights = re.findall('BELOW BASE OF [0-9].+', tract)[0].strip()
            top_qualifier = 'From The Base Of The'    
            top_zone = re.split(' [(].+', re.split('BELOW BASE OF [0-9]+ ', zone_rights)[1])[0]
            base_qualifier = 'To'
            base_zone = 'Basement'

        elif len(re.findall('ALL ZONES', tract)) != 0:
            top_qualifier = 'From'
            top_zone = 'Surface'
            base_qualifier = 'To'
            base_zone = 'Basement'

        elif len(re.findall('IN\s+[0-9]+\s+[A-Z]+', tract)) != 0:
            top_qualifier = 'From The Top Of The'
            top_zone = re.findall('IN\s+[0-9]+\s+[A-Z]+', tract)[0].split()[-1]
            base_qualifier = 'To The Base Of The'
            base_zone = top_zone

        elif len(re.findall('DOWN TO BASE OF.+', tract)) != 0:
            zone_rights = re.findall('DOWN TO BASE OF.+', tract)[0].strip()
            top_qualifier = 'From'
            top_zone = 'Surface'
            base_qualifier = 'To The Base Of The'
            base_zone = re.split(' [(].+', re.split('DOWN TO BASE OF [0-9]+ ', zone_rights)[1])[0]

        else:
            raise Exception('No subsurface rights found for tract', tract)

        top_zone = top_zone.title()
        base_zone = base_zone.title()

        return top_qualifier, top_zone, base_qualifier, base_zone


    def _uwi_to_kml_polygon(self, uwi, grid = 'dls'):

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

      kml_polygon = KML_TEMPLATE % (se_lng, se_lat, sw_lng, sw_lat, nw_lng, nw_lat, ne_lng, ne_lat)

      center_latitude = (se_lat + nw_lat) / 2.0
      center_longitude = (se_lng + nw_lng) / 2.0

      return kml_polygon, center_latitude, center_longitude




##################################################################
# ABPosting Manager

class ABPostingsManager(PostingsManager):
    """ Manage parsing and population of licence database for AB """

    def populate_databases(self):
        self._populate_posting_database()
        self._populate_results_database()


    def _populate_posting_database(self):
        """ Add all postings to the offerings database """
        posting_files  = self._get_postings_files()
        for posting_file in posting_files:
            postings, posting_aggregates = self._get_postings_from_file(posting_file)

            for posting in postings:
                self.posting_database.add_row(posting)

            for posting_aggregate in posting_aggregates:
                self.posting_aggregates_database.add_row(posting_aggregate)


    def _populate_results_database(self):
        """ Add all results to the offerings database """
        results_files  = self._get_results_files()
        for results_file in results_files:
            results, results_aggregates = self._get_results_from_file(results_file)
            for result in results:
                self.results_database.add_row(result)

            for results_aggregate in results_aggregates:
                self.results_aggregates_database.add_row(results_aggregate)


    def _get_postings_files(self):
        """ Retreive all the AB posting files """
        return glob.glob(IONWC_HOME + '/data/postings/ab/*PON.xml')


    def _get_results_files(self):
        """ Retreive all the AB results files """
        return glob.glob(IONWC_HOME + '/data/postings/ab/*PSR.xml')        


    def _get_postings_from_file(self, file):
        """ From each AB postings file, find all patterns for posting contracts """
        tree = ET.parse(file)
        root = tree.getroot()

        postings = []
        postingAggregates = []

        namespace = "{http://tempuri.org/PON.xsd}"
        sale_date = root.find(".//" + namespace + "SaleDate").text.replace('-','.')
        schedules = root.findall(".//" + namespace + "Schedule")

        for schedule in schedules:
            contract_type = schedule.find(".//" + namespace + "ContractType").text.title()
            contracts = schedule.findall(".//" + namespace + "Contract")

            for contract in contracts:
                contract_number = contract.find(".//" + namespace + "ContractNo").text
                hectares = contract.find(".//" + namespace + "Hectares").text
                tracts = contract.findall(".//" + namespace + "Tract")

                aggregate_latitudes = []
                aggregate_longitudes = []

                for tract in tracts:
                    tract_no = tract.find(".//" + namespace + "TractNo").text
                    lands = tract.findall(".//" + namespace + "Land")
                    base_zone = ''
                    top_zone = ''
                    lines = tract.findall(".//" + namespace + "Line")
                    top_qualifier = lines[0].find(".//" + namespace + "Qualifier").text.title()
                    top_zone = lines[0].find(".//" + namespace + "ZoneName").text.title()
                    base_qualifier = lines[1].find(".//" + namespace + "Qualifier").text.title()
                    base_zone = lines[1].find(".//" + namespace + "ZoneName").text.title()

                    for land in lands:
                        landKey = land.find(".//" + namespace + "LandKey").text
                        landKey += '       '
                        mer = landKey[0]
                        rng = landKey[1:3]
                        twp = landKey[3:6]
                        sec = landKey[6:8]
                        lsd = landKey[8:10]
                        uwi =  lsd + '-' + sec + '-' + twp + '-' + rng + 'W' + mer

                        kml_polygon, center_latitude, center_longitude = self._uwi_to_kml_polygon(uwi, lsd, sec, twp, rng, mer)
                        aggregate_latitudes.append(center_latitude)
                        aggregate_longitudes.append(center_longitude)

                        try:
                            top_age = FORMATION_AGE_DICT[top_zone.lower().replace(' fm', '').replace(' sd', '').replace(' grp', '').replace(' mbr', '').replace(' ss', '').replace('zone', '').strip()]
                            base_age = FORMATION_AGE_DICT[base_zone.lower().replace(' fm', '').replace(' sd', '').replace(' grp', '').replace(' mbr', '').replace(' ss', '').replace('zone', '').strip()]
                        except:
                            raise Exception('No entry found in FORMATION_AGE_DICT for ', top_zone, base_zone)

                        posting = Posting(sale_date, contract_type, contract_number, hectares, tract_no, uwi, top_qualifier + ' ' + top_zone, base_qualifier + ' ' + base_zone, top_age, base_age, kml_polygon, 'AB')
                        postings.append(posting)

                aggregateLatitude = sum(aggregate_latitudes) / len(aggregate_latitudes)
                aggregateLongitude = sum(aggregate_longitudes) / len(aggregate_longitudes)
                postingAggregate = PostingAggregate(sale_date, contract_type, contract_number, hectares, str(aggregateLatitude), str(aggregateLongitude), 'AB')
                postingAggregates.append(postingAggregate)

        return postings, postingAggregates


    def _get_results_from_file(self, file):
        tree = ET.parse(file)
        root = tree.getroot()
        
        results = []
        results_aggregates = []

        locale.setlocale(locale.LC_ALL, '')

        namespace = ''
        sale_date = root.find(".//" + namespace + "SaleDate").text.replace('/','.')
        parcels = root.findall(".//" + namespace + "Parcel")
        for parcel in parcels:
            parcel_number = parcel.find(".//" + namespace + "ParcelNumber").text
            contractFlag = parcel.find(".//" + namespace + "ContractFlag").text
            contract_number = contractFlag + parcel_number

            status = parcel.find(".//" + namespace + "Status").text.title()
            bonus = ''
            dollar_per_hect = ''
            if status == 'Accepted':
                bonus = locale.currency( float( parcel.find(".//" + namespace + "Bonus").text ), grouping = True)
                dollar_per_hect = locale.currency( float( parcel.find(".//" + namespace + "DollarPerHectare").text ), grouping=True)
            
            client_desc = ''
            clients = parcel.findall(".//" + namespace + "Clients")
            for client in clients:
                try:
                    clientName = client.find(".//" + namespace + "ClientName").text.title()
                    percentage = '%d' % float(client.find(".//" + namespace + "Percentage").text) + '%'
                    client_desc += clientName + " " + percentage + " "
                except: 
                    pass

            aggregate_latitude = '0'
            aggregate_longitude = '0'
            for row in self.posting_aggregates_database.rows:
                if (contract_number == row.contract_number) and (sale_date == row.sale_date) and (row.province == 'AB'):
                    aggregate_latitude = row.aggregate_latitude
                    aggregate_longitude = row.aggregate_longitude

            for row in self.posting_database.rows:
                if (contract_number == row.contract_number) and (sale_date == row.sale_date) and (row.province == 'AB'):

                    contract_type = row.contract_type
                    hectares = row.hectares
                    tract_number = row.tract_no
                    uwi = row.uwi
                    top_zone = row.top_qualified_zone
                    base_zone = row.base_qualified_zone
                    top_age = row.top_age
                    base_age = row.base_age
                    kml_polygon = row.kml_polygon

                    result = Result(row.sale_date,
                                    status,
                                    bonus,
                                    dollar_per_hect,
                                    client_desc,
                                    contract_type,
                                    contract_number,
                                    hectares,
                                    tract_number,
                                    uwi,
                                    top_zone,
                                    base_zone,
                                    top_age,
                                    base_age,
                                    kml_polygon,
                                    'AB')
                    results.append(result)

            result_aggregate = ResultAggregate(sale_date, status, bonus, dollar_per_hect, client_desc, contract_type, contract_number, hectares, str(aggregate_latitude), str(aggregate_longitude), 'AB')
            results_aggregates.append(result_aggregate)  

        return results, results_aggregates


    def _uwi_to_kml_polygon(self, uwi, lsd, sec, twp, rng, mer):
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

        kml_polygon = KML_TEMPLATE % (se_lng, se_lat, sw_lng, sw_lat, nw_lng, nw_lat, ne_lng, ne_lat)

        center_latitude = (se_lat + nw_lat) / 2.0
        center_longitude = (se_lng + nw_lng) / 2.0

        return kml_polygon, center_latitude, center_longitude




##################################################################
# SKPosting Manager


class SKPostingsManager(PostingsManager):
    """ Manage parsing and population of licence database for SK """
    TOP_QUALIFIER = 'From'
    BASE_QUALIFIER = 'To'

    def populate_databases(self):
        self._populate_posting_database()
        self._populate_results_database()


    def _populate_posting_database(self):
        """ Add all postings to the offerings database """
        posting_files  = self._get_postings_files()
        for posting_file in posting_files:
            postings, posting_aggregates = self._get_postings_from_file(posting_file)

            for posting in postings:
                self.posting_database.add_row(posting)

            for posting_aggregate in posting_aggregates:
                self.posting_aggregates_database.add_row(posting_aggregate)


    def _populate_results_database(self):
        """ Add all results to the offerings database """
        results_files  = self._get_results_files()
        for results_file in results_files:
            results, results_aggregates = self._get_results_from_file(results_file)
            for result in results:
                self.results_database.add_row(result)

            for results_aggregate in results_aggregates:
                self.results_aggregates_database.add_row(results_aggregate)


    def _get_postings_files(self):
        """ Retreive all the SK posting files """
        return glob.glob(IONWC_HOME + '/data/postings/sk/*otice*.txt')


    def _get_results_files(self):
        """ Retreive all the SK results files """
        return glob.glob(IONWC_HOME + '/data/postings/sk/*result*.txt')


    def _get_postings_from_file(self, file):
        postings = []
        posting_aggregates = []

        file_contents = ''.join(open(file).readlines())

        licences = re.split('Petroleum and Natural Gas Exploration Licence', file_contents)
        if len(licences) > 1:
            leases = re.split('Petroleum and Natural Gas Lease', licences[1])[1]
            licences = ''.join(re.split('Petroleum and Natural Gas Lease', licences[1])[0])
        else:
            licences = ''
            leases = re.split('Petroleum and Natural Gas Lease', file_contents)[1]

        sale_number = re.findall('PUBLIC NOTICE [0-9]+', file_contents)[0].split()[2]
        sale_date = SK_POSTING_NUMBER_TO_SALE_DATE[sale_number]
        entries = re.findall('.+[0-9]+.[0-9]+\s+Oil and Gas+.+', file_contents)

        for entry in entries:

            if entry in licences:
                contract_type = 'Licence'
            elif entry in leases:
                contract_type = 'Lease'
            else:
                contract_type = ''
                print 'ERROR: no valid contract type found for entry ', entry

            coordinates = re.findall('[\w]+', re.split('[0-9]+\.[0-9]+', entry)[0])

            # Check if new parcel has been reached
            if entry[0:3].strip().isdigit():
                contract_number = entry[0:3].strip()
                coordinates = coordinates[1:]
                tract_no = 1

                posting_aggregate = PostingAggregate(sale_date, contract_type, contract_number, 0, 0, 0, 'SK')
                posting_aggregates.append(posting_aggregate)

            if coordinates[0] == 'PTN': 
                coordinates = coordinates[1:]
            elif coordinates[0] == 'FRAC':
                coordinates = coordinates[1:]

            hectares = re.findall('[0-9]+\.[0-9]+',entry)[0]
            posting_aggregates[-1].hectares += float(hectares)

            top_zone = re.split('\s\s+', re.split('Oil and Gas', entry)[1])[1].title()
            base_zone = re.split('\s\s+', re.split('Oil and Gas', entry)[1])[2].title()

            top_age = FORMATION_AGE_DICT[top_zone.lower()]
            base_age = FORMATION_AGE_DICT[base_zone.lower()]

            kml_polygon, uwi, centerLatitude, centerLongitude = self._uwi_to_kml_polygon(coordinates)

            posting_aggregates[-1].aggregate_latitude *= (tract_no - 1) / float(tract_no)
            posting_aggregates[-1].aggregate_longitude *= (tract_no - 1) / float(tract_no)

            posting_aggregates[-1].aggregate_latitude += ((1.0) / float(tract_no)) * centerLatitude
            posting_aggregates[-1].aggregate_longitude += ((1.0) / float(tract_no)) * centerLongitude

            posting = Posting(sale_date,
                              contract_type,
                              contract_number,
                              hectares,
                              tract_no,
                              uwi,
                              self.TOP_QUALIFIER + ' ' + top_zone,
                              self.BASE_QUALIFIER + ' ' + base_zone,
                              top_age,
                              base_age, 
                              kml_polygon,
                              'SK')
            postings.append(posting)
            tract_no += 1

        return postings, posting_aggregates



    def _get_results_from_file(self, file):

        results = []
        results_aggregates = []

        file_contents = ''.join(open(file).readlines()).replace(',', '')

        saleNumberLine = re.findall('Sale [0-9]+', file_contents)

        if len(saleNumberLine) < 1:
            saleNumberLine = re.findall('Public Offering [0-9]+', file_contents)  

        saleNumber = re.findall('[0-9]+', saleNumberLine[0])[0]
        sale_date = SK_POSTING_NUMBER_TO_SALE_DATE[saleNumber]

        no_submitted_bids = re.findall('.+No Bids Submitted', file_contents)
        no_acceptable_bids = re.findall('.+No Acceptable Bids', file_contents)
        accepted_bids_multiple_interests = re.findall('\n[0-9]+[\s]+[\w]+.+[0-9]+[\s]+[0-9]+.[0-9]+[\s]+[0-9]+.[0-9]+\n                       [a-zA-Z].+               [0-9]+.[0-9]+', file_contents)
        accepted_bids_one_interests = re.findall('\n[0-9]+[\s]+[\w]+.+100[\s]+[0-9]+.[0-9]+[\s]+[0-9]+\.[0-9]+[\s]+[0-9]+\.[0-9]+', file_contents)

        for no_acceptable_bid in no_acceptable_bids:
            status = 'No Acceptable Offers'
            bonus = ''
            dollar_per_hect = ''
            client_desc = ''
            contract_number = no_acceptable_bid.split()[0]

            aggregate_latitude = '0'
            aggregate_longitude = '0'
            for row in self.posting_aggregates_database.rows:
                if (contract_number == row.contract_number) and (sale_date == row.sale_date) and (row.province == 'SK'):
                    aggregate_latitude = row.aggregate_latitude
                    aggregate_longitude = row.aggregate_longitude
                    break


            offering_contracts = []
            for row in self.posting_database.rows:
                if (contract_number == row.contract_number) and (sale_date == row.sale_date) and (row.province == 'SK'):
                    offering_contracts.append(row)

            total_hectares = 0

            for offering_contract in offering_contracts:
                contract_type = offering_contract.contract_type
                hectares = offering_contract.hectares
                total_hectares += float(hectares)
                tract_number = offering_contract.tract_no
                uwi = offering_contract.uwi
                top_zone = offering_contract.top_qualified_zone
                base_zone = offering_contract.base_qualified_zone
                top_age = offering_contract.top_age
                base_age = offering_contract.base_age
                kml_polygon = offering_contract.kml_polygon

                result = Result(sale_date,
                                status,
                                bonus,
                                dollar_per_hect,
                                client_desc,
                                contract_type,
                                contract_number,
                                hectares,
                                tract_number,
                                uwi,
                                top_zone,
                                base_zone,
                                top_age,
                                base_age,
                                kml_polygon,
                                'SK')
                results.append(result)

            if len(offering_contracts) > 0:
                results_aggregate = ResultAggregate(sale_date,
                                                    status,
                                                    bonus,
                                                    dollar_per_hect,
                                                    client_desc,
                                                    contract_type,
                                                    contract_number,
                                                    total_hectares,
                                                    str(aggregate_latitude),
                                                    str(aggregate_longitude),
                                                    'SK')
                results_aggregates.append(results_aggregate)
 
        for no_submitted_bid in no_submitted_bids:
            status =  'No Offers'
            bonus = ''
            dollar_per_hect = ''
            client_desc = ''
            contract_number = no_submitted_bid.split()[0]

            aggregate_latitude = '0'
            aggregate_longitude = '0'
            for row in self.posting_aggregates_database.rows:
                if (contract_number == row.contract_number) and (sale_date == row.sale_date) and (row.province == 'SK'):
                    aggregate_latitude = row.aggregate_latitude
                    aggregate_longitude = row.aggregate_longitude
                    break


            offering_contracts = []
            for row in self.posting_database.rows:
                if (contract_number == row.contract_number) and (sale_date == row.sale_date) and (row.province == 'SK'):
                    offering_contracts.append(row)

            total_hectares = 0

            for offering_contract in offering_contracts:
                contract_type = offering_contract.contract_type
                hectares = offering_contract.hectares
                total_hectares += float(hectares)
                tract_number = offering_contract.tract_no
                uwi = offering_contract.uwi
                top_zone = offering_contract.top_qualified_zone
                base_zone = offering_contract.base_qualified_zone
                top_age = offering_contract.top_age
                base_age = offering_contract.base_age
                kml_polygon = offering_contract.kml_polygon

                result = Result(sale_date,
                                status,
                                bonus,
                                dollar_per_hect,
                                client_desc,
                                contract_type,
                                contract_number,
                                hectares,
                                tract_number,
                                uwi,
                                top_zone,
                                base_zone,
                                top_age,
                                base_age,
                                kml_polygon,
                                'SK')
                results.append(result)

            if len(offering_contracts) > 0:
                results_aggregate = ResultAggregate(sale_date,
                                                    status,
                                                    bonus,
                                                    dollar_per_hect,
                                                    client_desc,
                                                    contract_type,
                                                    contract_number,
                                                    total_hectares,
                                                    str(aggregate_latitude),
                                                    str(aggregate_longitude),
                                                    'SK')
                results_aggregates.append(results_aggregate)

        for accepted_bids_multiple_interest in accepted_bids_multiple_interests:
            status = 'Accepted'
            numbers = re.findall('[^\s][0-9]+[^\s]+[0-9]+[^\s]', accepted_bids_multiple_interest)
            bonus = numbers[-4]
            dollar_per_hect = numbers[-2]
            clientArray = re.split('[\s][\s]+', accepted_bids_multiple_interest)
            client_desc = clientArray[2] + ' ' + clientArray[3] + '%'
            client_desc += clientArray[7] + ' '+ clientArray[8] + '%'
            
            contract_number = accepted_bids_multiple_interest.split()[0]

            aggregate_latitude = '0'
            aggregate_longitude = '0'
            for row in self.posting_aggregates_database.rows:
                if (contract_number == row.contract_number) and (sale_date == row.sale_date) and (row.province == 'SK'):
                    aggregate_latitude = row.aggregate_latitude
                    aggregate_longitude = row.aggregate_longitude
                    break


            offering_contracts = []
            for row in self.posting_database.rows:
                if (contract_number == row.contract_number) and (sale_date == row.sale_date) and (row.province == 'SK'):
                    offering_contracts.append(row)

            total_hectares = 0

            for offering_contract in offering_contracts:
                contract_type = offering_contract.contract_type
                hectares = offering_contract.hectares
                total_hectares += float(hectares)
                tract_number = offering_contract.tract_no
                uwi = offering_contract.uwi
                top_zone = offering_contract.top_qualified_zone
                base_zone = offering_contract.base_qualified_zone
                top_age = offering_contract.top_age
                base_age = offering_contract.base_age
                kml_polygon = offering_contract.kml_polygon

                result = Result(sale_date,
                                status,
                                bonus,
                                dollar_per_hect,
                                client_desc,
                                contract_type,
                                contract_number,
                                hectares,
                                tract_number,
                                uwi,
                                top_zone,
                                base_zone,
                                top_age,
                                base_age,
                                kml_polygon,
                                'SK')
                results.append(result)

            if len(offering_contracts) > 0:
                results_aggregate = ResultAggregate(sale_date,
                                                    status,
                                                    bonus,
                                                    dollar_per_hect,
                                                    client_desc,
                                                    contract_type,
                                                    contract_number,
                                                    total_hectares,
                                                    str(aggregate_latitude),
                                                    str(aggregate_longitude),
                                                    'SK')
                results_aggregates.append(results_aggregate)

        for accepted_bids_one_interest in accepted_bids_one_interests:
            status = 'Accepted'
            decimals = re.findall('[^\s][0-9]*\.+[0-9]*[^\s]', accepted_bids_one_interest)
            bonus = decimals[-3]
            dollar_per_hect = decimals[-1]
            client = re.split('[\s][\s]+', accepted_bids_one_interest)[2]
            workingInterest = re.split('[\s][\s]+', accepted_bids_one_interest)[3]
            client_desc = client + ' ' + workingInterest + '% '
            contract_number = accepted_bids_one_interest.split()[0]

            aggregate_latitude = '0'
            aggregate_longitude = '0'
            for row in self.posting_aggregates_database.rows:
                if (contract_number == row.contract_number) and (sale_date == row.sale_date) and (row.province == 'SK'):
                    aggregate_latitude = row.aggregate_latitude
                    aggregate_longitude = row.aggregate_longitude
                    break


            offering_contracts = []
            for row in self.posting_database.rows:
                if (contract_number == row.contract_number) and (sale_date == row.sale_date) and (row.province == 'SK'):
                    offering_contracts.append(row)

            total_hectares = 0

            for offering_contract in offering_contracts:
                contract_type = offering_contract.contract_type
                hectares = offering_contract.hectares
                total_hectares += float(hectares)
                tract_number = offering_contract.tract_no
                uwi = offering_contract.uwi
                top_zone = offering_contract.top_qualified_zone
                base_zone = offering_contract.base_qualified_zone
                top_age = offering_contract.top_age
                base_age = offering_contract.base_age
                kml_polygon = offering_contract.kml_polygon

                result = Result(sale_date,
                                status,
                                bonus,
                                dollar_per_hect,
                                client_desc,
                                contract_type,
                                contract_number,
                                hectares,
                                tract_number,
                                uwi,
                                top_zone,
                                base_zone,
                                top_age,
                                base_age,
                                kml_polygon,
                                'SK')
                results.append(result)

            if len(offering_contracts) > 0:
                results_aggregate = ResultAggregate(sale_date,
                                                    status,
                                                    bonus,
                                                    dollar_per_hect,
                                                    client_desc,
                                                    contract_type,
                                                    contract_number,
                                                    total_hectares,
                                                    str(aggregate_latitude),
                                                    str(aggregate_longitude),
                                                    'SK')
                results_aggregates.append(results_aggregate)

        return results, results_aggregates


    def _uwi_to_kml_polygon(self, coordinates):
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





##################################################################
# MBPosting Manager


class MBPostingsManager(PostingsManager):
    """ Manage parsing and population of licence database for MB """
    PROVINCE = 'MB'
    CONTRACT_TYPE = 'Lease'
    TRACT_NUMBER = 1
    TOP_ZONE = 'Surface'
    TOP_QUALIFIER = 'From'
    BASE_ZONE = 'Basement'
    BASE_QUALIFIER = 'To'
    TOP_AGE = 0
    BASE_AGE = 9999


    def populate_databases(self):
        self._populate_posting_database()
        self._populate_results_database()


    def _populate_posting_database(self):
        """ Add all postings to the offerings database """
        posting_files  = self._get_postings_files()
        for posting_file in posting_files:
            postings, posting_aggregates = self._get_postings_from_file(posting_file)

            for posting in postings:
                self.posting_database.add_row(posting)

            for posting_aggregate in posting_aggregates:
                self.posting_aggregates_database.add_row(posting_aggregate)


    def _populate_results_database(self):
        """ Add all results to the offerings database """
        results_files  = self._get_results_files()
        for results_file in results_files:
            results, results_aggregates = self._get_results_from_file(results_file)
            for result in results:
                self.results_database.add_row(result)

            for results_aggregate in results_aggregates:
                self.results_aggregates_database.add_row(results_aggregate)


    def _get_postings_files(self):
        """ Retreive all the SK posting files """
        return glob.glob(IONWC_HOME + '/data/postings/mb/*sale.txt')


    def _get_results_files(self):
        """ Retreive all the SK results files """
        return glob.glob(IONWC_HOME + '/data/postings/mb/*results.txt')


    def _get_postings_from_file(self, file):
        file_contents = ''.join(open(file).readlines())

        postings = []
        posting_aggregates = []
        sale_date = self._get_sale_date(file_contents)

        postings_entries = re.findall('\n[\s]+[\w]+[\s]+\*?.+[0-9]+\s+[0-9]+\s+[\w]+\s+[0-9]+', file_contents)
        for posting_entry in postings_entries:
            posting_entry = posting_entry.replace('*', '')
            posting_entry = posting_entry.replace('\n\n', '')
            postingArray = re.split('\s\s\s\s+', posting_entry)
            contract_number = postingArray[0].strip()
            sec = postingArray[1]
            twp = '%03d' % int(postingArray[2])
            rng = '%02d' % int(postingArray[3])
            mer = postingArray[4]
            if mer == 'WPM':
                mer = '1'

            uwi = twp + '-' + rng + 'W' + mer
            kml_polygon, aggregateLatitude, aggregateLongitude = self._uwi_to_kml_polygon([sec, twp, rng, mer])

            hectares = postingArray[5]

            posting = Posting(sale_date,
                              self.CONTRACT_TYPE,
                              contract_number,
                              hectares,
                              self.TRACT_NUMBER,
                              uwi,
                              self.TOP_QUALIFIER + ' ' + self.TOP_ZONE,
                              self.BASE_QUALIFIER + ' ' + self.BASE_ZONE,
                              self.TOP_AGE,
                              self.BASE_AGE, 
                              kml_polygon,
                              'MB')
            postings.append(posting)

            posting_aggregate = PostingAggregate(sale_date,
                                                 self.CONTRACT_TYPE, 
                                                 contract_number,
                                                 hectares,
                                                 aggregateLatitude,
                                                 aggregateLongitude,
                                                 'MB')
            posting_aggregates.append(posting_aggregate)

        return postings, posting_aggregates


    def _get_results_from_file(self, file):
        results = []
        results_aggregates = []

        file_contents = ''.join(open(file).readlines())

        sale_date = self._get_sale_date(file_contents)

        postings = re.findall('[\w]+[\s]+[0-9]+[\s]+[0-9]+[\s]+.{0,50}[0-9].+\.[0-9]+', file_contents)
        for posting in postings:
            contract_number = posting.split()[0]
            posting.split()[-1]
            bonus = posting.split()[-5]
            dollar_per_hect = posting.split()[-4]


            for row in self.posting_aggregates_database.rows:
                if (contract_number == row.contract_number) and (sale_date == row.sale_date) and (row.province == 'MB'):
                    aggregate_latitude = row.aggregate_latitude
                    aggregate_longitude = row.aggregate_longitude


            offering_contracts = []
            for row in self.posting_database.rows:
                if (contract_number == row.contract_number) and (sale_date == row.sale_date) and (row.province == 'MB'):
                    offering_contracts.append(row)

            for offering_contract in offering_contracts:
                contract_type = offering_contract.contract_type
                hectares = offering_contract.hectares
                tract_number = offering_contract.tract_no
                uwi = offering_contract.uwi
                top_zone = offering_contract.top_qualified_zone
                base_zone = offering_contract.base_qualified_zone
                top_age = offering_contract.top_age
                base_age = offering_contract.base_age
                kml_polygon = offering_contract.kml_polygon

            if 'No Acceptable Bid' in posting:
                status = 'No Acceptable Offers'
                client_desc = ''
            else:
                status = 'Accepted'
                client_desc = re.split('\s\s\s+', posting)[5] + ' 100%'

                result = Result(sale_date,
                                status,
                                bonus,
                                dollar_per_hect,
                                client_desc,
                                contract_type,
                                contract_number,
                                hectares,
                                tract_number,
                                uwi,
                                top_zone,
                                base_zone,
                                top_age,
                                base_age,
                                kml_polygon,
                                'MB')
                results.append(result)

                results_aggregate = ResultAggregate(sale_date,
                                                    status,
                                                    bonus,
                                                    dollar_per_hect,
                                                    client_desc,
                                                    contract_type,
                                                    contract_number,
                                                    hectares,
                                                    str(aggregate_latitude),
                                                    str(aggregate_longitude),
                                                    'MB')

                results_aggregates.append(results_aggregate)

        return results, results_aggregates


    def _get_sale_date(self, file_contents):
        closing_date = re.findall('[\w]+ [0-9]+\, [0-9][0-9][0-9][0-9]', file_contents)[0]

        year = closing_date.split()[2]
        day = '%02d' % int(closing_date.split()[1].replace(',', ''))
        month = MONTH_DICT[closing_date.split()[0].upper()]

        return year + '.' + month + '.' + day


    def _uwi_to_kml_polygon(self, uwi):
        kml_polygon = ""

        sec = uwi[0]
        twp = uwi[1]
        rng = uwi[2]
        mer = uwi[3]

        all_sections = re.findall('All [0-9]+', sec)

        quarter_sections = []
        half_sections = []
        lsd_string = []
        lsd_numbers = []

        aggregate_latitudes = []
        aggregate_longitudes = []

        try:
            section = re.findall('of [0-9]+', sec)[0].split()[1]
            quarter_sections = re.findall('[A-Z][A-Z]\xc2\xbc', sec)
            half_sections = re.findall('[A-Z]\xc2\xbd', sec)
            lsd_string = re.findall('Lsd.\'s .+ of', sec)
            if len(lsd_string) > 0:
                lsd_numbers = re.findall('[0-9]+', lsd_string[0])
        except:
            section =  all_sections[0].split()[1]

        for all_section in all_sections:
            se_uwi = '01' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            sw_uwi = '04' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            nw_uwi = '13' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            ne_uwi = '16' + '-' + section + '-' + twp + '-' + rng + 'W' + mer

            se_lat, se_lng = uwiToLatLng.convert(se_uwi, position = "se")
            sw_lat, sw_lng = uwiToLatLng.convert(sw_uwi, position = "sw")
            nw_lat, nw_lng = uwiToLatLng.convert(nw_uwi, position = "nw")
            ne_lat, ne_lng = uwiToLatLng.convert(ne_uwi, position = "ne")

            kml_polygon += KML_TEMPLATE % (se_lng, se_lat, sw_lng, sw_lat, nw_lng, nw_lat, ne_lng, ne_lat)
            aggregate_latitudes.append( (se_lat + nw_lat) / 2.0)
            aggregate_longitudes.append( (se_lng + nw_lng) / 2.0)

        for quarter_section in quarter_sections:
            if 'NE' in quarter_section: 
                se_uwi = '09' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
                sw_uwi = '10' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
                nw_uwi = '15' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
                ne_uwi = '16' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            elif 'NW' in quarter_section: 
                se_uwi = '11' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
                sw_uwi = '12' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
                nw_uwi = '13' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
                ne_uwi = '14' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            elif 'SE' in quarter_section: 
                se_uwi = '01' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
                sw_uwi = '02' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
                nw_uwi = '07' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
                ne_uwi = '08' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            elif 'SW' in quarter_section: 
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

            kml_polygon += KML_TEMPLATE % (se_lng, se_lat, sw_lng, sw_lat, nw_lng, nw_lat, ne_lng, ne_lat)
            aggregate_latitudes.append( (se_lat + nw_lat) / 2.0)
            aggregate_longitudes.append( (se_lng + nw_lng) / 2.0)

        for half_section in half_sections:
            if 'N' in half_section: 
                se_uwi = '09' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
                sw_uwi = '12' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
                nw_uwi = '13' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
                ne_uwi = '16' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            elif 'E' in half_section: 
                se_uwi = '01' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
                sw_uwi = '02' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
                nw_uwi = '15' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
                ne_uwi = '16' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            elif 'S' in half_section: 
                se_uwi = '01' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
                sw_uwi = '04' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
                nw_uwi = '05' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
                ne_uwi = '08' + '-' + section + '-' + twp + '-' + rng + 'W' + mer
            elif 'W' in half_section: 
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

            kml_polygon += KML_TEMPLATE % (se_lng, se_lat, sw_lng, sw_lat, nw_lng, nw_lat, ne_lng, ne_lat)

            aggregate_latitudes.append( (se_lat + nw_lat) / 2.0)
            aggregate_longitudes.append( (se_lng + nw_lng) / 2.0)

        for lsd_number in lsd_numbers:
            lsd_number = '%02d' % int(lsd_number)
            uwi_lsd = lsd_number + '-' + section + '-' + twp + '-' + rng + 'W' + mer

            se_lat, se_lng = uwiToLatLng.convert(uwi_lsd, position = "se")
            sw_lat, sw_lng = uwiToLatLng.convert(uwi_lsd, position = "sw")
            nw_lat, nw_lng = uwiToLatLng.convert(uwi_lsd, position = "nw")
            ne_lat, ne_lng = uwiToLatLng.convert(uwi_lsd, position = "ne")

            kml_polygon += KML_TEMPLATE % (se_lng, se_lat, sw_lng, sw_lat, nw_lng, nw_lat, ne_lng, ne_lat)
            aggregate_latitudes.append( (se_lat + nw_lat) / 2.0)
            aggregate_longitudes.append( (se_lng + nw_lng) / 2.0)

        try:
            aggregate_latitude = sum(aggregate_latitudes) / len(aggregate_latitudes)
            aggregate_longitude = sum(aggregate_longitudes) / len(aggregate_longitudes)
        except:
            print 'ERROR: unable to find averages of lat / lng from uwi ', uwi
            aggregate_latitude = 0
            aggregate_longitude = 0

        return kml_polygon, aggregate_latitude, aggregate_longitude
