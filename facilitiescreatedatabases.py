##################################################################
# Copyright (C) 2016-2017 Eye on Western Canada
#
# Create Database (csv) of Land Postings and Sale Results
#
##################################################################

from facilities import addBCFacilitiesToDataBase
import os

def run():
	IONWC_HOME = os.environ["IONWC_HOME"]

	DATA_BASE_FILE_NAME = IONWC_HOME + "/dbs/FacilitiesDataBase.csv"

	dataBaseFile = open(DATA_BASE_FILE_NAME, "w")
	dataBaseFile.write('saleDate:contractType:contractNo:hectares:tractNo:uwi:topZone:baseZone:topAge:baseAge:geometry:province\n')

	addBCFacilitiesToDataBase(dataBaseFile)
	#addABOfferingsToDataBase(dataBaseFile)
	#addSKOfferingsToDataBase(dataBaseFile)

	dataBaseFile.close()
