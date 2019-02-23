import urllib.request, requests
from bs4 import BeautifulSoup
import re
from time import sleep
import json


class Crawler:

    def __init__(self, seed_url, max_depth = 6, total_links = 1000, keywords = None):
        self.wait = 1
        self.max_depth = max_depth
        self.total_links = total_links
        self.seed_url = seed_url
        self.res = [seed_url]
        self.duplicate = {}
        self.keywords = [keyword.lower() for keyword in keywords] if keywords else None
        self.count = 1



    def links_in_page(self, url):

        # Politeness policy for 1 second
        sleep(self.wait)

        response = urllib.request.urlopen(url)

        #filtering out redicted URL
        if response.getcode() == requests.codes.ok:
            bs = BeautifulSoup(response.read(), features='lxml')
            self.count += 1
            with open("scrap/scrapped"+str(self.count)+".html", mode="w", encoding="utf8") as code:
                code.write(str(bs.prettify()))

            link_list = []

            # requirement d) 1, 2 and 3
            # Taking only urls which start with wiki and filtering links with :, So ignoring links with # and :

            for link in bs.findAll('a'):
                relative_link = link.get('href')
                if type(relative_link) is str:
                    exp = re.match("^/wiki/*.*", relative_link)
                    if type(exp) is re.Match and ":" not in exp.group():
                        if self.keywords is not None and not self.check(relative_link, link.string):
                            continue
                        link_list.append(exp.group())
                        if exp.group() not in self.duplicate:
                            self.duplicate[exp.group()] = 1
                        else:
                            self.duplicate[exp.group()] += 1

            header = "https://en.wikipedia.org"

            link_list_new = []

            for link in link_list:
                link_list_new.append(header + link)

            return link_list_new

    def check(self,url,text):
        for keyword in self.keywords:
            if url.lower().find(keyword) != -1 or (text and text.lower().find(keyword) != -1):
                return True
        return False

    def bfs(self):
        pages = 1
        depth = {self.seed_url: 1}
        for url in self.res:

            if depth[url] > self.max_depth:
                print("maximum depth has been reached:", self.max_depth)
                return

            links_list = self.links_in_page(url)

            for link in links_list:
                if link not in depth:
                    depth[link] = depth[url] + 1
                    self.res.append(link)
                    pages = pages + 1
                    if pages >= self.total_links:
                        print("maximum pages has been crawled and at depth", depth[link])
                        return

    def dfs(self):
        self.res = []
        self.visited_list = {self.seed_url: True}
        self.depth = 1
        self.dfs_recursive(1, self.seed_url)
        print("max depth reached", self.max_depth)

    def dfs_recursive(self, depth, url):
        self.depth = max(depth, self.depth)
        self.res.append(url)
        self.visited_list[url] = True
        if len(self.res) >= self.total_links:
            return
        if depth < self.max_depth:
            for link in self.links_in_page(url):
                if len(self.res) < self.total_links and link not in self.visited_list:
                    self.dfs_recursive(depth + 1, link)

    def get_results(self):
        return self.res

    def get_duplicates(self):
        return self.duplicate

    def write_crawled_links(self, name, stream):
        file = open(name, "w")
        if type(stream) is list:
            try:
                for url in stream:
                    file.write(url + "\n")
                file.close()
            except:
                print("Something went wrong with writing file")
        elif type(stream) is dict:
            try:
                with open(name, 'w') as file_new:
                    file_new.write(json.dumps([{"URL": k, "count": v } for k,v in stream.items()], indent=4))
                file_new.close()
            except:
                print("Something went wrong with writing file")
        else:
            print("stream can be list or dictionary only")





# seed URL from assignment
url = "https://en.wikipedia.org/wiki/Space_exploration"

obj = Crawler(url)

print("BFS\n")
obj.bfs()

obj.write_crawled_links("bfs_1.txt", obj.get_results())

print("DFS\n")
obj.dfs()

obj.write_crawled_links("dfs_1.txt", obj.get_results())

keywords = "Mars Rover Orbiter Pathfinder Mars Mission Exploration".split(' ')

obj = Crawler(url, keywords = keywords)

print("focused\n")
obj.bfs()

obj.write_crawled_links("Duplicates_focused.txt", obj.get_duplicates())

obj.write_crawled_links("focused_1.txt", obj.get_results())


input_url = input("Enter seed URL: ")
keywords_new = input("Enter keywords for focused crawling (split by a single space): ").split(' ')

obj = Crawler(input_url, keywords = keywords_new)
obj.bfs()

obj.write_crawled_links("Duplicates_focused_entered_maunally.txt", obj.get_duplicates())

obj.write_crawled_links("focused_entered_manually.txt", obj.get_results())
