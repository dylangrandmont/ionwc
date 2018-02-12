# Copyright (C) 2017-2018, Dylan Grandmont

import urllib
import urllib2
import os
import datetime
import calendar
import shutil
import glob
from constants import IONWC_HOME

class DataStream:
	days_window = 20
	today = datetime.datetime.now()

	url_opener = urllib.URLopener()

	def _isResponseXml(self, url):
		return 'text/xml' == urllib.urlopen(url).info().type

	def _isResponseOctet(self, url):
		return 'application/octet-stream' == urllib.urlopen(url).info().type

	def _isXZipCompressed(self, url):
		return 'application/x-zip-compressed' == urllib.urlopen(url).info().type


class DataStreamBC(DataStream):
	postings_directory = IONWC_HOME + '/data/postings/bc'
	spud_directory = IONWC_HOME + '/data/spud/bc'

	def retrieve_spuds(self):
		month_ago = self.today - datetime.timedelta(30)
		for date in [self.today, month_ago]:
			year = str(date.year)
			month = '%02d' % date.month

			in_name = 'rwservlet?prd_pimsr273+p_report_year=' + year + '+p_report_month=' + month
			out_name = self.spud_directory + '/bcogc-spud-' + year + '-' + month + '.pdf'

			print 'wget https://iris.bcogc.ca/reports/' + in_name + ' '  + out_name
			os.system('wget https://iris.bcogc.ca/reports/' + in_name + ' '  + out_name)

			os.system('pdftotext -layout ' + out_name)
			os.remove(out_name)

	def retrieve_licenses(self):
		os.system('wget https://reports.bcogc.ca/ogc/f?p=200:21:13026223742485:CSV:::: -O ' + IONWC_HOME +'/data/wells/bc/new_well_authorizations_issued.csv')

		os.system('grep -F -x -v -f $IONWC_HOME/data/wells/bc/well_authorizations_issued.csv $IONWC_HOME/data/wells/bc/new_well_authorizations_issued.csv > $IONWC_HOME/data/wells/bc/diff_well_authorizations_issued.csv')
		os.system('cat $IONWC_HOME/data/wells/bc/diff_well_authorizations_issued.csv >> $IONWC_HOME/data/wells/bc/well_authorizations_issued.csv')
		os.remove(IONWC_HOME + '/data/wells/bc/new_well_authorizations_issued.csv')
		os.remove(IONWC_HOME + '/data/wells/bc/diff_well_authorizations_issued.csv')

	def retrieve_land_postings(self):
		self._retrieve_land_posting_results()
		self._retrieve_land_posting_offerings()

	def retrieve_facilities(self):
		os.system('wget https://ams-reports.bcogc.ca/ords-prod/f?p=200:58:15168409196395:CSV:::: -O ' + IONWC_HOME +'/data/facilities/bc/facilities.csv')

	def _retrieve_land_posting_results(self):
		month_ago = self.today - datetime.timedelta(28)
		for date in [self.today, month_ago]:
			year = str(date.year)
			yr = year[2:4]
			month = calendar.month_abbr[date.month].lower()
			url = 'http://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/natural-gas-oil/png-crown-sale/results/' + month + yr + 'res.zip'
			if self._isXZipCompressed(url):
				os.system('wget -N ' + url + ' -P ' + self.postings_directory)
				os.system('unzip -o ' + self.postings_directory + '/' + month + yr + 'res.zip -d ' + self.postings_directory)

	def _retrieve_land_posting_offerings(self):
		one_month = self.today + datetime.timedelta(28)
		two_months = self.today + datetime.timedelta(56)
		three_months = self.today + datetime.timedelta(84)
		for date in [self.today, one_month, two_months, three_months]:
			year = str(date.year)
			yr = year[2:4]
			month = calendar.month_abbr[date.month].lower()

			url_octet = 'http://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/natural-gas-oil/png-crown-sale/sale-notices/' + year + '/' + month + yr + 'sal.rpt'
			url_zip   = 'http://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/natural-gas-oil/png-crown-sale/sale-notices/' + year + '/' + month + yr + 'sal.zip'
			if self._isResponseOctet(url_octet):
				os.system('wget -N ' + url_octet + ' -P ' + self.postings_directory)

			if self._isXZipCompressed(url_zip):
				os.system('wget -N ' + url_zip + ' -P ' + self.postings_directory)
				os.system('unzip -o ' + self.postings_directory + '/' + month + yr + 'sal.zip -d ' + self.postings_directory)

class DataStreamAB(DataStream):
	posting_window_ahead = 100
	posting_window_behind = 20
	postings_directory = IONWC_HOME +'/data/postings/ab'

	def _getDates(self, daysAgo):
		date = self.today - datetime.timedelta(daysAgo)
		year = str(date.year)
		month = '%02d' % date.month
		day = '%02d' % date.day
		return year, month, day

	def retrieve_spuds(self):
		for i in range(self.days_window):
			year, month, day = self._getDates(i)
			url = 'http://www.aer.ca/data/WELLS/SPUD' + month + day + '.TXT'
			if urllib.urlopen(url).getcode() != 404:
				self.url_opener.retrieve(url, IONWC_HOME +'/data/spud/' + year + '/SPUD' + month + day + '.TXT')

	def retrieve_licenses(self):
		for i in range(self.days_window):
			year, month, day = self._getDates(i)
			url = 'http://www.aer.ca/data/well-lic/WELLS' + month + day + '.TXT'
			if urllib.urlopen(url).getcode() != 404:
				self.url_opener.retrieve(url, IONWC_HOME + '/data/licences/' + year + '/WELLS' + month + day + '.TXT')
		
	def retrieve_land_postings(self):
		self._retrieve_land_posting_offerings()
		self._retrieve_land_posting_results()

	def retrieve_facilities(self):
		url = 'http://www.aer.ca/data/codes/ActiveFacility.txt'
		if urllib.urlopen(url).getcode() != 404:
			self.url_opener.retrieve(url, IONWC_HOME + '/data/facilities/ab/ActiveFacility.txt')

	def _retrieve_land_posting_results(self):
		for i in range(self.posting_window_behind):
			year, month, day = self._getDates(i)
			url = 'http://www.energy.alberta.ca/FTPPNG/' + year + month + day +'PSR.xml'
			if self._isResponseXml(url):
				os.system('wget -N ' + url + ' -P ' + self.postings_directory)

	def _retrieve_land_posting_offerings(self):
		for i in range(-1 * self.posting_window_ahead, self.posting_window_behind):
			year, month, day = self._getDates(i)
			url = 'http://www.energy.alberta.ca/FTPPNG/' + year + month + day +'PON.xml'
			if self._isResponseXml(url):
				os.system('wget -N ' + url + ' -P ' + self.postings_directory)


class DataStreamSK(DataStream):

	def retrieve_spuds(self):
		for i in range(self.days_window):
			date = datetime.datetime.now() - datetime.timedelta(i)
			year = str(date.year)
			month = '%02d' % date.month
			day = '%02d' % date.day

			url = 'http://www.economy.gov.sk.ca/Files/oilandgas/DrillingActivity/archives/DailyDrillingActivity-' + year + '-' + month + '-' + day + '.csv'
			if urllib.urlopen(url).getcode() != 404:
				self.url_opener.retrieve(url, IONWC_HOME + '/data/spud/sask/DailyDrillingActivity-' + year + '-' + month + '-' + day + '.csv')

	def retrieve_licenses(self):
		for i in range(self.days_window):
			date = datetime.datetime.now() - datetime.timedelta(i)
			year = str(date.year)
			yr = year[2:]
			month = '%02d' % date.month
			day = '%02d' % date.day

			url = 'http://www.economy.gov.sk.ca/Files/oilandgas/wellbullfile/archives/FL' + yr + month + day + '.csv'
			if urllib.urlopen(url).getcode() != 404:
				self.url_opener.retrieve(url, IONWC_HOME + '/data/licences/sask/FL' + yr + month + day + '.csv')

	def convertLandPostings(self):
		for file in os.listdir(IONWC_HOME + '/data/postings/sk'):
			os.rename(IONWC_HOME + '/data/postings/sk/' + file, IONWC_HOME + '/data/postings/sk/' + file.lower())

		for file in glob.glob(IONWC_HOME + '/data/postings/sk/' + '*.pdf'):
			os.system('pdftotext -layout ' + '"' + file + '"')

	def retrieve_facilities(self):
		url = 'http://economy.gov.sk.ca/files/Registry%20Downloads/NewAndActiveFacilitiesReport.csv'
		if urllib.urlopen(url).getcode() != 404:
			self.url_opener.retrieve(url, IONWC_HOME + '/data/facilities/sk/NewAndActiveFacilitiesReport.csv')


class DataStreamMB:
	activity_directory_data = IONWC_HOME + '/data/activity/mb/'
	activity_directory_raw = IONWC_HOME + '/raw_inputs/activity/mb/'
	wells_directory_data = IONWC_HOME + '/data/wells/mb/'
	wells_directory_raw = IONWC_HOME + '/raw_inputs/wells/mb/'
	postings_directory_data = IONWC_HOME + '/data/postings/mb/'
	postings_directory_raw = IONWC_HOME + '/raw_inputs/postings/mb/'

	def _hasConnection(self):
		try:
			url = urllib.urlopen('http://www.gov.mb.ca/iem/petroleum/wwar/')
			return (url.getcode() == 200)
		except:
			print 'No connection found for MB Data Stream'
			return False

	def retrieve_spuds(self):
		if (self._hasConnection()):
			os.system('wget -N -r -l1 --no-parent -A.pdf http://www.gov.mb.ca/iem/petroleum/wwar/ -P ' + self.activity_directory_raw)
			os.system('find ' + self.activity_directory_raw + ' -name \'*.pdf\' -exec cp -n -t ' + self.activity_directory_data + ' {} +')
			os.system('find ' + self.activity_directory_data + ' -type f ! -name \'*.pdf\' -delete')
			os.system('for file in ' + self.activity_directory_data + '*.pdf; do pdftotext -layout "$file" "$file.txt"; done')
			for file in glob.glob(self.activity_directory_data + '*.pdf'):
				os.remove(file)

	def retrieve_licenses(self):
		oneKiloByte = 1000
		uwi_weekly = urllib.urlopen('http://www.gov.mb.ca/iem/petroleum/reports/uwi_weekly.xls')
		if (self._is_content_length_over_1kB(uwi_weekly.info())):
			os.system('wget -N http://www.gov.mb.ca/iem/petroleum/reports/uwi_weekly.xls -P ' + self.wells_directory_raw)
			os.system('libreoffice --headless --convert-to csv ' + self.wells_directory_raw + 'uwi_weekly.xls --outdir ' + self.wells_directory_data)

	def retrieve_land_postings(self):
		os.system('wget -N -r -l1 --no-parent -A_results.pdf http://www.gov.mb.ca/iem/petroleum/landinfo/ -P ' + self.postings_directory_raw)
		os.system('wget -N -r -l1 --no-parent -A_sale.pdf http://www.gov.mb.ca/iem/petroleum/landinfo/ -P ' + self.postings_directory_raw)
		os.chdir(self.postings_directory_raw)

		for year in range(2006, 2016):
			os.system('find . -type f -name \'*' + str(year) + '*\' -delete')

		os.system('for file in ' + self.postings_directory_raw + 'www.gov.mb.ca/iem/petroleum/landinfo/*.pdf; do pdftotext -layout "$file"; done')
		os.system('find -name \'*results.txt\' -exec mv {} ' + self.postings_directory_data + ' \;')
		os.system('find -name \'*sale.txt\' -exec mv {} ' + self.postings_directory_data + ' \;')


	def _is_content_length_over_1kB(self, http_message):
		oneKiloByte = 1000
		try:
			return http_message.getheaders("Content-Length")[0] > oneKiloByte
		except:
			# This is due to a bug on the MB website
			return http_message.getheaders("Cteonnt-Length")[0] > oneKiloByte

def create_archive():
	now = datetime.datetime.now()
	date_stamp = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
	os.system('zip -r ' + IONWC_HOME + '/archives/data-' + date_stamp + '.zip ' + IONWC_HOME + '/data/ ')

def run_all():
	dataStreamBC = DataStreamBC()
	#TODO: fix BC data retrieval
	#dataStreamBC.retrieve_licenses()
	#dataStreamBC.retrieve_spuds()
	dataStreamBC.retrieve_land_postings()
	#dataStreamBC.retrieve_facilities()

	dataStreamAB = DataStreamAB()
	dataStreamAB.retrieve_spuds()
	dataStreamAB.retrieve_licenses()
	dataStreamAB.retrieve_land_postings()
	#dataStreamAB.retrieve_facilities()

	dataStreamSK = DataStreamSK()
	dataStreamSK.retrieve_spuds()
	dataStreamSK.retrieve_licenses()
	dataStreamSK.convertLandPostings()
	#dataStreamSK.retrieve_facilities()

	dataStreamMB = DataStreamMB()
	dataStreamMB.retrieve_spuds()
	dataStreamMB.retrieve_licenses()
	dataStreamMB.retrieve_land_postings()

	create_archive()