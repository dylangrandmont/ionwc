# Copyright (C) 2016-2018, Dylan Grandmont

import unittest
import utilities

class TestUtilities(unittest.TestCase):

    def _equal_within_tolerance(self, expected, actual, tolerance = 0.000001):
        if (abs(float(expected) - float(actual)) < tolerance):
            self.assertTrue(True)
        else:
            self.assertTrue(False, 'Expected ' + str(expected) + ' but found ' + str(actual))

    def test_substance_code_matches_substance(self):
        self.assertEqual('0', utilities.get_substance_code('oil'))
       	self.assertEqual('1', utilities.get_substance_code('gas'))
       	self.assertEqual('1', utilities.get_substance_code('methane'))
       	self.assertEqual('2', utilities.get_substance_code('bitumen'))
       	self.assertEqual('3', utilities.get_substance_code('water'))
       	self.assertEqual('4', utilities.get_substance_code('other'))
       	self.assertEqual('4', utilities.get_substance_code('unknown'))
       	self.assertEqual('4', utilities.get_substance_code(''))

    def test_conform_substance(self):
    	self.assertEqual('Unknown', utilities.conform_substance('0'))
    	self.assertEqual('Gas', utilities.conform_substance('gas well'))
    	self.assertEqual('Crude Oil', utilities.conform_substance('oil well'))

    def test_reformat_dollars(self):
    	self.assertEqual('$100.00', utilities.reformat_dollars('100'))
    	self.assertEqual('$100.00', utilities.reformat_dollars('$100.00'))
    	self.assertEqual('$100.00', utilities.reformat_dollars('100.00'))
    	self.assertEqual('$100.00', utilities.reformat_dollars('100.0'))
    	self.assertEqual('', utilities.reformat_dollars(''))
    	self.assertEqual('invalidformat', utilities.reformat_dollars('invalidformat'))

    def test_km_per_degree_lat_lng(self):
    	self._equal_within_tolerance(110.90803658265078, utilities.km_per_degree_lat_lng(50.0)[0])
    	self._equal_within_tolerance(71.695753616, utilities.km_per_degree_lat_lng(50.0)[1])

    	self._equal_within_tolerance(110.982650694, utilities.km_per_degree_lat_lng(55.0)[0])
    	self._equal_within_tolerance(63.9941292977, utilities.km_per_degree_lat_lng(55.0)[1])

    	self._equal_within_tolerance(111.057166525, utilities.km_per_degree_lat_lng(60.0)[0])
    	self._equal_within_tolerance(55.8000015724, utilities.km_per_degree_lat_lng(60.0)[1])

    	self._equal_within_tolerance(111.128086507, utilities.km_per_degree_lat_lng(65.0)[0])
    	self._equal_within_tolerance(47.1755310596, utilities.km_per_degree_lat_lng(65.0)[1])

if __name__ == '__main__':
    result = unittest.main()
