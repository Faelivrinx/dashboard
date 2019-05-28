import os
import utility as util
import codecs
import json
from math import log

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

#get letters from json file
def getJsonLetters(json_data):
    return [[key.upper(), value] for key, value in json_data['letters'].items()]

def getJsonDigrams(json_data):
    return [[key.upper(), value] for key, value in json_data['digrams'].items()]

def getJsonTrigrams(json_data):
    return [[key.upper(), value] for key, value in json_data['trigrams'].items()]

def getMonogramsFromJson(filename, json_data):
    letters = getJsonLetters(json_data)
    return {
        "language": filename[:filename.find(".")],
        "ngramType": 'monograms',
        "data": letters,
        "totalDataCount": sumNgrams(letters)
    }

def getDigramsFromJson(filename, json_data):
    digrams = getJsonDigrams(json_data)
    return {
        "language": filename[:filename.find(".")],
        "ngramType": 'bigrams',
        "data": digrams,
        "totalDataCount": sumNgrams(digrams)
    }

def getTrigramsFromJson(filename, json_data):
    trigrams = getJsonTrigrams(json_data)
    return {
        "language": filename[:filename.find(".")],
        "ngramType": 'trigrams',
        "data": trigrams,
        "totalDataCount": sumNgrams(trigrams)
    }

def sortData(result):
    result["data"].sort(key=lambda x: float(x[1]), reverse=True)
    return result

def saveInputToFile(data):
    monograms = getNgramFlatMap('monograms', data)
    digrams = getNgramFlatMap('bigrams', data)
    trigrams = getNgramFlatMap('trigrams', data)
    counter_monograms = Counter(monograms)
    counter_digrams = Counter(digrams)
    counter_trigrams = Counter(trigrams)
    letters = {str(count).upper(): str(counter_monograms[count]) for count in counter_monograms}
    digrams = {str(count).upper(): str(counter_digrams[count]) for count in counter_digrams}
    trigrams = {str(count).upper(): str(counter_trigrams[count]) for count in counter_trigrams}

    result = {
    'letters': letters,
    'digrams': digrams,
    'trigrams': trigrams
    }
    with open('./data/input.json', 'wb') as f:
        json.dump(result, codecs.getwriter('utf-8')(f), ensure_ascii=False)

# load files to array from data folder
def loadInitialData():
    directory = "./data"
    languageMap = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            data = codecs.open(directory + "/" + filename, 'r', encoding="utf8").read()
            json_data = json.loads(data)

            languageMap.append(sortData(getMonogramsFromJson(filename, json_data)))
            languageMap.append(sortData(getDigramsFromJson(filename, json_data)))
            languageMap.append(sortData(getTrigramsFromJson(filename, json_data)))
        else:
            ngramType = filename[(filename.find("_")+1):filename.find(".txt")]
            data = codecs.open(directory + "/" + filename, 'r', encoding="utf8").read()
            result = {
                "language": filename[:filename.find("_")],
                "ngramType": ngramType,
                "data": getNgramCounter(data),
                "totalDataCount": sumNgrams(getNgramCounter(data))
            }
            languageMap.append(sortData(result))
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

def getTrigramData(languageMap):
    return [language for language in languageMap if language["ngramType"] == "trigrams"]

# create language names for select
def createLanguageKeysSet(languageMap):
    return set([language["language"] for language in languageMap])

def findLanguageDataByKeyAndNgram(language, nGramType, languageMap):
    for langData in languageMap:
        if langData['language'] == language and langData['ngramType'] == nGramType:
            return langData

def changeToPercentValue(singleLangMap):
    for item in singleLangMap['data']:
        item[1] = float(item[1]) / singleLangMap['totalDataCount'] * 100
        item[1] = str(item[1])

def sortBySimilarity(languageMap, inputMaps):
    results = []
    for inputMap in inputMaps:
        for search in inputMap['data']:
            percent_search = float(search[1])/float(inputMap['totalDataCount']) * 100
            for single_lang in languageMap:
                sum_language = 0
                for ngram in single_lang['data']:
                    if ngram[0] == search[0]:
                        percent_ngram = float(ngram[1])/float(single_lang['totalDataCount'])*100
                        # print(single_lang['language']+ " similarity " + "ngram " + str(ngram[0]) + " with value" + str(percent_ngram))
                        sum_language += percent_ngram
                result = {'language': single_lang['language'],'similarity': sum_language}
                results.append(result)
                print(single_lang['language'] + " "+ str(sum_language))


    keys = [res['language'] for res in results]
    set_keys = set(keys)

    final_result = []
    for key in set_keys:
        final_result.append({'language': key, 'similarity': 0})

    for single_result in results:
        for final in final_result:
            if final['language'] == single_result['language']:
                final['similarity'] += single_result['similarity']
    print(final_result)
    # print(final_result)
        # for key in counts_english:
        #     if search == key[0]:
        #         print("English:" + key[0] + " with freq: " + str(key[1]))
        #         perc = key[1]/english_length
        #         sum_english += abs(log(perc))

def getMostSimilarLanguage():
    print()
