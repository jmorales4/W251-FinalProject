# mongoDB queries of the similarity DB
# SYWang 4-29-2015

import pymongo
from pymongo import MongoClient

from bson.son import SON

client=MongoClient()
db=client.celebritywatch2
collection=db.faces

# simple query to find similar faces to JK Rowling
for face in db.faces.find( { "$and": [ {"celebrity": "JK_Rowling"}, {"similarity": { "$lt" : 0.10 } } ] }).sort("similarity", 1):
    # list peer name and similarity score
    
   print face['peer'],face['similarity']
    
# group by celebrity and calculate the average similarity per celebrity

for face in db.faces.aggregate(
                   [ 
                    { "$group" : {
                                  "_id": "$celebrity",
                                  "avgSimilarity": { "$avg": "$similarity" }
                                  }
                     }
                    ]
                    ):
                        print face["_id"], face["avgSimilarity"]
                    
                    
for face in db.faces.aggregate(
                   [
                    { "$match" : { 
                                  "celebrity": "JK_Rowling" 
                                  }
                     },
                    { "$match" : {
                                  "similarity": { "$lt" : 0.05 }
                                  }
                     },
                    { "$match" : {
                                  "similarity": { "$gt" : 0.0 }
                                  }
                     },
                    { "$sort" : { "simlarity": 1 } 
                     }
                    ]
                   ):
    print face["peer"], face["similarity"], face["image location"]
    

for face in db.faces.aggregate(
                   [
                    { "$match" : { 
                                  "celebrity": "Elizabeth_Taylor" 
                                  }
                     },
                    { "$match" : {
                                  "peer": "JK_Rowling"
                                  }
                     },
                    ]
                   ):
    print face

# build the same transformation as a pipeline

pipeline = [
            { "$match" : { 
                                  "celebrity": "JK_Rowling" 
                                  }
                     },
            { "$match" : {
                                  "similarity": { "$lt" : 0.13 }
                                  }
                     },
            { "$sort" : SON([( "simlarity" , 1 )]) }
            ]


pipeline_sort = [
            { "$group" : 
             {                  
                "_id": { "celebrity": "celebrity", "peer": "peer" },
                "similarity": { "similarity": "similarity" }
                                  }
                     },
            { "$sort" : { "similarity" , 1 } },
            { "$group" :
             {
                "_id": "$_id.celebrity",
                "mostSimilar": { "$last": "$_id.peer" },
                "smallestSimilarity": { "$last": "$_id.similarity" },
                "leastSimilar": { "$first": "$_id.peer" },
                "largestSimilarity": { "$first": "$_id.similarity" }
                }
             }
            ]

# see results
# list(db.faces.aggregate(pipeline))

# see most similar and least similar
# list(db.faces.aggregate(pipeline_sort))

# try sort on query without an index for similarity
# error
# db.faces.find({ "celebrity" "JK_Rowling" }).sort(SON([{ "similarity": 1 }]))

# for face in taylor.limit(10):
    # face.aggregate(
                 #  [
                 #   { "$sort" : { "similarity" : -1 } }
                  #  ]
                 #  )
    
    # print face['peer'],face['similarity'], face['image location']
