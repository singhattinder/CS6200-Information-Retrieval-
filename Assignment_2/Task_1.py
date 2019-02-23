from bs4 import BeautifulSoup
from nltk.util import ngrams
import urllib.request
import string
import nltk
import re
import matplotlib.pyplot as plt
import json
nltk.download('punkt')


file = open("BFS.txt", "r")
count = 0

string.punctuation = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'

translator = str.maketrans('', '', string.punctuation)

dict = {}

for line in file:
    response = urllib.request.urlopen(line)
    bs = BeautifulSoup(response.read(), features='lxml')
    file_name = line.replace("https://en.wikipedia.org/wiki/", "")
    file_name = file_name.replace("\n", "")

    # removing javascript, css, links from html page
    for script in bs(["script", "style", "link"]):
        script.decompose()

    page = bs.get_text()

    lines = (line.strip() for line in page.splitlines())

    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    formatted_page = '\n'.join(chunk for chunk in chunks if chunk)

    # removing all punctuations except hyphen
    final_page = ' '.join(word.translate(translator) for word in formatted_page.split())

    # removing text starting with http or https
    links_removed = ' '.join(word.casefold() if word is not None or re.match('^(http|https).*', word) else "" for word in final_page.split())

    # removing non english content
    string_val = links_removed.encode('ascii', errors='ignore').decode()

    # tokenizing
    token = nltk.word_tokenize(string_val)

    # making trigrams
    trigrams = ngrams(token, 3)

    # adding trigrams to dictionary data structure and counting frequency
    for gram in trigrams:
        dict[gram] = dict.get(gram, 0) + 1

    # creating a file with given file name but replacing / with . because of unix directory structure
    with open("scrap/" + file_name.replace("/", ".") + ".txt", mode='w', encoding='utf-8') as code:
        code.write(string_val)

    count = count + 1
    print(str(count) + "  " + file_name)

file.close()

listofTuples = sorted(dict.items(), reverse=True, key=lambda x: x[1])


#print(listofTuples)

print(len(listofTuples))


frequency = [elem[1] for elem in listofTuples]

rank_dict = []

for i in range(len(frequency)):

    rank_dict.append(i)

plt.ylabel("Total Number of Occurrences")
plt.xlabel("Rank of word")

plt.loglog(rank_dict, frequency, basex=10)
plt.show()


total_sum = 0

for i in frequency:
    total_sum = total_sum + i

rank = 1

constant = []

for i in frequency:
    constant.append(rank * (i/total_sum))
    rank = rank + 1

rank_new = 1

new_list = {}

for i in constant:
    new_list[rank_new] = i
    rank_new = rank_new + 1

with open("constant_rank.txt", 'w') as file_new:
    file_new.write(json.dumps([{"Rank": k, "constant": v} for k, v in new_list.items()], indent=4))
file_new.close()
