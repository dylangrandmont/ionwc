#!/bin/bash

##################################################################
# Copyright (C) 2017 Eye on Western Canada
#
# Well Licence Parsing
#
##################################################################

import datetime
import os
import re
import csv
import random
import numpy as np

from utilities import writeLicenseFile, conformSub, getSubCode, kmPerDegreeLatLng, conformBCOGCLatLon
from coordinatemapping import uwiToLatLng
from constants import IONWC_HOME, MONTH_DICT, BCWellNameToOperatorMap, BCWellNameToFieldMap, UNKNOWN, MBPoolCodeToZoneMap

class LicenceDatabase:
	def __init__(self, csvDatabase):
		self.csvDatabase = open(csvDatabase,'w')
		self.licences = []
		self.csvDatabase.write("Licensee,Well Name,License Number,UWI,Date,DateMonth,Field/Pool,\
						   TerminatingZone,Orientation,Substance,SubstanceCode,latitude,longitude,province\n")


	def add_licence(self, licence):
		self.licences.append(licence)

	def write_to_csv(self):
		for licence in self.licences:
			writeLicenseFile(self.csvDatabase, licence.licencee, licence.wellname, licence.licnum,
				             licence.uwi, licence.year, licence.month, licence.day, licence.field,
				             licence.zone, licence.direct, licence.sub, licence.subcode, licence.lat,
				             licence.lng, licence.province)

class Licence:
	srcFile = ''
	srcPath = ''

	licencee = UNKNOWN
	wellname = UNKNOWN
	licnum = UNKNOWN
	uwi = UNKNOWN
	year = UNKNOWN
	month = UNKNOWN
	day = UNKNOWN
	field = UNKNOWN
	zone = UNKNOWN
	direct = UNKNOWN
	sub = UNKNOWN
	subcode = UNKNOWN
	lat = UNKNOWN
	lng = UNKNOWN
	province = UNKNOWN

	def _xy_sign(self, direction):
		sign = 1
		if direction == 'S' or direction == 'W':
			sign = -1
		return sign

	def _safe_divide(self, a, b):
		if (abs(b) > 0.1):
			return a/b
		else:
			return 0

	def _trim_all(self):
		self.licencee = self.licencee.strip()
		self.wellname = self.wellname.strip()
		self.licnum = self.licnum.strip()
		self.uwi = self.uwi.strip()
		self.year = self.year.strip()
		self.month = self.month.strip()
		self.day = self.day.strip()
		self.field = self.field.strip()
		self.zone = self.zone.strip()
		self.direct = self.direct.strip()
		self.sub = self.sub.strip()

class ABLicence(Licence):
	def __init__(self, entry, srcFile, srcPath):
		self.srcFile = srcFile
		self.srcPath = srcPath

		self.entry = entry.split('\r\n')
		for i in range(len(self.entry)):
			self.entry[i] = self.entry[i].strip()

		self._set_licencee()
		self._set_wellname()
		self._set_licnum()
		self._set_uwi()
		self._set_year()
		self._set_month()
		self._set_day()
		self._set_field()
		self._set_zone()
		self._set_direct()
		self._set_sub()
		self._set_subcode()
		self._set_lat_lng()
		self._trim_all()
		self.province = "AB"

	def _set_licencee(self):
		""" Return first set of characters before two or more white spaces """
		self.licencee = re.split('\s\s+', self.entry[4])[0]

	def _set_wellname(self):
		""" Return first set of characters before two or more white-spaces """
		self.wellname = re.split('\s\s+', self.entry[0])[0]

	def _set_licnum(self):
		""" assume the first number of 5 or more digits is the licence number """
		possibleLicNums = re.findall('[0-9]{5,}', self.entry[0])
		self.licnum = possibleLicNums[0]

	def _set_uwi(self):
		""" Return second line, first entry """
		self.uwi = re.split('\s\s+', self.entry[1])[0]

	def _set_year(self):
		self.year = self.year = self.srcPath.strip('/')[-4:]

	def _set_month(self):
		self.month = self.srcFile[5:7]

	def _set_day(self):
		self.day = self.srcFile[7:9]

	def _set_field(self):
		""" Third line, after first two consectutive white spaces """
		self.field = re.split('\s\s+', self.entry[2])[1]

	def _set_zone(self):
		""" Third line, last entry after consectutive white spaces """
		self.zone = re.split('\s\s+', self.entry[2])[-1]

	def _set_direct(self):
		""" Return first set of characters before two or more white-spaces """
		self.direct = re.split('\s\s+', self.entry[3])[0]

	def _set_sub(self):
		self.sub = conformSub( re.split('\s\s+', self.entry[3])[-1]	)

	def _set_subcode(self):
		self.subcode = getSubCode(self.sub)

	def _set_lat_lng(self):
		metersPerKm = 1000.0

		surfUWI = re.split('\s\s+', self.entry[4])[-1]
		offsets = re.split('\s+', self.entry[1])[1:5]

		yOffset = self._xy_sign(offsets[0]) * float(offsets[1][:-1]) / metersPerKm
		xOffset = self._xy_sign(offsets[2]) * float(offsets[3][:-1]) / metersPerKm

		lat, lng = uwiToLatLng.convert(surfUWI)

		kmPerDegreeLat, kmPerDegreeLng = kmPerDegreeLatLng(lat)

		self.lat = lat + self._safe_divide(yOffset, kmPerDegreeLat)
		self.lng = lng + self._safe_divide(xOffset, kmPerDegreeLng)


class BCLicence(Licence):
	def __init__(self, row):
		self.row = row

		self._set_licencee()
		self._set_wellname()
		self._set_licnum()
		self._set_uwi()
		self._set_year()
		self._set_month()
		self._set_day()
		self._set_field()
		self._set_zone()
		self._set_direct()
		self._set_sub()
		self._set_subcode()
		self._set_lat_lng()
		self._trim_all()
		self.province = "BC"

	def _set_licencee(self):
		self.licencee = self.row[1].replace(',','')

	def _set_wellname(self):
		self.wellname = self.row[4]

	def _set_licnum(self):
		self.licnum = self.row[0]

	def _set_uwi(self):
		self.uwi = self.row[14]

	def _set_year(self):
		self.year = self.row[2].split('-')[-1]

	def _set_month(self):
		self.month = MONTH_DICT[self.row[2].split('-')[1]]

	def _set_day(self):
		self.day = self.row[2].split('-')[0]

	def _set_field(self):
		for key in BCWellNameToFieldMap:
			if key in self.wellname.lower():
				self.field = BCWellNameToFieldMap[key]

	def _set_zone(self):
		self.zone = self.row[13]

	def _set_direct(self):
		self.direct = UNKNOWN

	def _set_sub(self):
		self.sub = conformSub(self.row[6])

	def _set_subcode(self):
		self.subcode = getSubCode(self.sub)

	def _set_lat_lng(self):
		try:
			self.lat, self.lng = conformBCOGCLatLon(self.row[8], self.row[9])
		except:
			print "INFO:  not able to find lat, long in BCOGC licence, using UWI", self.row
			if self.uwi[-4]=="W":   
				uwiIn="00/" + self.uwi[3:5] + "-" + self.uwi[5:7] + "-" + self.uwi[7:10] + "-" + self.uwi[10:14] + "/0"                     
				self.lat, self.lng = uwiToLatLng.convert(uwiIn)                                                                         
			else:                                                                                                           
				self.lat, self.lng = uwiToLatLng.convert(self.uwi, grid="NTS")  
			random.seed(int(re.sub("[^0-9]","", self.licnum)))       
			self.lat += random.uniform(-0.0005,0.0005)                                                                        
			self.lng += random.uniform(-0.0005,0.0005)   


class OldSKLicence(Licence):
	def __init__(self, row, srcFile):
		self.row = row
		self.srcFile = srcFile

		self._set_licencee()
		self._set_wellname()
		self._set_licnum()
		self._set_uwi()
		self._set_year()
		self._set_month()
		self._set_day()
		self._set_field()
		self._set_zone()
		self._set_direct()
		self._set_sub()
		self._set_subcode()
		self._set_lat_lng()
		self.province = "SK"

		self._trim_all()

	def _set_licencee(self):
		self.licencee = self.row[122].replace(',','')

	def _set_wellname(self):
		self.wellname = self.row[30].replace(',','')

	def _set_licnum(self):
		self.licnum = self.row[13].replace('\xa0','')

	def _set_uwi(self):
		self.uwi = self.row[3] + '-' + self.row[4] + '-' + self.row[5].zfill(3) + '-' + self.row[6] + 'W' + self.row[7]

	def _set_year(self):
		self.year = '20' + self.srcFile[2:4]

	def _set_month(self):
		self.month = self.srcFile[4:6]

	def _set_day(self):
		self.day = self.srcFile[6:8]

	def _set_field(self):
		self.field = self.row[116]

	def _set_zone(self):
		self.zone = self.row[90]

	def _set_direct(self):
		if ' hz ' in self.wellname:
			self.direct = "Horiztonal"
		else:
			self.direct = "Vertical"

	def _set_sub(self):
		self.sub = conformSub(self.row[101])

	def _set_subcode(self):
		self.subcode = getSubCode(self.sub)

	def _set_lat_lng(self):
		metersPerKm = 1000.0

		surfuwi = self.row[3] + '-' + self.row[4] + '-' + self.row[5].zfill(3) + '-' + self.row[6] + 'W' + self.row[7]
		offsets = [self.row[44], self.row[42], self.row[48], self.row[46]]
		lat, lng = uwiToLatLng.convert("00/"+ surfuwi +"/0")

		yOffset = self._xy_sign(offsets[0]) * float(offsets[1]) / metersPerKm
		xOffset = self._xy_sign(offsets[2]) * float(offsets[3]) / metersPerKm

		kmPerDegreeLat, kmPerDegreeLng = kmPerDegreeLatLng(lat)

		self.lat = lat + self._safe_divide(yOffset, kmPerDegreeLat)
		self.lng = lng + self._safe_divide(xOffset, kmPerDegreeLng)

 	def _conform_sk_zone(self, zone):
		if 'viking' in zone.lower(): conformedZone = "Viking"
		elif 'bakken' in zone.lower(): conformedZone = "Bakken"
		elif 'sparky' in zone.lower(): conformedZone = "Sparky"
		elif 'lower shaunavon' in zone.lower(): conformedZone = "Lower Shaunavon"
		elif ' l shaunavon' in zone.lower(): conformedZone = "Lower Shaunavon"
		elif ' u shaunavon' in zone.lower(): conformedZone = "Upper Shaunavon"
		elif 'upper shaunavon' in zone.lower(): conformedZone = "Upper Shaunavon"
		elif 'shaunavon' in zone.lower(): conformedZone = "Shaunavon"
		else: raise Exception('No Zone found for SASK field pool', zone, self.row, self.srcFile)

		return conformedZone

class NewSKLicence(Licence):
	def __init__(self, well_bore_entry, completion_entry, srcFile):
		self.well_bore_entry = well_bore_entry
		self.completion_entry = completion_entry
		self.srcFile = srcFile

		self._set_licencee()
		self._set_wellname()
		self._set_licnum()
		self._set_uwi()
		self._set_year()
		self._set_month()
		self._set_day()
		self._set_field()
		self._set_zone()
		self._set_direct()
		self._set_sub()
		self._set_subcode()
		self._set_lat_lng()
		self.province = "SK"

		self._trim_all()

	def _set_licencee(self):
		self.licencee = self.well_bore_entry[7].replace(',','')

	def _set_wellname(self):
		self.wellname = ''

	def _set_licnum(self):
		self.licnum = self.well_bore_entry[5].replace(' ','')

	def _set_uwi(self):
		self.uwi = self.well_bore_entry[34]

	def _set_year(self):
		self.year = '20' + self.srcFile[2:4]

	def _set_month(self):
		self.month = self.srcFile[4:6]

	def _set_day(self):
		self.day = self.srcFile[6:8]

	def _set_field(self):
		self.field = self.completion_entry[39]

	def _set_zone(self):
		self.zone = self.well_bore_entry[54]

	def _set_direct(self):
		self.direct = self.well_bore_entry[10]

	def _set_sub(self):
		self.sub = conformSub(self.completion_entry[37])

	def _set_subcode(self):
		self.subcode = getSubCode(self.sub)

	def _set_lat_lng(self):
		metersPerKm = 1000.0

		surfuwi = self.well_bore_entry[18]
		offsets = [self.well_bore_entry[15], self.well_bore_entry[14], self.well_bore_entry[17], self.well_bore_entry[16]]

		lat, lng = uwiToLatLng.convert("00/"+ surfuwi +"/0")

		yOffset = self._xy_sign(offsets[0]) * float(offsets[1]) / metersPerKm
		xOffset = self._xy_sign(offsets[2]) * float(offsets[3]) / metersPerKm

		kmPerDegreeLat, kmPerDegreeLng = kmPerDegreeLatLng(lat)

		self.lat = lat + self._safe_divide(yOffset, kmPerDegreeLat)
		self.lng = lng + self._safe_divide(xOffset, kmPerDegreeLng)



class MBLicence(Licence):
	def __init__(self, entry, licenceToPoolCodeMap, licenceToOrientationMap):
		self.licenceToPoolCodeMap = licenceToPoolCodeMap
		self.licenceToOrientationMap = licenceToOrientationMap
		self.meridian = UNKNOWN
		self.entry = entry

		self._set_date()
		self._set_year()
		self._set_month()
		self._set_day()
		self._set_licencee()
		self._set_wellname()
		self._set_licnum()
		self._set_uwi()
		self._set_field()
		self._set_zone()
		self._set_direct()
		self._set_subcode()
		self._set_lat_lng()
		self.province = "MB"

		self._trim_all()

	def _set_date(self):
		self.date = re.sub('Licence Issued:\s+', '', re.findall('Licence Issued:.*', self.entry)[0]).strip()

	def  _set_year(self):
		self.year = self.date.split('-')[2]

	def _set_month(self):
		self.month = MONTH_DICT[self.date.split('-')[1].upper()]

	def _set_day(self):
		self.day = self.date.split('-')[0]

	def _set_licencee(self):
		self.licencee = re.sub('Licensee: ', '', re.findall('Licensee:.*', self.entry)[0])

	def _set_wellname(self):
		wellNameLine = re.findall('Lic. No.:.*', self.entry)[0]
		self.wellname = re.sub('Lic. No.: [0-9]+', '', wellNameLine).strip()
		if '(WPM)' in self.wellname or '(PM)' in self.wellname or 'W1' in self.wellname:
			self.meridian = '1'
		else:
			raise Exception('Unknown meridian found in wellname', self.wellname)

	def _set_licnum(self):
		self.licnum = re.sub('Lic. No.[:\s]+', '', re.findall('Lic. No.[:\s]+[0-9]+', self.entry)[0]).strip()

	def _set_uwi(self):
		self.uwi = re.sub('UWI:[\s]+', '', re.findall('UWI:.*', self.entry)[0])

	def _set_field(self):
		if len(re.findall('Field: .*', self.entry)) == 1:
			self.field = re.sub('Field:\s+', '', re.findall('Field: .*', self.entry)[0])
		elif len(re.findall('Area: .*', self.entry)) == 1:
			self.field = re.sub('Area:\s+', '', re.findall('Area: .*', self.entry)[0])

	def _set_zone(self):
		try:
			poolCode = self.licenceToPoolCodeMap[self.licnum]
			for key in MBPoolCodeToZoneMap:
				if key in poolCode:
					self.zone = MBPoolCodeToZoneMap[key]
		except:
			print 'WARN: licnum ', self.licnum, ' has no MB pool'

	def _set_direct(self):
		try:
			self.direct = self.licenceToOrientationMap[self.licnum].title().replace('Hzntl', 'Horizontal')
		except:
			if 'HZNTL' in self.wellname:
				self.direct = "Horizontal"


	def _set_subcode(self):
		self.subcode = getSubCode(self.sub)

	def _set_lat_lng(self):
		if len(re.findall('Surface Location:.*', self.entry)) == 1:
			surfuwi = re.sub('Surface Location:\s+', '', re.findall('Surface Location:.*', self.entry)[0])
		elif len(re.findall('Surf. Location:.*', self.entry)) == 1:
			surfuwi = re.sub('Surf. Location:\s+', '', re.findall('Surf. Location:.*', self.entry)[0])
		elif len(re.findall('UWI:.*', self.entry)) == 1:
			surfuwi = re.sub('UWI:\s+', '', re.findall('UWI:.*', self.entry)[0])
			surfuwi = re.sub('[0-9][0-9][0-9]\.', '', surfuwi)
			surfuwi = re.sub('W[0-9]\.[0-9][0-9]', '', surfuwi)
		else:
			raise Exception('No valid surface uwi found ', self.entry)

		offsets = re.sub('Co-ords: ', '', re.findall('Co-ords.*\n.*', self.entry)[0])
		offsets = re.sub(' W ', ' (W) ', re.sub(' E ', ' (E) ', re.sub(' N', ' (N) ', re.sub(' S ',' (S) ', offsets))))

		gridPosition = self._get_grid_position(offsets)
		surfuwi = self._conform_uwi(surfuwi)

		if gridPosition == 'ne': 
			surfuwi = '-'.join(['16'] + surfuwi.split('-')[1:])
		elif gridPosition == 'nw':
			surfuwi = '-'.join(['09'] + surfuwi.split('-')[1:])
		elif gridPosition == 'sw':
			surfuwi = '-'.join(['04'] + surfuwi.split('-')[1:])
		elif gridPosition == 'se':
			surfuwi = '-'.join(['01'] + surfuwi.split('-')[1:])

		lat, lng = uwiToLatLng.convert(surfuwi, position = gridPosition)
		latOffset, lngOffset = self._calc_offset(offsets, lat)
		self.lat = lat + latOffset
		self.lng = lng + lngOffset

	def _conform_uwi(self, uwi):
		conformedUWI = re.sub('\s+\(WPM\)\s?', '', uwi)
		conformedUWI = re.sub('[a-zA-z]', '', conformedUWI)
		conformedUWI = conformedUWI.split('-')
		conformedUWI[2] = conformedUWI[2].zfill(3)
		conformedUWI[3] = conformedUWI[3].zfill(2)
		conformedUWI = '-'.join(conformedUWI)
		conformedUWI = '00/' + conformedUWI + 'W' + self.meridian + '/0'

		return conformedUWI

	def _get_grid_position(self, offsetString):
		offsetDirections = re.findall('\([SNEW]\)', offsetString)
		gridPosition = offsetDirections[1].replace(')', '').replace('(', '').lower()
		gridPosition += offsetDirections[3].replace(')', '').replace('(', '').lower()
		return gridPosition

	def _calc_offset(self, offsetString, lat):
		metersPerKm = 1000.0

		offsetDirections = re.findall('\([SNEW]\)', offsetString)
		offsetDistance = re.findall('[0-9]+\.[0-9]?', offsetString)
		yOffsetDirection = offsetDirections[0].replace(')', '').replace('(', '')
		xOffsetDirection = offsetDirections[1].replace(')', '').replace('(', '')
		yOffsetDistance = offsetDistance[0]
		xOffsetDistance = offsetDistance[1]
		yOffset = self._xy_sign(yOffsetDirection) * float(yOffsetDistance) / metersPerKm
		xOffset = self._xy_sign(xOffsetDirection) * float(xOffsetDistance) / metersPerKm

		kmPerDegreeLat, kmPerDegreeLng = kmPerDegreeLatLng(lat)

		latOffset = self._safe_divide(yOffset, kmPerDegreeLat)
		lngOffset = self._safe_divide(xOffset, kmPerDegreeLng)

		return latOffset, lngOffset


class LicenceManager:
	startYear = 2010
	yearRange = map(str, range(startYear, datetime.datetime.now().year + 1) )


class ABLicenceManager(LicenceManager):
	""" Manage parsing and population of licence database for AB """

	def __init__(self, licenceDatabase):
		self.licenceDatabase = licenceDatabase
		self.files = []

	def populate_database(self):
		""" Add all licences to the database """
		self._get_files()
		for file in self.files:
			name = file.split('/')[-1]
			path = file.replace(name, '')
			entries = self._entry_from_file(file)
			for entry in entries:
				licence = ABLicence(entry, name, path)
				self.licenceDatabase.add_licence(licence)

	def _get_files(self):
		""" Retreive all the AB licence files """
		for year in self.yearRange:
			path = IONWC_HOME + '/data/licences/' + year + '/'
			for (dirpath, dirnames, filenames) in os.walk(path):

				for filename in filenames:
					self.files.append(path + filename)
				break

	def _entry_from_file(self, file):
		""" From each AB licence file, find all patterns for licence entries """
		line1 = '[a-zA-Z0-9].+\s.+[0-9]M\s+'
		line2 = '\s+[0-9].+[0-9]M\s+'
		line3 = '\s+[\w].+[\w].+'
		line4 = '\s+\w.+\w\s+'
		line5 = line4
		blank = '\s+'
		pattern = line1 + '\r\n' + line2 + '\r\n' + line3 + '\r\n' + line4 + '\r\n' + line4 + '\r\n' + blank + '\r\n'

		fileContent = ''.join(open(file).readlines())
		return re.findall(pattern, fileContent)

class BCLicenceManager(LicenceManager):
	allLicencesFile = IONWC_HOME + '/data/wells/bc/well_authorizations_issued.csv'

	def __init__(self, licenceDatabase):
		self.licenceDatabase = licenceDatabase
		self.allLicencesReader = csv.reader(open(self.allLicencesFile))
		# Skip header (first row)
		next(self.allLicencesReader)

	def populate_database(self):
		for row in self.allLicencesReader:
			try:
				if len(row) > 2:
					year = row[2].split('-')[-1]

					if int(year) >= self.startYear:
						licence = BCLicence(row)
						self.licenceDatabase.add_licence(licence)
			except:
				print 'WARN: Skipping row: ', row

class SKLicenceManager(LicenceManager):
	licenceDirectory = IONWC_HOME + '/data/licences/sask/'

	def __init__(self, licenceDatabase):
		self.licenceDatabase = licenceDatabase
		self.files = []

	def populate_database(self):
		self._get_files()
		for file in self.files:
			name = file.split('/')[-1]
			entries = self._rows_from_file(file, self._is_after_nov_2015(file))

			if (self._is_after_nov_2015(file)):

				for entry in entries:
					well_bore_entry = entry[0]
					completion_entry = entry[1]
					licence = NewSKLicence(well_bore_entry, completion_entry, name)
					self.licenceDatabase.add_licence(licence)

			else:
				for entry in entries:
					licence = OldSKLicence(entry, name)
					self.licenceDatabase.add_licence(licence)


	def _get_files(self):
		""" Retreive all the SK licence files """
		for (dirpath, dirnames, filenames) in os.walk(self.licenceDirectory):

			for filename in filenames:
				if int(filename[2:4]) >= int(str(self.startYear)[2:4]):
					self.files.append(filename)
			break


	def _rows_from_file(self, file, is_after_nov_2015):
		""" From each SK licence file, find all patterns for licence entries """
		entries = []

		for row in csv.reader(open(self.licenceDirectory + file,'r')): 
			if is_after_nov_2015:
				if ('new' in row[0].lower()):
					entries.append(row)
			else:
				if ('new' in row[1].lower()):
					entries.append(row)

		if is_after_nov_2015:
			for row in csv.reader(open(self.licenceDirectory + file,'r')):              
				if ('new' in row[0].lower()):
					entries.append(row)

			paired_entries = []
			index = 0

			# TODO: handle the case where there are multiple completions per wellbore

			well_bore_entries = []
			completion_entries = []

			for entry in entries:
				if self._is_well_bore_licence(entry):
					well_bore_entries.append(entry)
				elif self._is_completion_licence(entry):
					completion_entries.append(entry)

			for well_bore_entry in well_bore_entries:

				paired_entries.append([well_bore_entry, []])

				for completion_entry in completion_entries:
					if self._are_licnums_equal(well_bore_entry, completion_entry):
						paired_entries[-1] = [well_bore_entry, completion_entry]

			return paired_entries

		return entries

	def _is_after_nov_2015(self, file):

		year = '20' + file[2:4]
		month = file[4:6]
		day = file[6:8]

		if int(year) > 2015:
			return True
		elif (year == '2015' and int(month) >= 11):
			if int(month) == 12:
				 return True
			elif int(month) == 11 and int(day) > 6:
				return True

		return False

	def _are_licnums_equal(self, entry1, entry2):
		return entry1[5].replace(' ','') == entry2[5].replace(' ','')

	def _is_well_bore_licence(self, entry):
		return entry[33].lower().strip() == 'wellbore'

	def _is_completion_licence(self, entry):
		return entry[33].lower().strip() == 'completion'


class MBLicenceManager(LicenceManager):
	allLicencesFile = IONWC_HOME + '/data/wells/mb/uwi_weekly.csv'
	activityDirectory = IONWC_HOME + '/data/activity/mb/'
	poolCodes = []
	files = []

	def __init__(self, licenceDatabase):
		self.licenceDatabase = licenceDatabase
		self.allLicences = np.genfromtxt(self.allLicencesFile, delimiter=",", invalid_raise=False, comments=None, dtype=str)
		self.allLicenceNums = list(self.allLicences[:,[2]].ravel())
		self.allFields = list(self.allLicences[:,[6]].ravel())
		self.allPools = list(self.allLicences[:,[7]].ravel())
		self.allOrientations = list(self.allLicences[:,15].ravel())
		self._get_pool_codes()
		self.licenceToPoolCodeMap = dict(zip(self.allLicenceNums, self.poolCodes))
		self.licenceToOrientationMap = dict(zip(self.allLicenceNums, self.allOrientations))

	def populate_database(self):
		self._get_files()
		for file in self.files:
			entries = self._entry_from_file(file)
			for entry in entries:
				licence = MBLicence(entry, self.licenceToPoolCodeMap, self.licenceToOrientationMap)
				self.licenceDatabase.add_licence(licence)

	def _get_pool_codes(self):
		for i in range(len(self.allPools)):
			self.poolCodes.append(self.allFields[i] + self.allPools[i])

	def _get_files(self):
		for (dirpath, dirnames, filenames) in os.walk(self.activityDirectory):
			for filename in filenames:
				if int(filename[0:2]) >= int(str(self.startYear)[2:]):
					self.files.append(filename)
			break

	def _entry_from_file(self, file):
		pattern = 'Lic. No.*?Licence Issued.*?Licensee.*?Status.*?\n\n'
		content = ''.join(open(self.activityDirectory + file, 'r').readlines())
		licenceEntries = []
		allEntries = re.findall(pattern, content, re.DOTALL)
		for entry in allEntries:
			if len(re.findall('Lic. No', entry)) == 1:
				licenceEntries.append(entry)
		return licenceEntries

