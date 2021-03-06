import sys, urllib, urllib2, json, pymongo, base64, requests, os
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from threading import Timer
from bs4 import BeautifulSoup
from io import open
from pymongo import MongoClient # Database connector

NO_PROXY = {
    'no': 'pass',
}

username = 'admin'
#password = 'password'
password = 'xxxxxxxx'

# Test/Stage API
url = "http://localhost:8002/manage/LATEST/requests?format=json&seconds-min=3&fullrefs=true"

# Live API
#url = "http://localhost:8002/manage/LATEST/requests?format=json&seconds-min=3&fullrefs=true"

response = requests.get(url, auth=HTTPDigestAuth(username, password), cert=('/etc/ssl/certs/marklogic.pem','/etc/ssl/certs/marklogic.key'), proxies=NO_PROXY)

data = response.json()

#Configure the connection to the database
client = MongoClient('localhost', 27017)    #Select the db host and port
db = client.dst    #Select the database
col = db.slowQueries   #Select the collection


dataItems = data['request-default-list']['list-items']

value = dataItems.get('list-item', "empty")

if (value == 'empty'):
	print '\n'
	print "No list-items"

else:
	dataItemList = dataItems['list-item']

	res = {}
	

	for props in dataItemList :
		req_id = props['idref']

		# Used with '&fullrefs=true'
		host = props['relation'][0]['nameref']
		ml_server = props['relation'][1]['nameref']
		ml_db = props['relation'][2]['nameref']
		t_id = props['relation'][3]['idref']

		rt = props['item-properties']['request-text']
		secs = props['item-properties']['seconds-elapsed']['value']
		sTime = props['item-properties']['start-time']['value']
		maxTimeLimit = props['item-properties']['max-time-limit']['value']
		timeLimit = props['item-properties']['time-limit']['value']
		exTreeHits = props['item-properties']['expanded-tree-cache-hits']['value']
		exTreeMiss = props['item-properties']['expanded-tree-cache-misses']['value']
		print '\n'
		print 'Query Inserted'
		print 'Query Duration (s): ' + str(secs)
		print 'Start Time: ' + sTime
		
		
		# Add the values to a dictionary
		req_doc = {'host':host, 'request-id': req_id,'transaction_id': t_id, 'app-server': ml_server, 'database': ml_db, 'request-text': rt, 'query-duration': secs, 'start-time': sTime,'expanded-tree-cache-hits':exTreeHits,'expanded-tree-cache-misses':exTreeMiss,'max-time-limit':maxTimeLimit,'time-limit':timeLimit}

		# We don't want the default record returned in every ML json request, so strip those out!
		if (ml_db != 'App-Services'):
			# Insert into mongoDB
			col.insert(req_doc)




#def myLoop():
	# Code here

#t = Timer(10.0, myLoop) # Run every 10 secs.
#t.start()
