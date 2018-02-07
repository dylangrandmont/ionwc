# Copyright (C) 2016-2017, Eye on Western Canada
#
# Script to update databases and push changes to a google FusionTable

import os
import datastream
import licencescreatedatabases
import postingscreatedatabase
import unittest
import licence_test
import constants_test
import sys
from licences import ABLicenceManager, BCLicenceManager, SKLicenceManager, MBLicenceManager, LicenceDatabase

os.system('export IONWC_HOME=/home/dylan/Development/ionwc')

from constants import IONWC_HOME

# Update raw data collection
datastream.run_all()

def run_licence_unit_tests():
	suite = unittest.TestLoader().loadTestsFromTestCase(licence_test.TestABLicence)
	result = unittest.TextTestRunner(verbosity=2).run(suite)
	if len(result.errors) > 0:
		sys.exit()

def run_constants_unit_tests():
	suite = unittest.TestLoader().loadTestsFromTestCase(constants_test.TestConstants)
	result = unittest.TextTestRunner(verbosity=2).run(suite)
	if len(result.errors) > 0:
		sys.exit()

def run_unit_tests():
	run_licence_unit_tests()
	run_constants_unit_tests()


run_unit_tests();

licenceDatabaseName = IONWC_HOME + '/dbs/licenceDBAll.csv'
licenceDatabase = LicenceDatabase(licenceDatabaseName)

abLicenceManager = ABLicenceManager(licenceDatabase)
abLicenceManager.populate_database()

bcLicenceManager = BCLicenceManager(licenceDatabase)
bcLicenceManager.populate_database()

skLicenceManager = SKLicenceManager(licenceDatabase)
skLicenceManager.populate_database()

mbLicenceManager = MBLicenceManager(licenceDatabase)
mbLicenceManager.populate_database()

licenceDatabase.write_to_csv()

licencescreatedatabases.run()
postingscreatedatabase.run()

#postingsDatabaseName = IONWC_HOME + '/dbs/PostingsDataBase.csv'
#postingsDatabase = PostingsDatabase()
#abPostingsManager = ABPostingsManager(postingsDatabase)
#postingsDatabase.write_to_csv()


# Generate Differences between new and submitted databases
os.system('sort $IONWC_HOME/dbs/licenceDBAll.csv $IONWC_HOME/dbs/submitted_licenceDBAll.csv | uniq -u > $IONWC_HOME/dbs/diff_licenceDBAll.csv')
os.system('less $IONWC_HOME/dbs/diff_licenceDBAll.csv')
os.system('sort $IONWC_HOME/dbs/AUGlicdb.csv $IONWC_HOME/dbs/submitted_AUGlicdb.csv | uniq -u > $IONWC_HOME/dbs/AUGlicdb_diff.csv')
os.system('less $IONWC_HOME/dbs/AUGlicdb_diff.csv')
os.system('sort $IONWC_HOME/dbs/PostingsDataBase.csv $IONWC_HOME/dbs/submitted_PostingsDataBase.csv | uniq -u > $IONWC_HOME/dbs/diff_PostingsDataBase.csv')
os.system('less $IONWC_HOME/dbs/diff_PostingsDataBase.csv')
os.system('sort $IONWC_HOME/dbs/PostingsResultsDataBase.csv $IONWC_HOME/dbs/submitted_PostingsResultsDataBase.csv | uniq -u > $IONWC_HOME/dbs/diff_PostingsResultsDataBase.csv')
os.system('less $IONWC_HOME/dbs/diff_PostingsResultsDataBase.csv')
os.system('sort $IONWC_HOME/dbs/PostingsAggregateDataBase.csv $IONWC_HOME/dbs/submitted_PostingsAggregateDataBase.csv | uniq -u > $IONWC_HOME/dbs/diff_PostingsAggregateDataBase.csv')
os.system('less $IONWC_HOME/dbs/diff_PostingsAggregateDataBase.csv')
os.system('sort $IONWC_HOME/dbs/PostingsAggregateResultsDataBase.csv $IONWC_HOME/dbs/submitted_PostingsAggregateResultsDataBase.csv | uniq -u > $IONWC_HOME/dbs/diff_PostingsAggregateResultsDataBase.csv')
os.system('less $IONWC_HOME/dbs/diff_PostingsAggregateResultsDataBase.csv')

os.system('python $IONWC_HOME/scripts/uploadfusiontablediffs.py')

# Update the submitted copies
os.system('cp $IONWC_HOME/dbs/licenceDBAll.csv  $IONWC_HOME/dbs/submitted_licenceDBAll.csv')
os.system('cp $IONWC_HOME/dbs/AUGlicdb.csv  $IONWC_HOME/dbs/submitted_AUGlicdb.csv')
os.system('cp $IONWC_HOME/dbs/PostingsDataBase.csv  $IONWC_HOME/dbs/submitted_PostingsDataBase.csv')
os.system('cp $IONWC_HOME/dbs/PostingsResultsDataBase.csv  $IONWC_HOME/dbs/submitted_PostingsResultsDataBase.csv')
os.system('cp $IONWC_HOME/dbs/PostingsAggregateDataBase.csv  $IONWC_HOME/dbs/submitted_PostingsAggregateDataBase.csv')
os.system('cp $IONWC_HOME/dbs/PostingsAggregateResultsDataBase.csv  $IONWC_HOME/dbs/submitted_PostingsAggregateResultsDataBase.csv')
