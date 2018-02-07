# Copyright (C) 2016-2018, Dylan Grandmont

from postingsab import addABOfferingsToDataBase, addABResultsToDataBase
from postingsbc import addBCOfferingsToDataBase, addBCResultsToDataBase
from postingssk import addSKOfferingsToDataBase, addSKResultsToDataBase
from postingsmb import addMBOfferingsToDataBase, addMBResultsToDataBase
import os


def run():
	IONWC_HOME = os.environ["IONWC_HOME"]

	PON_DATA_BASE_FILE_NAME = IONWC_HOME + "/dbs/PostingsDataBase.csv"
	PON_AGGREGATE_FILE_NAME = IONWC_HOME + "/dbs/PostingsAggregateDataBase.csv"
	PSR_DATA_BASE_FILE_NAME = IONWC_HOME + "/dbs/PostingsResultsDataBase.csv"
	PSR_AGGREGATE_FILE_NAME = IONWC_HOME + "/dbs/PostingsAggregateResultsDataBase.csv"

	ponDataBaseFile = open(PON_DATA_BASE_FILE_NAME, "w")
	ponDataBaseFile.write('saleDate:contractType:contractNo:hectares:tractNo:uwi:topZone:baseZone:topAge:baseAge:geometry:province\n')

	ponAggregateDataBaseFile = open(PON_AGGREGATE_FILE_NAME, "w")
	#ponAggregateDataBaseFile.write('saleDate:contractType:contractNo:hectares:province\n')
	ponAggregateDataBaseFile.write('saleDate:contractType:contractNo:hectares:centerLat:centerLng:province\n')

	psrDataBaseFile = open(PSR_DATA_BASE_FILE_NAME, "w")
	psrDataBaseFile.write('saleDate:status:bonus:dollarPerHectare:ClientDescription:contractType:contractNo:hectares:tractNo:uwi:topZone:baseZone:topAge:baseAge:geometry:province\n')

	psrAggregateDataBaseFile = open(PSR_AGGREGATE_FILE_NAME, "w")
	psrAggregateDataBaseFile.write('saleDate:status:bonus:dollarPerHectare:ClientDescription:contractType:contractNo:hectares:centerLat:centerLng:province\n')

	addBCOfferingsToDataBase(ponDataBaseFile, ponAggregateDataBaseFile)
	addABOfferingsToDataBase(ponDataBaseFile, ponAggregateDataBaseFile)
	addSKOfferingsToDataBase(ponDataBaseFile, ponAggregateDataBaseFile)
	addMBOfferingsToDataBase(ponDataBaseFile, ponAggregateDataBaseFile)

	ponDataBaseFile.close()
	ponAggregateDataBaseFile.close()
	ponDataBaseFile = open(PON_DATA_BASE_FILE_NAME, "r")
	ponAggregateDataBaseFile = open(PON_AGGREGATE_FILE_NAME, "r")

	addBCResultsToDataBase(psrDataBaseFile, psrAggregateDataBaseFile, PON_DATA_BASE_FILE_NAME, PON_AGGREGATE_FILE_NAME)
	addABResultsToDataBase(psrDataBaseFile, psrAggregateDataBaseFile, PON_DATA_BASE_FILE_NAME, PON_AGGREGATE_FILE_NAME)
	addSKResultsToDataBase(psrDataBaseFile, psrAggregateDataBaseFile, PON_DATA_BASE_FILE_NAME, PON_AGGREGATE_FILE_NAME)
	addMBResultsToDataBase(psrDataBaseFile, psrAggregateDataBaseFile, PON_DATA_BASE_FILE_NAME, PON_AGGREGATE_FILE_NAME)
