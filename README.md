# MarkLogic Slow Queries

* Using the MarkLogic API, identify queries that take longer than x seconds to perform.
	- Write the results to a local standalone instance of mongoDB  { ml-slowquery-api.py }
* Sanitise the data by deduplicating request-ids that appear more than once. { mongo-dedup-sq.js }
* Chart the results using matplotlib & mpld3  { slowquery-charts.py }
