# Copyright (C) 2018, Dylan Grandmont

from constants import FORMATION_AGE_DICT, BC_POSTING_DATES_TO_SALE_DATE_MAP
import unittest

class TestConstants(unittest.TestCase):
	def test_central_plains_formations_are_in_order(self):
		self.assertTrue(
			FORMATION_AGE_DICT['surface'] <
			FORMATION_AGE_DICT['paskapoo'] <
			FORMATION_AGE_DICT['edmonton'] <
			#FORMATION_AGE_DICT['belly river'] <
		    FORMATION_AGE_DICT['upper colorado shale'] <
		    FORMATION_AGE_DICT['bluesky'] <
		    FORMATION_AGE_DICT['halfway'] <
		    FORMATION_AGE_DICT['montney'] <
		    FORMATION_AGE_DICT['banff'] <
		    FORMATION_AGE_DICT['wabamun'] <
		    FORMATION_AGE_DICT['leduc'] <
		    FORMATION_AGE_DICT['basement']
		)

	def test_bc_postings_date_order(self):
		previousDate = '2016.01.01'
		nextDate = '2016.01.01'

		for year in ['2016', '2017', '2018']:
			for month in ['01', '02', '03','04', '05', '06', '07', '08', '09', '10', '11', '12']:
				nextDate = BC_POSTING_DATES_TO_SALE_DATE_MAP[year + '.' + month]
				self.assertTrue(nextDate > previousDate, 'Expected ' + nextDate + ' to come after ' + previousDate)
				previousDate = nextDate

if __name__ == '__main__':
	unittest.main()