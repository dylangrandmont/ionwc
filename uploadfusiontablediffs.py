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

licTableId  = "1c5dt503OlbDr5-nRRP-xsotq3cTuJeBx3p5K_Ri7"
spudTableId = "1lc9vWq_M45gnsL5VLLNsLKBPlPQ2LgCOWxt_kUHI"
postTableId = '1kEPGipJ6rVtYNDcj96g7sGwzCvdxlY2WyU1cHY-L'
postResultsTableId = '1jCuFLgiI-K7ftnl7OGewbeQ2yLkNuRKOWgYckHp3'
postAggregateTableId = '1HUapBmqcSP_Dkz1OA_L1LAv7flecCkVeK8gQrJnV'
postResultsAggregateTableId = '1n_vrhZ_gRfyv_Zg-lNBdeRfmQq62CNUgG8crWdGn'

class RunAPITest:
  def __init__(self):
    self.access_token = ""
    self.params = ""

  def main(self):
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

  def importRow(self, data, tableId):
    print "IMPORT ROW", data
    self.runRequest(
      "POST",
      "/upload/fusiontables/v2/tables/%s/import%s" % (tableId, self.params),
      data,
      headers={'Content-Type':'application/octet-stream'}) 

  def importRowColonDelimiter(self, data, tableId):
    print "IMPORT ROW", data
    self.runRequest(
      "POST",
      "/upload/fusiontables/v2/tables/%s/import%s%s" % (tableId, self.params, '&delimiter=%3A'),
      data,
      headers={'Content-Type':'application/octet-stream'})


  def runRequest(self, method, url, data=None, headers=None):
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

def _importDiffRows(diffLines, tableId, dataType):

  if len(diffLines) == 0:
    print "WARN:  No difference found between submitted and current + " + dataType + " files, importing zero rows"  
    return

  print "INFO:  Importing " + str(len(diffLines)) + " rows of " + dataType

  data = ""
  for line in diffLines:
    data += line
  api_test.importRow(data, tableId)
  return


def _importDiffRowsColonDelimiter(diffLines, tableId, dataType):

  if len(diffLines) == 0:
    print "WARN:  No difference found between submitted and current + " + dataType + " files, importing zero rows"  
    return

  print "INFO:  Importing " + str(len(diffLines)) + " rows of " + dataType
  data = ""
  for diffLine in diffLines:
    data += diffLine
  api_test.importRowColonDelimiter(data, tableId)


if __name__ == "__main__":
  licDiffFile = open(IONWC_HOME + "/dbs/diff_licenceDBAll.csv")
  licDiffLines = licDiffFile.readlines()

  spudDiffFile = open(IONWC_HOME + "/dbs/AUGlicdb_diff.csv")
  spudDiffLines = spudDiffFile.readlines()

  postDiffFile = open(IONWC_HOME + "/dbs/diff_PostingsDataBase.csv")
  postDiffLines = postDiffFile.readlines()

  postResultsDiffFile = open(IONWC_HOME + "/dbs/diff_PostingsResultsDataBase.csv")
  postResultsDiffLines = postResultsDiffFile.readlines()

  postAggregateDiffFile = open(IONWC_HOME + "/dbs/diff_PostingsAggregateDataBase.csv")
  postAggregateDiffLines = postAggregateDiffFile.readlines()
  
  postAggregateResultsDiffFile = open(IONWC_HOME + "/dbs/diff_PostingsAggregateResultsDataBase.csv")
  postAggregateResultsDiffLines = postAggregateResultsDiffFile.readlines()

  if len(licDiffLines)>0 or len(spudDiffLines)>0 or len(postDiffLines)>0 or len(postResultsDiffLines)>0:
    api_test = RunAPITest()
    api_test.main()

    _importDiffRows(licDiffLines, licTableId, "well licences")

    _importDiffRows(spudDiffLines, spudTableId, "well spuds")

    _importDiffRowsColonDelimiter(postDiffLines, postTableId, "land postings")

    _importDiffRowsColonDelimiter(postResultsDiffLines, postResultsTableId, "land posting results")

    _importDiffRowsColonDelimiter(postAggregateDiffLines, postAggregateTableId, "aggregate land postings")

    _importDiffRowsColonDelimiter(postAggregateResultsDiffLines, postResultsAggregateTableId, "aggregate land posting results")
