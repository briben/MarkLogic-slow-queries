# MarkLogic Slow Queries

* Using the MarkLogic API, identify queries that take longer than x seconds to perform.
	- Write the results to a local standalone instance of mongoDB  _[ml-slowquery-api.py]_
* Sanitise the data by deduplicating request-ids that appear more than once. _[mongo-dedup-sq.js]_
* Chart the results using matplotlib & mpld3  _[slowquery-charts.py]_
