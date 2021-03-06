# ionwc

Eye on Western Canada Code Package README
Author: Dylan Grandmont, (C) 2016-2018


# Introduction

Eye on Western Canada (IONWC) has three components: 
* Web client: web-based mapping platform hosted at http://ionwc.com/map.
See https://github.com/dylangrandmont/ionwc-client
* Database Parser: collection of code to download, update, and parse data for mapping.
See https://github.com/dylangrandmont/ionwc
* Google Account: hosts Fusion Tables, which act as the database which is read by (1). The account name is ionwestcan@gmail.com

This folder contains the Database Parser component. It generally works as follows:
* Data is downloaded from online government sources
* Data is parsed into consistent formats and placed in database files (csv files)
* The databases are uploaded and stored in Google Fusion Tables
* Finally, http://ionwc.com reads these Fusion tables and plots them in dynamic maps and charts

These steps are automated as much as possible, this README details the manual steps involved

# Getting Started

## System Requirements

This code package was developed on Ubuntu operating system but will work on most Linux distributions

Depedencies: 
* Python 2.7
* wget

## Setting Environment Variables

One environment variable, 'IONWC_HOME', must be set.
This variable is the directory location of this folder (i.e. this directory must sit in $IONWC_HOME/scripts)

## Package Contents

IONWC_HOME/data
* Raw data (txt, pdf, etc.) as downloaded from online government sources
IONWC_HOME/dbs
* Final databases (csv files) of all data
IONWC_HOME/scripts
* All code for updating databases

## Running the Package

To perform updates and run this package, simply type

			python run.py
into your command line. This will update all raw data, determine any new additions, and 
then send those additions to the Fusion Tables Database.
You will be prompted with login credentials in order to update the Fusion Tables Database.


# Information for Developers

## Running Unit Tests

To run the full suite, execute

```
python -m unittest discover
```


# Manual Maintainence

## SK Land Postings
The URLs for Land Postings and Results are not organized in a predictable manner.
Because of this, they must be chcked and downloaded manually

## Data Retrieval Dates
URLs used in data retrieval require an input of the year.
Currently, these are string constants.
Improvements should be made to grab the current year, next year, etc. instead of using constants.

## Constants.py
BC_POSTING_DATES_TO_SALE_DATE_MAP
SK_POSTING_NUMBER_TO_SALE_DATE

# Data Sources

## Well Licences
* BC: https://reports.bcogc.ca/ogc/f?p=AMS_REPORTS:WA_ISSUED:16572487065452:
* AB: http://www.aer.ca/data/well-lic/WELLS
* SK: http://www.economy.gov.sk.ca/Files/oilandgas/wellbullfile/archives/
* MB: http://www.manitoba.ca/iem/petroleum/wwar/index.html

## Drilling
* BC: https://iris.bcogc.ca/reports/rwservlet?prd_ogcr9985
* AB: http://www.aer.ca/data/WELLS/
* SK: http://www.economy.gov.sk.ca/Archived-Drilling-Activity-Reports
* MB: http://www.manitoba.ca/iem/petroleum/wwar/index.html

## Land Postings (Offerings)
* BC: http://www2.gov.bc.ca/gov/content/industry/natural-gas-oil/petroleum-natural-gas-tenure
* AB: http://www.energy.alberta.ca/Tenure/607.asp
* SK: http://www.saskatchewan.ca/business/agriculture-natural-resources-and-industry/oil-and-gas/crown-land-sales-dispositions-and-tenure/public-offerings/schedule-of-crown-land-sales
* MB: http://www.gov.mb.ca/iem/petroleum/landinfo/landsale.html

## Land Postings (Results)
* BC: http://www2.gov.bc.ca/gov/content/industry/natural-gas-oil/petroleum-natural-gas-tenure/sales-results-statistics/2016-sale-results
* AB: http://www.energy.alberta.ca/Tenure/607.asp
* SK: http://www.saskatchewan.ca/business/agriculture-natural-resources-and-industry/oil-and-gas/crown-land-sales-dispositions-and-tenure/public-offerings/schedule-of-crown-land-sales
* MB: http://www.gov.mb.ca/iem/petroleum/landinfo/landsale.html

## All Wells
* MB: http://www.gov.mb.ca/iem/petroleum/reports/uwi_weekly.xls

## Facilities
* BC: https://ams-reports.bcogc.ca/ords-prod/f?p=200:58:15168409196395:CSV::::
* AB: http://www.aer.ca/data/codes/ActiveFacility.txt
* SK: http://economy.gov.sk.ca/files/Registry%20Downloads/NewAndActiveFacilitiesReport.csv
* MB: Unavailable?

## Formations
https://landman.ca/pdf/CORELAB.pdf

# Copyright Notice
This README and the entire contents of this directory are copyright of Dylan Grandmont, 2016-2018.
