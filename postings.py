# Copyright (C) 2016-2018, Dylan Grandmont

from coordinatemapping import uwiToLatLng
from constants import FORMATION_AGE_DICT
from constants import KML_TEMPLATE
from constants import IONWC_HOME
from constants import UNKNOWN
from utilities import writePostingOfferingDataBaseFile
from utilities import writePostingOfferingAggregateDataBaseFile
from utilities import writePostingResultDataBaseFile
from utilities import writePostingResultAggregateDataBaseFile
import xml.etree.ElementTree as ET
import glob
import locale

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

                        posting = Posting(sale_date, contract_type, contract_number, hectares, tract_no, uwi, topQualifier + ' ' + topZone, baseQualifier + ' ' + baseZone, top_age, base_age, kml_polygon, 'AB')
                        postings.append(posting)

                aggregateLatitude = sum(aggregateLatitudes) / len(aggregateLatitudes)
                aggregateLongitude = sum(aggregateLongitudes) / len(aggregateLongitudes)
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
            parcelNumber = parcel.find(".//" + namespace + "ParcelNumber").text
            contractFlag = parcel.find(".//" + namespace + "ContractFlag").text
            contract_number = contractFlag + parcelNumber

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


    def _postingUWIToKmlPolygon(self, uwi, lsd, sec, twp, rng, mer):
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


