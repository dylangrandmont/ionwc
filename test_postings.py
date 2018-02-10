# -*- coding: utf-8 -*-

# Copyright (C) 2016-2018, Dylan Grandmont

import unittest
import postings
import csv
import os

class TestPosting(unittest.TestCase):

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
			                       "KML Polygon Content")

		self.assertEquals(posting.sale_date, "2014.01.01")
		self.assertEquals(posting.contract_type, "lease")
		self.assertEquals(posting.contract_no, "12345")
		self.assertEquals(posting.hectares, "1000.00")
		self.assertEquals(posting.tract_no, "1")
		self.assertEquals(posting.uwi, "100/13-24-037-03W4/00")
		self.assertEquals(posting.top_qualified_zone, "Base Montney")
		self.assertEquals(posting.base_qualified_zone, "Base Leduc")
		self.assertEquals(posting.top_age, "252.0")
		self.assertEquals(posting.base_age, "323.0")
		self.assertEquals(posting.kml_polygon, "KML Polygon Content")

	def test_bc_posting(self):

		posting = postings.BCPosting("2014.01.01",
			                         "lease",
			                         "12345",
			                         "1000.00",
			                         "1",
			                         "100/13-24-037-03W4/00",
			                         "Base Montney",
			                         "Base Leduc",
			                         "252.0",
			                         "323.0",
			                         "KML Polygon Content")

		self.assertEquals(posting.province, "BC")

	def test_ab_posting(self):

		posting = postings.ABPosting("2014.01.01",
			                         "lease",
			                         "12345",
			                         "1000.00",
			                         "1",
			                         "100/13-24-037-03W4/00",
			                         "Base Montney",
			                         "Base Leduc",
			                         "252.0",
			                         "323.0",
			                         "KML Polygon Content")

		self.assertEquals(posting.province, "AB")

	def test_sk_posting(self):

		posting = postings.SKPosting("2014.01.01",
			                         "lease",
			                         "12345",
			                         "1000.00",
			                         "1",
			                         "100/13-24-037-03W4/00",
			                         "Base Montney",
			                         "Base Leduc",
			                         "252.0",
			                         "323.0",
			                         "KML Polygon Content")

		self.assertEquals(posting.province, "SK")

	def test_mb_posting(self):

		posting = postings.MBPosting("2014.01.01",
			                         "lease",
			                         "12345",
			                         "1000.00",
			                         "1",
			                         "100/13-24-037-03W4/00",
			                         "Base Montney",
			                         "Base Leduc",
			                         "252.0",
			                         "323.0",
			                         "KML Polygon Content")

		self.assertEquals(posting.province, "MB")

	def test_postings_database(self):
		database = postings.PostingsDatabase("temp.csv")
		posting = postings.ABPosting("2014.01.01",
			                       "lease",
			                       "12345",
			                       "1000.00",
			                       "1",
			                       "100/13-24-037-03W4/00",
			                       "Base Montney",
			                       "Base Leduc",
			                       "252.0",
			                       "323.0",
			                       "KML Polygon Content")
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
		self.assertEquals(content[0][0] , "saleDate:contractType:contractNo:hectares:centerLat:centerLng:province")

		os.remove("temp.csv")

	def test_posting_results_database(self):
		database = postings.PostingResultsDatabase("temp.csv")
		database.close()

		reader = csv.reader(open("temp.csv"))
		content = list(reader)
		self.assertEquals(content[0][0] , "saleDate:status:bonus:dollarPerHectare:ClientDescription:contractType:contractNo:hectares:tractNo:uwi:topZone:baseZone:topAge:baseAge:geometry:province")

		os.remove("temp.csv")

if __name__ == '__main__':
	result = unittest.main()