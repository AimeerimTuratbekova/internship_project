import sys
import json
from pymongo import MongoClient
import os 

f = open("/app/myfile.txt", "a")

for line in sys.stdin:
    f.write(line)