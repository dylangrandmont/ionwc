# ionwc

Eye on Western Canada Code Package README
Author: Dylan Grandmont, (C) 2016-2018

Table of Contents
	0. Introduction
	1. Getting Started 
		1A. System Requirements
		1B. Setting Environment Variables
		1C. Package Contents
		1D. Running the Package
	2. Required Maintenance
	3. Data Sources
	4. Known Issues / Improvements
	5. Copyright Notice

0. IntroductionretrieveLandPostings

	Eye on Western Canada (IONWC) has three components: 
		(1) WEBSITE: web-based mapping platform hosted at http://ionwc.com
		(2) SERVER CODE: collection of code to download, update, and parse data for mapping.
		(3) GOOGLE ACCOUNT: account hosts Fusion Tables, which act as the database which
			is read by (1). The account name is ionwestcan@gmail.com

	This folder contains component (2). It generally works as follows:

	 - Data is downloaded from online government sources
	 - Data is parsed into consistent formats and placed in database files (csv files)
	 - The databases are uploaded and stored in Google Fusion Tables
	 - Finally, http://ionwc.com reads these Fusion tables and plots them in dynamic maps and 
	 charts

	These steps are automated as much as possible, this README details the manual steps involved

1. Getting Started

	1A. System Requirements

		This code package was developed on Ubuntu operating system but will work on most Linux distributions

		Depedencies: 
			Python 2.7
			wget

	1B. Setting Environment Variables

		ONE environment variable, 'IONWC_HOME', must be set. This variable is the directory location 
		of this folder (i.e. this directory must sit in $IONWC_HOME/scripts)

	1C. Package Contents

		IONWC_HOME/data
			Raw data (txt, pdf, etc.) as downloaded from online government sources
		IONWC_HOME/dbs
			Final databases (csv files) of all data
		IONWC_HOME/scripts
			All code for updating databases

	1D. Running the Package

		To perform updates and run this package, simply type

			python run.py

		into your command line. This will update all raw data, determine any new additions, and 
		then send those additions to the Fusion Tables Database. You will be prompted with login
		credentials in order to update the Fusion Tables Database.

2. Manual Maintainence

	SK Land Postings
		The URLs for Land Postings and Results are not organized in a predictable manner.
		Because of this, they must be chcked and downloaded manually

	Data Retrieval Dates
		URLs used in data retrieval require an input of the year. Currently, these are string constants.
		Improvements should be made to grab the current year, next year, etc. instead of using constants.

		Constants.py
			BCPostingDatesToSaleDateMap
			SKPostingNumberToSaleDate

3. Data Sources

	Well Licences
		BC: 
		AB: http://www.aer.ca/data/well-lic/WELLS
		SK: http://www.economy.gov.sk.ca/Files/oilandgas/wellbullfile/archives/
		MB:

	Drilling
		BC:
		AB: http://www.aer.ca/data/WELLS/
		SK: http://www.economy.gov.sk.ca/Archived-Drilling-Activity-Reports
		MB:

	Land Postings (Offerings)
		BC: http://www2.gov.bc.ca/gov/content/industry/natural-gas-oil/petroleum-natural-gas-tenure
		AB: http://www.energy.alberta.ca/Tenure/607.asp
		SK: http://www.saskatchewan.ca/business/agriculture-natural-resources-and-industry/oil-and-gas/crown-land-sales-dispositions-and-tenure/public-offerings/schedule-of-crown-land-sales
		MB: http://www.gov.mb.ca/iem/petroleum/landinfo/landsale.html

	Land Postings (Results)
		BC: http://www2.gov.bc.ca/gov/content/industry/natural-gas-oil/petroleum-natural-gas-tenure/sales-results-statistics/2016-sale-results
		AB: http://www.energy.alberta.ca/Tenure/607.asp
		SK: http://www.saskatchewan.ca/business/agriculture-natural-resources-and-industry/oil-and-gas/crown-land-sales-dispositions-and-tenure/public-offerings/schedule-of-crown-land-sales
		MB: http://www.gov.mb.ca/iem/petroleum/landinfo/landsale.html

	All Wells
		MB: http://www.gov.mb.ca/iem/petroleum/reports/uwi_weekly.xls

	Facilities
		BC: https://ams-reports.bcogc.ca/ords-prod/f?p=200:58:15168409196395:CSV::::
		AB: http://www.aer.ca/data/codes/ActiveFacility.txt
		SK: http://economy.gov.sk.ca/files/Registry%20Downloads/NewAndActiveFacilitiesReport.csv
		MB: 

	Formations
		

4. Known Issues / Improvements / Technical Debt
	Remove dependencies on wget, replace with python libraries
	Automate SK posting retrieval

5. Copyright Notice

	This README and the entire contents of this directory are copyright of Dylan Grandmont, 2016.
