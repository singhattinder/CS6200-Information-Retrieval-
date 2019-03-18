import os
import nltk
import collections
import numpy as np
from itertools import accumulate

class InvertedIndexer:
    def __init__(self, directory_name):

        if not os.path.exists("Proximity_query"):
            os.mkdir("Proximity_query")

        self.corpus_dictionary = {}
        self.list_of_documents = set()
        self.inverted_index = collections.defaultdict(list)

        for file in os.listdir(directory_name):
            # this was throwing error reading in utf-8, so we have to exclude this macOS metadata file
            if file != ".DS_Store":
                with open(directory_name + '/' + file, encoding='ascii', mode='r') as file_input:
                    data = file_input.read()
                    # getting rid of extension for document id
                    key_name = file.rstrip(".txt")
                    # this dictionary has keys as document Id or file name and values as corpus data
                    self.corpus_dictionary[key_name] = data

    def index_delta(self):
        count = 0
        for file, corpus in self.corpus_dictionary.items():
            # tokenising the corpus
            token = nltk.word_tokenize(corpus)
            # making a numpy array
            values = np.array(token)
            for word in set(token):
                # checking where word matches and returning a list
                ii = np.where(values == word)[0]
                # delta encoding
                list_final = np.diff(ii).tolist()
                # putting back first element in delta encoding
                list_final.insert(0, ii[0])
                self.inverted_index[word].append({file: list_final})
            count += 1
            print(count)

        return self.inverted_index

    def list_of(self, term1, term2, input_in):
        # casefolding all to inputs to lower cases
        term1 = term1.casefold()
        term2 = term2.casefold()
        index = self.inverted_index
        # getting the list from index
        list1 = index[term1]
        list2 = index[term2]

        for first_dictionary in list1:
            for second_dictionary in list2:
                for k, v in first_dictionary.items():
                    for a, b in second_dictionary.items():
                        if k == a:
                            # conversion from delta encoding
                            c = list(accumulate(v))
                            d = list(accumulate(b))
                            self.calculate(c, d, k, input_in)

    def calculate(self, c, d, k, input_in):
        for i in range(len(c)):
            for j in range(len(d)):
                # calculating for any ordered input
                if abs(c[i] - d[j]) <= input_in + 1:
                    self.list_of_documents.add(k)
                    return
                elif j + 1 <= len(d) - 1 and abs(c[i] - d[j + 1]) <= input_in + 1:
                    self.list_of_documents.add(k)
                    return
                elif i + 1 <= len(c) - 1 and abs(c[i + 1] - d[j]) <= input_in + 1:
                    self.list_of_documents.add(k)
                    return

    def write_to_file(self, filename):
        with open("Proximity_query/" + filename + ".txt", encoding='utf8', mode='w') as file:
            file.write("\n".join(self.list_of_documents))


obj = InvertedIndexer("scrap")
obj.index_delta()
obj.list_of("space", "mission", 6)
obj.write_to_file("documents_with_space_mission_6")
obj.list_of("space", "mission", 12)
obj.write_to_file("documents_with_space_mission_12")
obj.list_of("earth", "orbit", 5)
obj.write_to_file("documents_with_earth_orbit_5")
obj.list_of("earth", "orbit", 10)
obj.write_to_file("documents_with_earth_orbit_10")
