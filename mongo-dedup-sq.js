db.slowQueries.aggregate([  
    {$group: { 
        _id: {requestID: "$request-id"},
        uniqueIds: {$addToSet: "$_id"},
        duration: {$addToSet: "$query-duration"},
        count: {$sum: 1}
        } 
    },
    {$match: { 
        count: {"$gt": 1}
        }
    },
    {$sort: {
        duration: -1
        }
    }
]).forEach(function(doc) {
   doc.uniqueIds.shift();
   db.slowQueries.remove({
       _id: {$in: doc.uniqueIds}
   });
})