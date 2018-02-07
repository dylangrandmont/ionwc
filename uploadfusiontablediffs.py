#!/usr/bin/python

# Copyright (C) 2016-2018, Dylan Grandmont

import urllib2
import urllib
import simplejson
import sys
import httplib
import os

IONWC_HOME = os.environ["IONWC_HOME"]

client_id = "595289711288-9b4087cj95fuuqa7ggk8b7vfia084b9r.apps.googleusercontent.com"
client_secret = "5-LF80C6e0F7oheknMIkYX5f"
redirect_uri = "http://ionwc.com"
api_key = "AIzaSyB3Z7U6oXminsygGJOvdkvtn18NmrLs7Ws"

licence_table_id  = "1c5dt503OlbDr5-nRRP-xsotq3cTuJeBx3p5K_Ri7"
spud_table_id = "1lc9vWq_M45gnsL5VLLNsLKBPlPQ2LgCOWxt_kUHI"
postings_table_id = '1kEPGipJ6rVtYNDcj96g7sGwzCvdxlY2WyU1cHY-L'
postings_results_table_id = '1jCuFLgiI-K7ftnl7OGewbeQ2yLkNuRKOWgYckHp3'
postings_aggregate_table_id = '1HUapBmqcSP_Dkz1OA_L1LAv7flecCkVeK8gQrJnV'
postings_results_aggregate_table_id = '1n_vrhZ_gRfyv_Zg-lNBdeRfmQq62CNUgG8crWdGn'

class FusionTable:
    def __init__(self):
        self.access_token = ""
        self.params = ""

    def get_tokens(self):
        print "copy and paste the url below into browser address bar and hit enter"
        website = "https://accounts.google.com/o/oauth2/auth?%s%s%s%s" % \
            ("client_id=%s&" % (client_id),
            "redirect_uri=%s&" % (redirect_uri),
            "scope=https://www.googleapis.com/auth/fusiontables&",
            "response_type=code")
        os.system("firefox --new-window \"" + website + "\"")
        print website

        code = raw_input("Enter code (parameter of URL): ")
        data = urllib.urlencode({
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        })

        serv_req = urllib2.Request(url="https://accounts.google.com/o/oauth2/token",
           data=data)

        serv_resp = urllib2.urlopen(serv_req)
        response = serv_resp.read()
        tokens = simplejson.loads(response)
        access_token = tokens["access_token"]
        self.access_token = access_token
        self.params = "?key=%s&access_token=%s" % \
            (api_key, self.access_token)

    def _import_row(self, data, tableId):
        print "IMPORT ROW", data
        self.run_request(
            "POST",
            "/upload/fusiontables/v2/tables/%s/import%s" % (tableId, self.params),
            data,
            headers={'Content-Type':'application/octet-stream'}) 

    def _import_row_colon_delimiter(self, data, tableId):
        print "IMPORT ROW", data
        self.run_request(
            "POST",
            "/upload/fusiontables/v2/tables/%s/import%s%s" % (tableId, self.params, '&delimiter=%3A'),
            data,
            headers={'Content-Type':'application/octet-stream'})


    def run_request(self, method, url, data=None, headers=None):
        request = httplib.HTTPSConnection("www.googleapis.com")

        if data and headers:
           request.request(method, url, data, headers)
        else:
           request.request(method, url)

        response = request.getresponse()
        print response.status, response.reason
        response = response.read()
        print response
        return response

    def import_row_from_diff(self, diffLines, tableId, dataType):
        if len(diffLines) == 0:
            print "WARN:  No difference found between submitted and current + " + dataType + " files, importing zero rows"  
            return

        print "INFO:  Importing " + str(len(diffLines)) + " rows of " + dataType

        data = ""
        for line in diffLines:
            data += line
        self._import_row(data, tableId)

    def import_row_from_diff_colon_delimited(self, diffLines, tableId, dataType):
        if len(diffLines) == 0:
            print "WARN:  No difference found between submitted and current + " + dataType + " files, importing zero rows"  
            return

        print "INFO:  Importing " + str(len(diffLines)) + " rows of " + dataType
        data = ""
        for diffLine in diffLines:
            data += diffLine
        self._import_row_colon_delimiter(data, tableId)


if __name__ == "__main__":
    licences_diff_file = open(IONWC_HOME + "/dbs/diff_licenceDBAll.csv")
    licence_diff_lines = licences_diff_file.readlines()

    spud_diff_file = open(IONWC_HOME + "/dbs/AUGlicdb_diff.csv")
    spud_diff_lines = spud_diff_file.readlines()

    postings_diff_file = open(IONWC_HOME + "/dbs/diff_PostingsDataBase.csv")
    postings_diff_lines = postings_diff_file.readlines()

    results_diff_file = open(IONWC_HOME + "/dbs/diff_PostingsResultsDataBase.csv")
    results_diff_lines = results_diff_file.readlines()

    posting_aggregate_diff_file = open(IONWC_HOME + "/dbs/diff_PostingsAggregateDataBase.csv")
    posting_aggregate_diff_lines = posting_aggregate_diff_file.readlines()
    
    results_aggregate_diff_file = open(IONWC_HOME + "/dbs/diff_PostingsAggregateResultsDataBase.csv")
    results_aggregate_diff_lines = results_aggregate_diff_file.readlines()

    if len(licence_diff_lines) > 0 or len(spud_diff_lines) > 0 or len(postings_diff_lines) > 0 or len(results_diff_lines) > 0:
        fusion_table = FusionTable()
        fusion_table.get_tokens()

        fusion_table.import_row_from_diff(licence_diff_lines, licence_table_id, "well licences")

        fusion_table.import_row_from_diff(spud_diff_lines, spud_table_id, "well spuds")

        fusion_table.import_row_from_diff_colon_delimited(postings_diff_lines, postings_table_id, "land postings")

        fusion_table.import_row_from_diff_colon_delimited(results_diff_lines, postings_results_table_id, "land posting results")

        fusion_table.import_row_from_diff_colon_delimited(posting_aggregate_diff_lines, postings_aggregate_table_id, "aggregate land postings")

        fusion_table.import_row_from_diff_colon_delimited(results_aggregate_diff_lines, postings_results_aggregate_table_id, "aggregate land posting results")
