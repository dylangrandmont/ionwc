# Copyright (C) 2016-2018, Dylan Grandmont

from coordinatemapping import uwiToLatLng
from constants import FORMATION_AGE_DICT
from constants import KML_TEMPLATE
from constants import IONWC_HOME
from constants import UNKNOWN
from constants import MONTH_DICT
from constants import BC_POSTING_DATES_TO_SALE_DATE_MAP
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
        Database.__init__(self, csvDatabase, "saleData:contractType:contractNo:hectares:tractNo:uwi:topZone:baseZone:topAge:baseAge:geometry:province\n")

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
        Database.__init__(self, csvDatabase, "saleData:contractType:contractNo:hectares:centerLat:centerLng:province\n")

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
        Database.__init__(self, csvDatabase, "saleData:status:bonus:dollarPerHectare:ClientDescription:contractType:contractNo:hectares:tractNo:uwi:topZone:baseZone:topAge:baseAge:geometry:province\n")

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
        Database.__init__(self, csvDatabase, "saleData:status:bonus:dollarPerHectare:ClientDescription:contractType:contractNo:hectares:centerLat:centerLng:province\n")

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
                                bonus,
                                status,
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

class ABPostingsManager(PostingsManager):
    """ Manage parsing and population of licence database for AB """

    def populate_databases(self):
        self._populate_posting_database()
        self._populate_results_database()

    def _populate_posting_database(self):
        """ Add all postings to the offerings database """
        posting_files  = self._get_postings_files()
        for posting_file in posting_files:
            postings, posting_aggregates = self._postings_from_file(posting_file)

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

    def _postings_from_file(self, file):
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

                    contract_type = row.contract_number
                    hectares = row.hectares
                    tract_number = row.tract_no
                    uwi = row.uwi
                    top_zone = row.top_qualified_zone
                    base_zone = row.base_qualified_zone
                    top_age = row.top_age
                    base_age = row.base_age
                    kml_polygon = row.kml_polygon

                    result = Result(row.sale_date,
                                    bonus,
                                    status,
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


