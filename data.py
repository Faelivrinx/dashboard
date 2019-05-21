import os
import utility as util
import codecs

# get Ngram Flat Map form raw text file like a book or smth  :) all ngrams raw one after another not Count'ed
def getNgramFlatMap(ngramType, rawData):
    if ngramType == "monograms":
        return util.flatten_array([util.zip_ngrams(w, 1) for w in util.clear_text(rawData).split() if len(w) >= 1])
    elif ngramType == "bigrams":
        return util.flatten_array([util.zip_ngrams(w, 2) for w in util.clear_text(rawData).split() if len(w) >= 2])
    else:
        return util.flatten_array([util.zip_ngrams(w, 3) for w in util.clear_text(rawData).split() if len(w) >= 3])

# get Ngram Flat Map from specially prepared files hehe
def getNgramCounter(data):
    ngramData = []
    for line in data.splitlines():
        ngramData.append(line.split())
    return ngramData

# load files to array from data folder
def loadInitialData():
    directory = "./data"
    languageMap = []
    for filename in os.listdir(directory):
        ngramType = filename[(filename.find("_")+1):filename.find(".txt")]
        data = codecs.open(directory + "/" + filename, 'r', encoding="utf8").read()
        result = {
            "language": filename[:filename.find("_")],
            "ngramType": ngramType,
            "data": getNgramCounter(data),
            "totalDataCount": sumNgrams(getNgramCounter(data))
        }
        languageMap.append(result)
    return languageMap

def sumNgrams(data):
    sum = 0
    for item in data:
        sum += int(item[1])
    return sum

def getMonogramData(languageMap):
    return [language for language in languageMap if language["ngramType"] == "monograms"]

def getBigramData(languageMap):
    return [language for language in languageMap if language["ngramType"] == "bigrams"]

# create language names for select
def createLanguageKeysSet(languageMap):
    return set([language["language"] for language in languageMap])