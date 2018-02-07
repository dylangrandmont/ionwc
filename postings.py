# Copyright (C) 2016-2018, Dylan Grandmont

from coordinatemapping import uwiToLatLng
from constants import FORMATION_AGE_DICT, KML_TEMPLATE, IONWC_HOME, UNKNOWN
from utilities import writePostingOfferingDataBaseFile, writePostingOfferingAggregateDataBaseFile, writePostingResultDataBaseFile
import xml.etree.ElementTree as ET

class Database:
    def __init__(self, csvDatabase, header):
        self.csvDatabase = open(csvDatabase, "w")
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
            writePostingOfferingDataBaseFile(self.csvDatabase, row.sale_date, row.contract_type, row.contract_no,
                                             row.hectares, row.tract_no, row.uwi, row.top_qualified_zone,
                                             row.base_qualified_zone, row.top_age, row.base_age, row.kml_polygon,
                                             row.province)

class PostingsAggregateDatabase(Database):
    def __init__(self, csvDatabase):
        Database.__init__(self, csvDatabase, "saleDate:contractType:contractNo:hectares:centerLat:centerLng:province\n")

    def write_to_csv(self):
        for row in self.rows:
        	writePostingOfferingAggregateDataBaseFile(self.csvDatabase,
        		                                      row.sale_date,
        		                                      row.contract_type,
        		                                      row.contract_no,
        		                                      row.hectares,
        		                                      row.aggregate_latitude,
        		                                      row.aggregate_longitude,
        		                                      row.province)

class PostingResultsDatabase(Database):
    def __init__(self, csvDatabase):
        Database.__init__(self, csvDatabase, "saleDate:status:bonus:dollarPerHectare:ClientDescription:contractType:contractNo:hectares:tractNo:uwi:topZone:baseZone:topAge:baseAge:geometry:province\n")

    def write_to_csv(self):
        for row in self.rows:
        	writePostingResultDataBaseFile(self.csvDatabase, row.sale_date, row.status, row.bonus,
        		                           row.dollar_per_hect, row.client_desc, row.contract_type,
        		                           row.contract_number, row.hectares, row.tract_no, row.uwi,
        		                           row.top_qualified_zone, row.base_qualified_zone, row.top_age, 
                                           row.base_age, row.kml_polygon, row.province)


class Posting:
    province = UNKNOWN

    def __init__(self, sale_date, contract_type, contract_no, hectares, tract_no, uwi, top_qualified_zone,
                 base_qualified_zone, top_age, base_age, kml_polygon):

        self.sale_date = sale_date
        self.contract_type = contract_type
        self.contract_no = contract_no
        self.hectares = hectares
        self.tract_no = tract_no
        self.uwi = uwi
        self.top_qualified_zone = top_qualified_zone
        self.base_qualified_zone = base_qualified_zone
        self.top_age = top_age
        self.base_age = base_age
        self.kml_polygon = kml_polygon

class PostingAggregate:
    province = UNKNOWN

    def __init__(self, sale_date, contract_type, contract_no, hectares, aggregate_latitude, aggregate_longitude):

        self.sale_date = sale_date
        self.contract_type = contract_type
        self.contract_no = contract_no
        self.hectares = hectares
        self.aggregate_latitude = aggregate_latitude
        self.aggregate_longitude = aggregate_longitude

class PostingResult:
    def __init__(self, sale_date, status, bonus, dollar_per_hect, client_desc, contract_type, contract_no, hectares, tract_no, uwi, top_qualified_zone,
                 base_qualified_zone, top_age, base_age, kml_polygon):

        self.sale_date = sale_date
        self.status = status
        self.bonus = bonus
        self.dollar_per_hect = dollar_per_hect
        self.client_desc = client_desc
        self.contract_type = contract_type
        self.contract_no = contract_no
        self.hectares = hectares
        self.tract_no = tract_no
        self.uwi = uwi
        self.top_qualified_zone = top_qualified_zone
        self.base_qualified_zone = base_qualified_zone
        self.top_age = top_age
        self.base_age = base_age
        self.kml_polygon = kml_polygon


class BCPosting(Posting):
    province = 'BC'

class BCPostingResult(PostingResult):
    province = 'BC'

class ABPosting(Posting):
    province = 'AB'

class ABPostingAggregate(PostingAggregate):
	province = 'AB'

class ABPostingResult(PostingResult):
    province = 'AB'

class SKPosting(Posting):
    province = 'SK'

class MBPosting(Posting):
    province = 'MB'

class SKPostingResult(PostingResult):
    province = 'SK'

class MBPostingResult(PostingResult):
    province = 'MB'



class PostingsManager:
    def __init__(self, posting_database, posting_aggregates_database, results_database):
        self.posting_database = posting_database
        self.posting_aggregates_database = posting_aggregates_database
        self.results_database = results_database



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
        """ Add all postings to the offerings database """
        results_files  = self._get_results_files()
        for results_file in results_files:
            results = self._postings_from_file(results_file)
            for result in results:
                self.results_database.add_row(result)

    def _get_postings_files(self):
        """ Retreive all the AB posting files """
        return glob.glob(IONWC_HOME + '/data/postings/ab/*PON.xml')

    def _get_results_files(self):
        """ Retreive all the AB results files """
        return glob.glob(IONWC_HOME + '/data/postings/ab/*PSR.xml')    	

    def _postings_from_file(self, file):
        """ From each AB postings file, find all patterns for posting contracts """
        tree = ET.parse(AER_POSTING_FILE)
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
                contract_no = contract.find(".//" + namespace + "ContractNo").text
                hectares = contract.find(".//" + namespace + "Hectares").text
                tracts = contract.findall(".//" + namespace + "Tract")

                aggregateLatitudes = []
                aggregateLongitudes = []

                for tract in tracts:
                    tract_no = tract.find(".//" + namespace + "TractNo").text
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

                        kml_polygon, centerLatitude, centerLongitude = self._postingUWIToKmlPolygon(uwi, lsd, sec, twp, rng, mer)
                        aggregateLatitudes.append(centerLatitude)
                        aggregateLongitudes.append(centerLongitude)

                        try:
                            top_age = FORMATION_AGE_DICT[topZone.lower().replace(' fm', '').replace(' sd', '').replace(' grp', '').replace(' mbr', '').replace(' ss', '').replace('zone', '').strip()]
                            base_age = FORMATION_AGE_DICT[baseZone.lower().replace(' fm', '').replace(' sd', '').replace(' grp', '').replace(' mbr', '').replace(' ss', '').replace('zone', '').strip()]
                        except:
                            raise Exception('No entry found in FORMATION_AGE_DICT for ', topZone, baseZone)

                        posting = ABPosting(sale_date, contract_type, contract_no, hectares, tract_no, uwi, topQualifier + ' ' + topZone, baseQualifier + ' ' + baseZone, top_age, base_age, kml_polygon)
                        postings.append(posting)

                aggregateLatitude = sum(aggregateLatitudes) / len(aggregateLatitudes)
                aggregateLongitude = sum(aggregateLongitudes) / len(aggregateLongitudes)
                postingAggregate = ABPostingAggregate(sale_date, contract_type, contract_no, hectares, str(aggregateLatitude), str(aggregateLongitude))
                postingAggregates.append(postingAggregate)

        return postings, postingAggregates


    def _postingUWIToKmlPolygon(uwi, lsd, sec, twp, rng, mer):
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


