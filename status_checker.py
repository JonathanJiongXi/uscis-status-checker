#!/usr/bin/python

import sys
import urllib
import urllib2

sys.path.append('/Users/jiongxi/Documents/Code/UscisStatusChecker/beautifulsoup4-4.4.0')
from bs4 import BeautifulSoup

REQUEST_PARAMS = {}
REQUEST_PARAMS['completedActionsCurrentPage'] = '0'
REQUEST_PARAMS['upcomingActionsCurrentPage'] = '0'
REQUEST_PARAMS['caseStatusSearchBtn'] = 'CHECK+STATUS'
REQUEST_URL = 'https://egov.uscis.gov/casestatus/mycasestatus.do'
DEFAULT_RECEIPT_NUMBER_PREFIX = 'LIN'
DEFAULT_RECEIPT_NUMBER_START = '1591229800'
DEFAULT_RECEIPT_NUMBER_END = '1591229900'
RESULT_DIC_TITLE = 'title'
RESULT_DIC_DETAILS = 'details'
RESULT_DIC_DATE = 'date'
RESULT_DIC_RECEIPT_NUMBER = 'receipt-number'

def QueryServer(receipt_number):
  params = REQUEST_PARAMS
  params['appReceiptNum'] = receipt_number
  params_encoded =  urllib.urlencode(params)
  headers={'User-agent' : 'Mozilla/5.0'}
  req = urllib2.Request(REQUEST_URL, params_encoded, headers)
  f = urllib2.urlopen(req)
  response = f.read()
  f.close()
  return response

def ParseResponse(response, receipt_number):
  soup = BeautifulSoup(response, 'html.parser')
  div = soup.find('div', {'class' : 'rows text-center'})
  result = ParseStatusDiv(div, receipt_number)
  return result

def ParseStatusDiv(status_div, receipt_number):
  result = {}
  result[RESULT_DIC_TITLE] = str(status_div.h1.contents[0])
  result[RESULT_DIC_DETAILS] = str(status_div.p.contents[0])
  result[RESULT_DIC_RECEIPT_NUMBER] = receipt_number
  return result;

def PrintResults(results):
  for result in results:
    print '%s: %s' % (result[RESULT_DIC_RECEIPT_NUMBER], result[RESULT_DIC_TITLE])

def main(argv=None):
  if argv is None:
    argv = sys.argv
  if len(argv) > 1:
    receipt_number_start = argv[1]
  else:
    receipt_number_start = DEFAULT_RECEIPT_NUMBER_START
  if len(argv) > 2:
    receipt_number_end = argv[2]
  else:
    receipt_number_end = DEFAULT_RECEIPT_NUMBER_END
  results = []
  for num in range(int(receipt_number_start), int(receipt_number_end)):
    receipt_number = DEFAULT_RECEIPT_NUMBER_PREFIX + str(num)
    response = QueryServer(receipt_number)
    parsed_response = ParseResponse(response, receipt_number)
    results.append(parsed_response)
  PrintResults(results)

if __name__=="__main__":
  main()
