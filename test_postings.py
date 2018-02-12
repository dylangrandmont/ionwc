# -*- coding: utf-8 -*-

# Copyright (C) 2016-2018, Dylan Grandmont

import unittest
import postings
import csv
import os

class TestPosting(unittest.TestCase):

    def test_postings_database(self):
        database = postings.PostingsDatabase("temp.csv")
        posting = postings.Posting("2014.01.01",
                                   "lease",
                                   "12345",
                                   "1000.00",
                                   "1",
                                   "100/13-24-037-03W4/00",
                                   "Base Montney",
                                   "Base Leduc",
                                   "252.0",
                                   "323.0",
                                   "KML Polygon Content",
                                   "AB")
        database.add_row(posting)
        database.write_to_csv()
        database.close()

        reader = csv.reader(open("temp.csv"))
        content = list(reader)
        self.assertEquals(content[0][0], "saleDate:contractType:contractNo:hectares:tractNo:uwi:topZone:baseZone:topAge:baseAge:geometry:province")
        self.assertEquals(content[1][0], "2014.01.01:lease:12345:1000.00:1:100/13-24-037-03W4/00:Base Montney:Base Leduc:252.0:323.0:KML Polygon Content:AB")

        os.remove("temp.csv")

    def test_postings_aggregate_database(self):
        database = postings.PostingsAggregateDatabase("temp.csv")
        
        database.close()

        reader = csv.reader(open("temp.csv"))
        content = list(reader)
        self.assertEquals(content[0][0], "saleDate:contractType:contractNo:hectares:centerLat:centerLng:province")

        os.remove("temp.csv")

    def test_posting_results_database(self):
        database = postings.ResultsDatabase("temp.csv")
        database.close()

        reader = csv.reader(open("temp.csv"))
        content = list(reader)
        self.assertEquals(content[0][0], "saleDate:status:bonus:dollarPerHectare:ClientDescription:contractType:contractNo:hectares:tractNo:uwi:topZone:baseZone:topAge:baseAge:geometry:province")

        os.remove("temp.csv")

    def test_posting_resuts_aggregate_database(self):
        database = postings.ResultsAggregateDatabase("temp.csv")
        database.close()

        reader = csv.reader(open("temp.csv"))
        content = list(reader)
        self.assertEquals(content[0][0], "saleDate:status:bonus:dollarPerHectare:ClientDescription:contractType:contractNo:hectares:centerLat:centerLng:province")

        os.remove("temp.csv")

    def test_posting(self):

        posting = postings.Posting("2014.01.01",
                                   "lease",
                                   "12345",
                                   "1000.00",
                                   "1",
                                   "100/13-24-037-03W4/00",
                                   "Base Montney",
                                   "Base Leduc",
                                   "252.0",
                                   "323.0",
                                   "KML Polygon Content",
                                   "AB")

        self.assertEquals(posting.sale_date, "2014.01.01")
        self.assertEquals(posting.contract_type, "lease")
        self.assertEquals(posting.contract_number, "12345")
        self.assertEquals(posting.hectares, "1000.00")
        self.assertEquals(posting.tract_no, "1")
        self.assertEquals(posting.uwi, "100/13-24-037-03W4/00")
        self.assertEquals(posting.top_qualified_zone, "Base Montney")
        self.assertEquals(posting.base_qualified_zone, "Base Leduc")
        self.assertEquals(posting.top_age, "252.0")
        self.assertEquals(posting.base_age, "323.0")
        self.assertEquals(posting.kml_polygon, "KML Polygon Content")

    def test_result(self):
        result = postings.Result("2014.01.01",
                                 "No Bids",
                                 "$1000.00",
                                 "$10.00",
                                 "Some Company",
                                 "Lease",
                                 "Contract 5",
                                 "100.00",
                                 "Tract 1",
                                 "100/13-24-037-03W4/00",
                                 "Base Montney",
                                 "Base Leduc",
                                 "252.0",
                                 "323.0",
                                 "KML Polygon Content",
                                 "AB")

        self.assertEquals(result.sale_date, "2014.01.01")
        self.assertEquals(result.status, "No Bids")
        self.assertEquals(result.bonus, "$1000.00")
        self.assertEquals(result.dollar_per_hect, "$10.00")
        self.assertEquals(result.client_desc, "Some Company")
        self.assertEquals(result.contract_type, "Lease")
        self.assertEquals(result.contract_number, "Contract 5")
        self.assertEquals(result.hectares, "100.00")
        self.assertEquals(result.tract_no, "Tract 1")
        self.assertEquals(result.uwi, "100/13-24-037-03W4/00")
        self.assertEquals(result.top_qualified_zone, "Base Montney")
        self.assertEquals(result.base_qualified_zone, "Base Leduc")
        self.assertEquals(result.top_age, "252.0")
        self.assertEquals(result.base_age, "323.0")
        self.assertEquals(result.kml_polygon, "KML Polygon Content")
        self.assertEquals(result.province, "AB")

    def test_ab_postings_manager(self):

        postings_database = postings.PostingsDatabase('temp_PostingsDataBase.csv')
        postings_aggregate_database = postings.PostingsAggregateDatabase('temp_PostingsAggregateDataBase.csv')
        results_database = postings.ResultsDatabase('temp_PostingsResultsDataBase.csv')
        results_aggregate_database = postings.ResultsAggregateDatabase('temp_PostingsAggregateResultsDataBase.csv')

        ab_postings_manager = postings.ABPostingsManager(postings_database,
                                                         postings_aggregate_database,
                                                         results_database,
                                                         results_aggregate_database)

        os.remove('temp_PostingsDataBase.csv')
        os.remove('temp_PostingsAggregateDataBase.csv')
        os.remove('temp_PostingsResultsDataBase.csv')
        os.remove('temp_PostingsAggregateResultsDataBase.csv')


if __name__ == '__main__':
    result = unittest.main()
