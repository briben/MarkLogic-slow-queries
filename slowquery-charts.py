import pymongo, pprint, json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import mpld3
from mpld3 import plugins

from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from collections import OrderedDict
from pymongo import MongoClient

#mpld3 hack
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        import numpy as np
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
from mpld3 import _display
_display.NumpyEncoder = NumpyEncoder

plasma = cm.get_cmap('plasma', 12)


#Configure the connection to the database
client = MongoClient('localhost', 27017)    #Select the Dev host and port
db = client.dst    #Select the database
sq = db.slowQueries   #Select the collection

duration = []
timestamp = []

for query in sq.find({}):
	# print(query['query-duration'])
	# print(query['start-time'])
	dur = query['query-duration']
	durTwoPlaces = round(dur, 2)
	duration.append(durTwoPlaces)
	timestamp.append(query['start-time'])

fig, ax = plt.subplots(subplot_kw=dict(facecolor='#f2f6fc'))

for i in [duration]:
    x = timestamp
    y = duration
    scatter = ax.scatter(x, y, c=i, alpha=0.5, edgecolors='none', cmap=plt.cm.jet, label=l)
 

ax.grid(color='white', linestyle='solid')
ax.set_title("MarkLogic Slow Queries", size=20)
ax.set_xlabel('Timestamp', fontsize=12, fontdict={'family': 'monospace'}, labelpad=5)
ax.set_ylabel('Query Duration (secs)', fontsize=12, fontdict={'family': 'monospace'}, labelpad=10)


tooltip = mpld3.plugins.PointLabelTooltip(scatter)
mpld3.plugins.connect(fig, tooltip)

mpld3.display()

#plt.show()