# get directory content
from os import listdir
from os.path import isfile, join

mypath = "C:\\Users\\Adrian\\sciebo\\Masterarbeit\\Korpus\\altafsir\\"
fileslisting = [f for f in listdir(mypath) if isfile(join(mypath, f))]


# load directory content into list
import json

samples = []

for i in fileslisting:
    with open(mypath + i, encoding="utf8") as f:
        samples.append(set(json.load(f)["text"]))