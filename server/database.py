
# from flask import Flask

# from flask_pymongo import PyMongo

# app = Flask(__name__)

# app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
# mongo = PyMongo(app)


# def add_to_db(results):

#     all_locations = []
#     print(results[7])
#     # Iterate through the results and append the places to the list
#     for place in results[7]:
#         location_data = {
#             "address": place[0],
#             "latitude": place[1][0],
#             "longitude": place[1][1]
#         }
#         all_locations.append(location_data)

#     # Insert the entire list of locations as a single document in the "locations" collection
#     mongo.db.Adds.insert_one(
#         {"locations": all_locations, "catogory": results[4], "Price": results[5], "contacts": results[6]})
