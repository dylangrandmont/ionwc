#!/usr/bin/python

# Copyright (C) 2016-2018, Dylan Grandmont

import os
import datastream
import licencescreatedatabases
import unittest
import test_licences
import test_postings
import test_constants
import test_utilities
import sys
from licences import ABLicenceManager
from licences import BCLicenceManager
from licences import SKLicenceManager
from licences import MBLicenceManager
from licences import LicenceDatabase
from postings import PostingsDatabase
from postings import PostingsAggregateDatabase
from postings import ResultsDatabase
from postings import ResultsAggregateDatabase
from postings import BCPostingsManager
from postings import ABPostingsManager
from postings import SKPostingsManager
from postings import MBPostingsManager
from postings import ResultsDatabase

os.system('export IONWC_HOME=/home/dylan/Development/ionwc')

from constants import IONWC_HOME

# Update raw data collection
datastream.run_all()

# Execute Unit Test Coverage
def run_unit_tests_module(module):
	suite = unittest.TestLoader().loadTestsFromTestCase(module)
	result = unittest.TextTestRunner(verbosity=2).run(suite)
	if len(result.errors) > 0:
		sys.exit()

run_unit_tests_module(test_licences.TestABLicence)
run_unit_tests_module(test_postings.TestPosting)
run_unit_tests_module(test_constants.TestConstants)
run_unit_tests_module(test_utilities.TestUtilities)


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

postings_database = PostingsDatabase(IONWC_HOME + '/dbs/PostingsDataBase.csv')
postings_aggregate_database = PostingsAggregateDatabase(IONWC_HOME + '/dbs/PostingsAggregateDataBase.csv')
results_database = ResultsDatabase(IONWC_HOME + '/dbs/PostingsResultsDataBase.csv')
results_aggregate_database = ResultsAggregateDatabase(IONWC_HOME + '/dbs/PostingsAggregateResultsDataBase.csv')

bc_postings_manager = BCPostingsManager(postings_database,
                                        postings_aggregate_database,
                                        results_database,
                                        results_aggregate_database)
bc_postings_manager.populate_databases()

ab_postings_manager = ABPostingsManager(postings_database,
                                        postings_aggregate_database,
                                        results_database,
                                        results_aggregate_database)
ab_postings_manager.populate_databases()

sk_postings_manager = SKPostingsManager(postings_database,
                                        postings_aggregate_database,
                                        results_database,
                                        results_aggregate_database)
sk_postings_manager.populate_databases()

mb_postings_manager = MBPostingsManager(postings_database,
                                        postings_aggregate_database,
                                        results_database,
                                        results_aggregate_database)
mb_postings_manager.populate_databases()

postings_database.write_to_csv()
postings_aggregate_database.write_to_csv()
results_database.write_to_csv()
results_aggregate_database.write_to_csv()


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
