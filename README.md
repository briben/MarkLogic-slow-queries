# MarkLogic Slow Queries

* Using the MarkLogic API, identify queries that take longer than x seconds to perform.
* Write the results to a local standalone instance of mongoDB  _[ml-slowquery-api.py]_
* Sanitise the data by deduplicating request-ids that appear more than once. _[mongo-dedup-sq.js]_
* Chart the results using matplotlib & mpld3  _[slowquery-charts.py]_

## Create a tunnel for to MarkLogic ports 8000,8001,8002
This script currently connects to the API on localhost:8002 via SSH Tunnel, so first create a tunnel:
```sh
ssh -L 8000:xstore153:8000 -L 8001:xstore153:8001 -L 8002:xstore153:8002 Access
```

## Run the MarkLogic slow query check
Run the slow query check (`ml-slowquery-api.py`) on a loop for desired time period.
```sh
while true; do sudo python ml-slowquery-api.py; sleep 5; done
```


## Remove any duplicate queries from the mongoDB database
As the query check can be running for a while, it can record the same query more than once at different intervals. 
To remove these duplicates, execute the following javaScript on the slow query mongodb database.
1. Using an app such as Robo 3T, connect to the mongoDB on localhost:27017
2. Paste the contents of `mongo-dedup-sq.js` into the query field
3. Execute the query