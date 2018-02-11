#!/usr/bin/python

# Copyright (C) 2016-2018, Dylan Grandmont

# Development testing for making postings database object oriented, to be moved into run.py later

from postings import PostingsDatabase
from postings import PostingsAggregateDatabase
from postings import ResultsDatabase
from postings import ResultsAggregateDatabase
from postings import BCPostingsManager
from postings import ABPostingsManager
from postings import ResultsDatabase

IONWC_HOME = "/home/dylan/Development/ionwc"

postings_database = PostingsDatabase(IONWC_HOME + '/dbs/TestPostingsDataBase.csv')
postings_aggregate_database = PostingsAggregateDatabase(IONWC_HOME + '/dbs/TestPostingsAggregateDataBase.csv')
results_database = ResultsDatabase(IONWC_HOME + '/dbs/TestResultsDataBase.csv')
results_aggregate_database = ResultsAggregateDatabase(IONWC_HOME + '/dbs/TestResultsAggregateDataBase.csv')

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

postings_database.write_to_csv()
postings_aggregate_database.write_to_csv()
results_database.write_to_csv()
results_aggregate_database.write_to_csv()
