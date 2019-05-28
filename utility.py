import re
import string, random, time
from collections import Counter, defaultdict

# funkcja tworząca z tekstu ngramy
def zip_ngrams(text, n=3, exact=True):
    return ["".join(j).upper() for j in zip(*[text[i:] for i in range(n)])]
    
# Usuwanie nieznaczących danych dla poszczególnych języków
def clear_text(text):
    return re.sub(r'\d+', '', text).translate(str.maketrans('','',string.punctuation)).strip()

# Scalanie ngramów do jednej listy w celu łatwiejszego operowania na nich
# [house ite] = [[hou, ous, use], [ite] ... ] => [hou, ous ...]
def flatten_array(array):
    return [item for sublist in array for item in sublist]

#znajduje w podanej tablicy języków wystąpienie danego n-gramu
#languageMap = [{"data": english_list, "language": "English"},{"data": german_list, "language": "German"}]
def find_in_lng(ngram, languageMap):
    result = {}
    for language in languageMap:
        result[language["language"]] = Counter(language["data"])[ngram]
    return result