import os
import nltk
import collections
import json
import numpy as np


class InvertedIndexer:
    def __init__(self, directory_name):

        self.corpus_dictionary = {}

        if not os.path.exists("inverted_index"):
            os.mkdir("inverted_index")

        for file in os.listdir(directory_name):
            # this was throwing error reading in utf-8, so we have to exclude this macOS metadata file
            if file != ".DS_Store":
                with open(directory_name + '/' + file, encoding='ascii', mode='r') as file_input:
                    data = file_input.read()
                    # getting rid of extension for document id
                    key_name = file.rstrip(".txt")
                    # this dictionary has keys as document Id or file name and values as corpus data
                    self.corpus_dictionary[key_name] = data

    # task 1 - a
    def index_freq(self, gram=1):
        # default dictionary with initial values of empty list
        inverted_index = collections.defaultdict(list)
        for file, corpus in self.corpus_dictionary.items():
            # tokens as single words as a list is returned
            token = nltk.word_tokenize(corpus)
            # makes ngrams or you can use nltk.ngram
            ngram = zip(*[token[i:] for i in range(gram)])
            # Counter takes a list and makes a dictionary with values as frequency of keys
            count_dictionary = collections.Counter(ngram)
            for term, frequency in count_dictionary.items():
                # appending to inverted index dictionary with file as document id and frequency of term
                if gram == 1:
                    inverted_index[term[gram-1]].append({file: frequency})
                elif gram == 2:
                    string = term[gram-2] + " " + term[gram-1]
                    inverted_index[string].append({file: frequency})
                elif gram == 3:
                    string = term[gram-3] + " " + term[gram-2] + " " + term[gram-1]
                    inverted_index[string].append({file: frequency})
        return inverted_index

    # task 1 - b
    def number_of_terms(self, gram=1):
        terms = {}
        for file, corpus in self.corpus_dictionary.items():
            # tokens as single words as a list is returned
            token = nltk.word_tokenize(corpus)
            # makes ngrams or you can use nltk.ngram
            ngram = zip(*[token[i:] for i in range(gram)])
            # storing number of terms in dictionary terms
            terms[file] = len(set(ngram))
        return terms

    def index_delta(self):
        # making a default dictionary which has list as default value
        inverted_index = collections.defaultdict(list)
        count = 0
        for file, corpus in self.corpus_dictionary.items():

            # tokens as single words as a list is returned
            token = nltk.word_tokenize(corpus)
            # tokens in numpy array
            values = np.array(token)
            for word in set(token):
                # returning an array where word matches
                ii = np.where(values == word)[0]
                # delta encoding
                list_final = np.diff(ii).tolist()
                # putting back first element because it was omitted while calculating d gaps
                list_final.insert(0, ii[0])
                # appending to inverted index
                inverted_index[word].append({file: list_final})
            count += 1
            print(count)

        return inverted_index

    # writing files to system in json format
    def write_to_file(self, filename, ob):
        with open("inverted_index/" + filename + ".txt", encoding='utf8', mode='w') as file:
            file.write(json.dumps(ob, indent=2))


obj = InvertedIndexer("scrap")
# writing inverted index to files
# for i in 1, 2, 3:
#     obj.write_to_file("index_"+str(i), obj.index_freq(i))

# write task 1-d to file
with open("inverted_index/" + "inverted_index_delta_encoded" + ".txt", encoding='utf8', mode='w') as file:
    for k, v in obj.index_delta().items():
        file.write(str(k) + "  " + str(v) + "\n")

# writing task 1-b to file
# with open("inverted_index/" + "document_terms_task1_b" + ".txt", encoding='utf8', mode='w') as file:
#     for k, v in obj.number_of_terms().items():
#         file.write(str(k) + ":  " + str(v) + "\n")

