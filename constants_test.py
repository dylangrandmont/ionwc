from constants import FORMATION_AGE_DICT
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

if __name__ == '__main__':
	unittest.main()