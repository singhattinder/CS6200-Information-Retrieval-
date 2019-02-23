import urllib.request, requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re



class GraphBuilder:

    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.docs = set([line[30:].rstrip('\n') for line in file.readlines()])
        self.graph = defaultdict(list)

    def links_in_page(self, doc):
        url = "https://en.wikipedia.org/wiki/" + doc
        response = urllib.request.urlopen(url)
        if response.getcode() == requests.codes.ok:
            bs = BeautifulSoup(response.read(), features='lxml')

            link_set = set()

            for link in bs.findAll('a'):
                relative_link = link.get('href')
                if type(relative_link) is str:
                    exp = re.match("^/wiki/*.*", relative_link)
                    if type(exp) is re.Match and ":" not in exp.group() and exp.group()[6:] in self.docs:
                        link_set.add(exp.group()[6:])
            return link_set

    def graph_build(self):
        count = 0
        for doc in self.docs:
            print(str(count) + " " + doc)
            count = count + 1
            for link in self.links_in_page(doc):
                if link != doc:
                    self.graph[link].append(doc)

    def print_graph(self):
        for doc, inlinks in self.graph.items():
            print(doc)
            for link in inlinks:
                print(' ' + link)
            print('\n')

    def write_graph(self, filename):
        with open(filename, 'w+') as file:
            for doc, incoming_links in self.graph.items():
                file.write(doc)
                for link in incoming_links:
                    file.write(' ' + link)
                file.write('\n')

    def read_graph(self, file_name):
        links = defaultdict(list)
        with open(file_name, 'r') as file:
            for line in file:
                pages = line.rstrip('\n').split(' ')
                page, in_links = pages[0], pages[1:]
                for link in in_links:
                    links[page].append(link)
        return links



g1 = GraphBuilder("BFS.txt")
g1.graph_build()
g1.print_graph()
g1.write_graph("g1.txt")


g2 = GraphBuilder("FOCUSED.txt")
g2.graph_build()
g2.write_graph("g2.txt")

g3 = GraphBuilder("BFS.txt")
dicton = g3.read_graph("g2.txt")


count = 0
list_pages = dicton.keys()

for k, v in dicton.items():
    for item in v:
        if item not in dicton:
            count += 1


print("G2 out degree " + str(count) + '\n')

g3 = GraphBuilder("BFS.txt")
dicton1 = g3.read_graph("g1.txt")


count = 0
list_pages = dicton1.keys()

for k, v in dicton1.items():
    for item in v:
        if item not in dicton1:
            count += 1


print("G1 out degree " + str(count) + '\n')

g3 = GraphBuilder("BFS.txt")
dicton2 = g3.read_graph("g1.txt")


max = 0
list_pages = dicton2.keys()

for k, v in dicton2.items():
    if len(v) >= max:
        max = len(v)
    else:
        max = max


print("Max in degree G1 " + str(max) + '\n')

g4 = GraphBuilder("BFS.txt")
dicton2 = g4.read_graph("g2.txt")


max = 0
list_pages = dicton2.keys()

for k, v in dicton2.items():
    if len(v) >= max:
        max = len(v)
    else:
        max = max


print("Max in degree G2 " + str(max) + '\n')




g6 = GraphBuilder("BFS.txt")
dicton1 = g6.read_graph("g2.txt")


max = 0
list_pages = dicton1.keys()

for k, v in dicton1.items():
    for item in v:
        current_max = 0
        for i, j in dicton.items():
            if item in j:
                current_max +=1
        if current_max >= max:
            max = current_max


print("Max out degree G2 " + str(max) + '\n')

