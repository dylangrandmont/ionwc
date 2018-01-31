import urllib
import urllib2
import os
import datetime
import calendar
import shutil
import glob
from constants import IONWC_HOME

class DataStream:
	daysWindow = 20
	today = datetime.datetime.now()

	urlOpener = urllib.URLopener()

	def _isResponseXml(self, url):
		return 'text/xml' == urllib.urlopen(url).info().type

	def _isResponseOctet(self, url):
		return 'application/octet-stream' == urllib.urlopen(url).info().type

	def _isXZipCompressed(self, url):
		return 'application/x-zip-compressed' == urllib.urlopen(url).info().type


class DataStreamBC(DataStream):
	postingDirectory = IONWC_HOME + '/data/postings/bc'
	spudDirectory = IONWC_HOME + '/data/spud/bc'

	def retrieveSpuds(self):
		monthAgo = self.today - datetime.timedelta(30)
		for date in [self.today, monthAgo]:
			year = str(date.year)
			month = '%02d' % date.month

			inName = 'rwservlet?prd_pimsr273+p_report_year=' + year + '+p_report_month=' + month
			outName = self.spudDirectory + '/bcogc-spud-' + year + '-' + month + '.pdf'

			print 'wget https://iris.bcogc.ca/reports/' + inName + ' '  + outName
			os.system('wget https://iris.bcogc.ca/reports/' + inName + ' '  + outName)

			os.system('pdftotext -layout ' + outName)
			os.remove(outName)

	def retrieveLicences(self):
		os.system('wget https://ams-reports.bcogc.ca/ords-prod/f?p=200:21:21525241583986:CSV:::: -O ' + IONWC_HOME +'/data/wells/bc/new_well_authorizations_issued.csv')

		os.system('grep -F -x -v -f $IONWC_HOME/data/wells/bc/well_authorizations_issued.csv $IONWC_HOME/data/wells/bc/new_well_authorizations_issued.csv > $IONWC_HOME/data/wells/bc/diff_well_authorizations_issued.csv')
		os.system('cat $IONWC_HOME/data/wells/bc/diff_well_authorizations_issued.csv >> $IONWC_HOME/data/wells/bc/well_authorizations_issued.csv')
		os.remove(IONWC_HOME + '/data/wells/bc/new_well_authorizations_issued.csv')
		os.remove(IONWC_HOME + '/data/wells/bc/diff_well_authorizations_issued.csv')

	def retrieveLandPostings(self):
		self._retrieveLandPostingsResults()
		self._retrieveLandPostingsOfferings()

	def retrieveFacilities(self):
		os.system('wget https://ams-reports.bcogc.ca/ords-prod/f?p=200:58:15168409196395:CSV:::: -O ' + IONWC_HOME +'/data/facilities/bc/facilities.csv')

	def _retrieveLandPostingsResults(self):
		monthAgo = self.today - datetime.timedelta(28)
		for date in [self.today, monthAgo]:
			year = str(date.year)
			yr = year[2:4]
			month = calendar.month_abbr[date.month].lower()
			url = 'http://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/natural-gas-oil/png-crown-sale/results/' + month + yr + 'res.zip'
			if self._isXZipCompressed(url):
				os.system('wget -N ' + url + ' -P ' + self.postingDirectory)
				os.system('unzip -o ' + self.postingDirectory + '/' + month + yr + 'res.zip -d ' + self.postingDirectory)

	def _retrieveLandPostingsOfferings(self):
		oneMonth = self.today + datetime.timedelta(28)
		twoMonth = self.today + datetime.timedelta(56)
		threeMonth = self.today + datetime.timedelta(84)
		for date in [self.today, oneMonth, twoMonth, threeMonth]:
			year = str(date.year)
			yr = year[2:4]
			month = calendar.month_abbr[date.month].lower()

			urlOctet = 'http://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/natural-gas-oil/png-crown-sale/sale-notices/' + year + '/' + month + yr + 'sal.rpt'
			urlZip   = 'http://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/natural-gas-oil/png-crown-sale/sale-notices/' + year + '/' + month + yr + 'sal.zip'
			if self._isResponseOctet(urlOctet):
				os.system('wget -N ' + urlOctet + ' -P ' + self.postingDirectory)

			if self._isXZipCompressed(urlZip):
				os.system('wget -N ' + urlZip + ' -P ' + self.postingDirectory)
				os.system('unzip -o ' + self.postingDirectory + '/' + month + yr + 'sal.zip -d ' + self.postingDirectory)

class DataStreamAB(DataStream):
	postingWindowAhead = 100
	postingWindowBehind = 20
	postingDirectory = IONWC_HOME +'/data/postings/ab'

	def _getDates(self, daysAgo):
		date = self.today - datetime.timedelta(daysAgo)
		year = str(date.year)
		month = '%02d' % date.month
		day = '%02d' % date.day
		return year, month, day

	def retrieveSpuds(self):
		for i in range(self.daysWindow):
			year, month, day = self._getDates(i)
			url = 'http://www.aer.ca/data/WELLS/SPUD' + month + day + '.TXT'
			if urllib.urlopen(url).getcode() != 404:
				self.urlOpener.retrieve(url, IONWC_HOME +'/data/spud/' + year + '/SPUD' + month + day + '.TXT')

	def retrieveLicences(self):
		for i in range(self.daysWindow):
			year, month, day = self._getDates(i)
			url = 'http://www.aer.ca/data/well-lic/WELLS' + month + day + '.TXT'
			if urllib.urlopen(url).getcode() != 404:
				self.urlOpener.retrieve(url, IONWC_HOME + '/data/licences/' + year + '/WELLS' + month + day + '.TXT')
		
	def retrieveLandPostings(self):
		self._retrieveLandPostingsOfferings()
		self._retrieveLandPostingsResults()

	def retrieveFacilities(self):
		url = 'http://www.aer.ca/data/codes/ActiveFacility.txt'
		if urllib.urlopen(url).getcode() != 404:
			self.urlOpener.retrieve(url, IONWC_HOME + '/data/facilities/ab/ActiveFacility.txt')

	def _retrieveLandPostingsResults(self):
		for i in range(self.postingWindowBehind):
			year, month, day = self._getDates(i)
			url = 'http://www.energy.alberta.ca/FTPPNG/' + year + month + day +'PSR.xml'
			if self._isResponseXml(url):
				os.system('wget -N ' + url + ' -P ' + self.postingDirectory)

	def _retrieveLandPostingsOfferings(self):
		for i in range(-1 * self.postingWindowAhead, self.postingWindowBehind):
			year, month, day = self._getDates(i)
			url = 'http://www.energy.alberta.ca/FTPPNG/' + year + month + day +'PON.xml'
			if self._isResponseXml(url):
				os.system('wget -N ' + url + ' -P ' + self.postingDirectory)


class DataStreamSK(DataStream):

	def retrieveSpuds(self):
		for i in range(self.daysWindow):
			date = datetime.datetime.now() - datetime.timedelta(i)
			year = str(date.year)
			month = '%02d' % date.month
			day = '%02d' % date.day

			url = 'http://www.economy.gov.sk.ca/Files/oilandgas/DrillingActivity/archives/DailyDrillingActivity-' + year + '-' + month + '-' + day + '.csv'
			if urllib.urlopen(url).getcode() != 404:
				self.urlOpener.retrieve(url, IONWC_HOME + '/data/spud/sask/DailyDrillingActivity-' + year + '-' + month + '-' + day + '.csv')

	def retrieveLicences(self):
		for i in range(self.daysWindow):
			date = datetime.datetime.now() - datetime.timedelta(i)
			year = str(date.year)
			yr = year[2:]
			month = '%02d' % date.month
			day = '%02d' % date.day

			url = 'http://www.economy.gov.sk.ca/Files/oilandgas/wellbullfile/archives/FL' + yr + month + day + '.csv'
			if urllib.urlopen(url).getcode() != 404:
				self.urlOpener.retrieve(url, IONWC_HOME + '/data/licences/sask/FL' + yr + month + day + '.csv')

	def convertLandPostings(self):
		for file in os.listdir(IONWC_HOME + '/data/postings/sk'):
			os.rename(IONWC_HOME + '/data/postings/sk/' + file, IONWC_HOME + '/data/postings/sk/' + file.lower())

		for file in glob.glob(IONWC_HOME + '/data/postings/sk/' + '*.pdf'):
			os.system('pdftotext -layout ' + '"' + file + '"')

	def retrieveFacilities(self):
		url = 'http://economy.gov.sk.ca/files/Registry%20Downloads/NewAndActiveFacilitiesReport.csv'
		if urllib.urlopen(url).getcode() != 404:
			self.urlOpener.retrieve(url, IONWC_HOME + '/data/facilities/sk/NewAndActiveFacilitiesReport.csv')


class DataStreamMB:
	activityDirectoryData = IONWC_HOME + '/data/activity/mb/'
	activityDirectoryRaw = IONWC_HOME + '/raw_inputs/activity/mb/'
	wellsDirectoryData = IONWC_HOME + '/data/wells/mb/'
	wellsDirectoryRaw = IONWC_HOME + '/raw_inputs/wells/mb/'
	postingDirectoryData = IONWC_HOME + '/data/postings/mb/'
	postingDirectoryRaw = IONWC_HOME + '/raw_inputs/postings/mb/'

	def _hasConnection(self):
		try:
			url = urllib.urlopen('http://www.gov.mb.ca/iem/petroleum/wwar/')
			return (url.getcode() == 200)
		except:
			print 'No connection found for MB Data Stream'
			return False

	def retrieveSpuds(self):
		if (self._hasConnection()):
			os.system('wget -N -r -l1 --no-parent -A.pdf http://www.gov.mb.ca/iem/petroleum/wwar/ -P ' + self.activityDirectoryRaw)
			os.system('find ' + self.activityDirectoryRaw + ' -name \'*.pdf\' -exec cp -n -t ' + self.activityDirectoryData + ' {} +')
			os.system('find ' + self.activityDirectoryData + ' -type f ! -name \'*.pdf\' -delete')
			os.system('for file in ' + self.activityDirectoryData + '*.pdf; do pdftotext -layout "$file" "$file.txt"; done')
			for file in glob.glob(self.activityDirectoryData + '*.pdf'):
				os.remove(file)

	def retrieveLicences(self):
		oneKiloByte = 1000
		uwiWeekly = urllib.urlopen('http://www.gov.mb.ca/iem/petroleum/reports/uwi_weekly.xls')
		if (uwiWeekly.info().getheaders("Content-Length")[0] > oneKiloByte):
			os.system('wget -N http://www.gov.mb.ca/iem/petroleum/reports/uwi_weekly.xls -P ' + self.wellsDirectoryRaw)
			os.system('libreoffice --headless --convert-to csv ' + self.wellsDirectoryRaw + 'uwi_weekly.xls --outdir ' + self.wellsDirectoryData)

	def retrieveLandPostings(self):
		os.system('wget -N -r -l1 --no-parent -A_results.pdf http://www.gov.mb.ca/iem/petroleum/landinfo/ -P ' + self.postingDirectoryRaw)
		os.system('wget -N -r -l1 --no-parent -A_sale.pdf http://www.gov.mb.ca/iem/petroleum/landinfo/ -P ' + self.postingDirectoryRaw)
		os.chdir(self.postingDirectoryRaw)

		for year in range(2006, 2016):
			os.system('find . -type f -name \'*' + str(year) + '*\' -delete')

		os.system('for file in ' + self.postingDirectoryRaw + 'www.gov.mb.ca/iem/petroleum/landinfo/*.pdf; do pdftotext -layout "$file"; done')
		os.system('find -name \'*results.txt\' -exec mv {} ' + self.postingDirectoryData + ' \;')
		os.system('find -name \'*sale.txt\' -exec mv {} ' + self.postingDirectoryData + ' \;')


def createArchive():
	now = datetime.datetime.now()
	dateStamp = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
	os.system('zip -r ' + IONWC_HOME + '/archives/data-' + dateStamp + '.zip ' + IONWC_HOME + '/data/ ')

def run_all():
	dataStreamBC = DataStreamBC()
	#dataStreamBC.retrieveLicences()
	#dataStreamBC.retrieveSpuds()
	dataStreamBC.retrieveLandPostings()
	#dataStreamBC.retrieveFacilities()

	dataStreamAB = DataStreamAB()
	dataStreamAB.retrieveSpuds()
	dataStreamAB.retrieveLicences()
	dataStreamAB.retrieveLandPostings()
	#dataStreamAB.retrieveFacilities()

	dataStreamSK = DataStreamSK()
	dataStreamSK.retrieveSpuds()
	dataStreamSK.retrieveLicences()
	dataStreamSK.convertLandPostings()
	#dataStreamSK.retrieveFacilities()

	dataStreamMB = DataStreamMB()
	dataStreamMB.retrieveSpuds()
	dataStreamMB.retrieveLicences()
	dataStreamMB.retrieveLandPostings()

	createArchive()