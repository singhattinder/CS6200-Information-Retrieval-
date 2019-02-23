from collections import defaultdict
import numpy as np


class PageRank():

    def __init__(self, file_name):
        self.links = defaultdict(list)
        with open(file_name, 'r') as file:
            for line in file:
                pages = line.rstrip('\n').split(' ')
                page, in_links = pages[0], pages[1:]
                for link in in_links:
                    self.links[page].append(link)
        self.pages = self.links.keys()
        self.norm = []

    def procedure(self, lamb=0.15):

        I = {}
        R = {}


        count = 0
        old_l2_norm = 0
        x = dict()

        for page in self.pages:
            x[page] = 0

        for page in self.pages:
            I[page] = 1/len(self.pages)


        while count < 4:
            for page in self.pages:
                R[page] = lamb/len(self.pages)

            for page in self.pages:
                Q = set()
                for same_page in self.pages:
                    if page is not same_page:
                        for q in self.links[same_page]:
                            if q is page and same_page in self.pages:
                                Q.add(same_page)

                if len(Q) > 0:
                    for q in Q:
                        R[q] += ((1 - lamb) * I[page]) / len(Q)
                else:
                    for p in self.pages:
                        R[p] += ((1 - lamb) * I[page]) / len(self.pages)

                x[page] = (R[page] - I[page])

            for j in self.pages:
                I[j] = R[j]

            vector = []

            for key, val in x.items():
                vector.append(val)

            current_l2_norm = np.linalg.norm(vector, 2)

            sum1 = 0
            for k, v in R.items():
                sum1 = sum1 + v

            self.norm.append("norm " + str(current_l2_norm) + " sum " + str(sum1) + '\n')

            change_l2_norm = current_l2_norm - old_l2_norm

            if change_l2_norm < 0.0005:
                count = count + 1
            else:
                count = 0
            old_l2_norm = current_l2_norm
        return R

    def write_norm(self, file_name):
        with open(file_name, 'w') as file:
            for item in self.norm:
                file.write(item)
        file.close()


pr0 = PageRank("ungrade.txt")
print("\n" + "Ungraded results")
list_sort0 = pr0.procedure()
#list_sort0 = pr0.procedure(lamb=0.25)
#list_sort0 = pr0.procedure(lamb=0.35)
#list_sort0 = pr0.procedure(lamb=0.5)
print(sorted(list_sort0.items(), reverse=True, key=lambda x: x[1]))


pr = PageRank("g1.txt")
print("\n" + "G1 results")
list_sort = pr.procedure()
#list_sort = pr.procedure(lamb=0.25)
#list_sort = pr.procedure(lamb=0.35)
#list_sort = pr.procedure(lamb=0.5)
print(sorted(list_sort.items(), reverse=True, key=lambda x: x[1]))

print("\n" + "G2 results")
pr1 = PageRank("g2.txt")

list_sort1 = pr1.procedure()
#list_sort1 = pr1.procedure(lamb=0.25)
#list_sort1 = pr1.procedure(lamb=0.35)
#list_sort1 = pr1.procedure(lamb=0.5)
print(sorted(list_sort1.items(), reverse=True, key=lambda x: x[1]))




