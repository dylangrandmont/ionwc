# -*- coding: utf-8 -*-

import unittest
import licences

class TestABLicence(unittest.TestCase):
	def _assertEqualsLatLng(self, actual, expected):
		self.assertTrue(abs(actual - expected) < 0.000001)

	def testABLicence(self):
		testEntry = """    SURGE ENERGY HZ PROVOST 13-24-37-3   0482527   ALBERTA CROWN        742.8M        \r\n                  
    		 100/13-24-037-03W4/00  N   64.9M  E   85.0M    WAINWRIGHT           2280.0M  \r\n
    		 DEV (NC)                             PROVOST                        SPARKY MBR              \r\n  
    		 HORIZONTAL                           NEW       PRODUCTION           CRUDE OIL                       \r\n
    		 SURGE ENERGY INC.                                                   04-24-037-03W4   """

		srcFile = 'WELLS0123.TXT'
		srcPath = 'some/arbitrary/path/to/file/2017/'

		abLicence = licences.ABLicence(testEntry, srcFile, srcPath)

		self.assertEquals(abLicence.licencee, 'SURGE ENERGY INC.')
		self.assertEquals(abLicence.wellname, 'SURGE ENERGY HZ PROVOST 13-24-37-3')
		self.assertEquals(abLicence.licnum, '0482527')
		self.assertEquals(abLicence.uwi, '100/13-24-037-03W4/00')
		self.assertEquals(abLicence.year, '2017')
		self.assertEquals(abLicence.month, '01')
		self.assertEquals(abLicence.day, '23')
		self.assertEquals(abLicence.field, 'PROVOST')
		self.assertEquals(abLicence.zone, 'SPARKY MBR')
		self.assertEquals(abLicence.direct, 'HORIZONTAL')
		self.assertEquals(abLicence.sub, 'Crude Oil')
		self.assertEquals(abLicence.subcode, '0')
		self._assertEqualsLatLng(abLicence.lat, 52.18902350929477)
		self._assertEqualsLatLng(abLicence.lng, -110.30956809807209)
		self.assertEquals(abLicence.province, 'AB')

	def testBCLicenceMissingZoneLatLng(self):
		testRow = ["00639","Whitecap Resources Inc.","22-JUL-1960","Development",
		"WHITECAP ET AL  BOUNDARY  06-24-085-14","Crown","-",
		"North 607.2m East 609.7m from SW corner of LSD 04 SECT 24","56 22 57.47","120 04 25.09","-","748.2","-","-",
		"100062408514W600"]

		bcLicence = licences.BCLicence(testRow)

		self.assertEquals(bcLicence.licencee, 'Whitecap Resources Inc.')
		self.assertEquals(bcLicence.wellname, 'WHITECAP ET AL  BOUNDARY  06-24-085-14')
		self.assertEquals(bcLicence.licnum, '00639')
		self.assertEquals(bcLicence.uwi, '100062408514W600')
		self.assertEquals(bcLicence.year, '1960')
		self.assertEquals(bcLicence.month, '07')
		self.assertEquals(bcLicence.day, '22')
		self.assertEquals(bcLicence.field, 'Boundary Lake')
		self.assertEquals(bcLicence.zone, '-')
		self.assertEquals(bcLicence.direct, 'Unknown')
		self.assertEquals(bcLicence.sub, '-')
		self.assertEquals(bcLicence.subcode, '4')
		self.assertEquals(bcLicence.lat, 56.38263055555556)
		self.assertEquals(bcLicence.lng, -120.07363611111111)
		self.assertEquals(bcLicence.province, 'BC')

	def testBCLicenceHasZoneLatLng(self):

		testRow = ["32842","Kelt Exploration (LNG) Ltd.","20-JAN-2017","Development",
		"KELT LNG  HZ OAK  14-11-086-18","Private","Gas",
		"North -70m East 550.1m from NW corner of LSD 14 SECT 11","56 26 57.47","120 43 58.77","06-02-086-18","661.5",
		"4,000","MONTNEY","100060208618W600"]

		bcLicence = licences.BCLicence(testRow)

		self.assertEquals(bcLicence.licencee, 'Kelt Exploration (LNG) Ltd.')
		self.assertEquals(bcLicence.wellname, 'KELT LNG  HZ OAK  14-11-086-18')
		self.assertEquals(bcLicence.licnum, '32842')
		self.assertEquals(bcLicence.uwi, '100060208618W600')
		self.assertEquals(bcLicence.year, '2017')
		self.assertEquals(bcLicence.month, '01')
		self.assertEquals(bcLicence.day, '20')
		self.assertEquals(bcLicence.field, 'Oak')
		self.assertEquals(bcLicence.zone, 'MONTNEY')
		self.assertEquals(bcLicence.direct, 'Unknown')
		self.assertEquals(bcLicence.sub, 'Gas')
		self.assertEquals(bcLicence.subcode, '1')
		self.assertEquals(bcLicence.lat, 56.44929722222222)
		self.assertEquals(bcLicence.lng, -120.73299166666666)
		self.assertEquals(bcLicence.province, 'BC')

	def testSKLicenceAfterNov2015(self):
		test_well_bore_entry = ["New","Issued","2017-04-18","2017-04-18","","72457","12746","WHITECAP RESOURCES INC.",
			"Suite 3800 East Tower 525 - 8th Avenue SW CALGARY Alberta T2P 1G1 ","Horizontal","HORIZONTAL","N",
			"Kindersley","2","200.8","S","633.0","W","15-18-033-23W3","15","18","N","033","N","23","N","3","700",
			"Dev Well","01","SK0130317","Kindersley","290","Wellbore","SK WI 102101903323W300","SK0130317B001","706",
			"","","","","505.0","S","803.0","W","10-19-033-23W3","10","19","N","033","N","23","N","3","VIKING FORMATION",
			"4500","1950.00"]

		test_completion_entry = ["New","Issued","2017-04-18","2017-04-18","","72457","12746",
			"WHITECAP RESOURCES INC.","Suite 3800 East Tower 525 - 8th Avenue SW CALGARY Alberta T2P 1G1 ",
			"Horizontal","HORIZONTAL","N","Kindersley","2","200.8","S","633.0","W","15-18-033-23W3","15","18","N",
			"033","N","23","N","3","700","Dev Well","01","SK0130317","Kindersley","290","Completion",
			"SK WI 102101903323W300","SK0130317V000","700","Oil Well","10","KERROBERT VIKING","227342","","","","",
			"","","","","","","","","","","",""]

		testFile = "FL170503.csv"

		skLicence = licences.NewSKLicence(test_well_bore_entry, test_completion_entry, testFile)

		self.assertEquals(skLicence.licencee, 'WHITECAP RESOURCES INC.')
		self.assertEquals(skLicence.wellname, '')
		self.assertEquals(skLicence.licnum, '72457')
		self.assertEquals(skLicence.uwi, 'SK WI 102101903323W300')
		self.assertEquals(skLicence.year, '2017')
		self.assertEquals(skLicence.month, '05')
		self.assertEquals(skLicence.day, '03')
		self.assertEquals(skLicence.field, 'KERROBERT VIKING')
		self.assertEquals(skLicence.zone, 'VIKING FORMATION')
		self.assertEquals(skLicence.direct, 'HORIZONTAL')
		self.assertEquals(skLicence.sub, 'Crude Oil')
		self.assertEquals(skLicence.subcode, '0')
		self.assertEquals(skLicence.lat, 51.834237765811686)
		self.assertEquals(skLicence.lng, -109.25840923847824)
		self.assertEquals(skLicence.province, 'SK')		

	def testSKLicenceBeforeNov2015(self):
		test_entry = ["20061127","NEW LICENSE         ","11","08","22","48","26","3"," "," "," "," "," ","06K336",
		" ","20061127","  ","  ","  ","  ","  "," "," "," "," "," ","  "," ","        "," ",
		"CNRL LASHBURN WEST DD 4A8-22-4A8-22-48-26         ","  ","  ","  ","  ","  "," "," "," "," "," "," ",
		"0600.4"," ","N"," ","0070.0"," ","W"," ","22"," ","48"," ","26"," ","3"," ","0612.4","  ","  ","  ","  ","  ",
		" "," "," "," "," ","  "," ","  ","  ","  ","  ","  "," "," "," "," "," ","  "," "," ","235019",
		"CUMMINGS                      "," ","0611.4"," ","234119","LLOYDMINSTER                  "," ","0527.2",
		"      ","                              ","      ","                              "," ","04",
		"NEW POOL WILDCAT         "," ","OIL WELL                             "," ","30 DAYS   "," ",
		"                              "," "," PN39603"," ","100.00000"," ","000.00000"," ","000.00000"," ","1",
		"LLOYDMINSTER ","                                        "," ","472"," ","50449",
		"CANADIAN NATURAL RESOURCES LIMITED           ","2500 855 2ND ST SW            ","                              ",
		"CALGARY AB                    ","                              ","T2P4J8"," ","09579",
		"TRAILBLAZER DRILLING CORPORATION             ","1 444 2ND ST SE               ","                              ",
		"MEDICINE HAT AB               ","                              ","T1A0C3","01 DIKE REQD                     ",
		"69 BOTTOM DRAINAGE               ","68 PERF TARGET                   ","                                 ",
		"                                 ","                                 ","                                 ",
		"                                 ","                                 ","                                 "]

		testFile = "FL061127.csv"

		skLicence = licences.OldSKLicence(test_entry, testFile)

		self.assertEquals(skLicence.licencee, 'CANADIAN NATURAL RESOURCES LIMITED')
		self.assertEquals(skLicence.wellname, 'CNRL LASHBURN WEST DD 4A8-22-4A8-22-48-26')
		self.assertEquals(skLicence.licnum, '06K336')
		self.assertEquals(skLicence.uwi, '08-22-048-26W3')
		self.assertEquals(skLicence.year, '2006')
		self.assertEquals(skLicence.month, '11')
		self.assertEquals(skLicence.day, '27')
		self.assertEquals(skLicence.field, 'LLOYDMINSTER')
		self.assertEquals(skLicence.zone, 'LLOYDMINSTER')
		self.assertEquals(skLicence.direct, 'Vertical')
		self.assertEquals(skLicence.sub, 'Crude Oil')
		self.assertEquals(skLicence.subcode, '0')
		self.assertEquals(skLicence.lat, 53.15788561435807)
		self.assertEquals(skLicence.lng, -109.71445481647301)
		self.assertEquals(skLicence.province, 'SK')	

	def testMBLicence(self):
		testEntry = """Lic. No.: 10645   Tundra Daly Sinclair HZNTL 16-15-9-29 (WPM)
                  UWI: 102.16-15-009-29W1.00
                  Licence Issued: 26-Jan-2017
                  Licensee: Tundra Oil & Gas Partnership
                  Mineral Rights: Tundra Oil & Gas Partnership
                  Contractor: Trinidad Drilling Ltd. - Rig# 9
                  Surface Location: 13B-15-09-29
                  Co-ords: 215.85m (S) of (N) boundary of Sec. 15
                         76.00m (E) of (W) boundary of Sec. 15
                  Grd Elev: 534.93 m
                  Proj. TD: 2201.9 m (Mississippian)
                  Field: Daly Sinclair
                  Classification: DEVELOPMENT (NON CONFIDENTIAL)
                  Spud Date: 29-Jan-2017
                  K.B. Elevation: 538.93 m
                  Status: Drilling Ahead (DR)
                  Drilling Ahead: 30-Jan-2017"""

		mbLicence = licences.MBLicence(testEntry, {}, {})

		self.assertEquals(mbLicence.licencee, "Tundra Oil & Gas Partnership")
		self.assertEquals(mbLicence.wellname, "Tundra Daly Sinclair HZNTL 16-15-9-29 (WPM)")
		self.assertEquals(mbLicence.licnum, "10645")
		self.assertEquals(mbLicence.uwi, "102.16-15-009-29W1.00")
		self.assertEquals(mbLicence.year, "2017")
		self.assertEquals(mbLicence.month, "01")
		self.assertEquals(mbLicence.day, "26")
		self.assertEquals(mbLicence.field, "Daly Sinclair")
		self.assertEquals(mbLicence.zone, "Unknown")
		self.assertEquals(mbLicence.direct, "Horizontal")
		self.assertEquals(mbLicence.sub, "Unknown")
		self.assertEquals(mbLicence.subcode, "4")
		self.assertEquals(mbLicence.lat, 49.74766470926755)
		self.assertEquals(mbLicence.lng, -101.33068212572245)
		self.assertEquals(mbLicence.province, 'MB')	

if __name__ == '__main__':
	result = unittest.main()