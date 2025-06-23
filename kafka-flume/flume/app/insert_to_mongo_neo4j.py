import sys
import json
from pymongo import MongoClient
from neo4j import GraphDatabase

# Read configuration file
with open('kafka-flume/flume/app/config.json') as file:
    config = json.load(file)

# MongoDB connection
mongo_client = MongoClient(config["mongo_uri"])
mongo_db = mongo_client[config["mongo_db"]]
mongo_collection = mongo_db[config["mongo_collection"]]


# Neo4j connection
driver = GraphDatabase.driver(config["neo4j_uri"], auth=(config["neo4j_user"], config["neo4j_pass"]))

def insert_to_neo4j(data):
    with driver.session() as session:
        session.run(
            "CREATE (n:Sensor {type: $type, value: $value})",
            type=data.get("type"),
            value=data.get("value")
        )

def insert_to_mongo(data):
    mongo_collection.insert_one(data)

try:
    input_data = sys.stdin.read().strip()
    doc = json.loads(input_data)

    docs = doc if isinstance(doc, list) else [doc]

    for d in docs:
        dtype = d.get("type", "").lower()
        if dtype.startswith("temp") or dtype == "":
            insert_to_mongo(d)
            print("Inserted to MongoDB:", d)
        elif dtype.startswith("pressure"):
            insert_to_neo4j(d)
            print("Inserted to Neo4j:", d)
        else:
            insert_to_mongo(d)
            print("Inserted to MongoDB (unknown type):", d)
except Exception as e:
    print("Error:", e, file=sys.stderr)
