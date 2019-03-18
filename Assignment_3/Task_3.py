import os

class Stats:

    def __init__(self):

        if not os.path.exists("stats"):
            os.mkdir("stats")

        # for all values from 1 to 3
        for n in 1, 2, 3:
            # opening inverted index files from task 1 -a
            file = "inverted_index/index_" + str(n) + ".txt"
            with open(file, 'r') as fin:
                index = eval(fin.read())
                # making term frequency and document frequency dictionary
            term_frequency, document_frequency = {}, {}
            for term, ls in index.items():
                document_frequency[term] = len(ls)
                count = 0
                for doc in ls:
                    for k, v in doc.items():
                        count += v
                term_frequency[term] = count

            with open("stats/stop_list_" + str(n) + ".txt", "w") as fout:
                for term, freq in document_frequency.items():
                    if freq > 800:
                        fout.write(str(term) + ":   " + str(freq) + '\n')

            with open("stats/term_frequency_" + str(n) + ".txt", "w") as file:
                term_frequency = sorted(term_frequency.items(), key=lambda x: x[1], reverse=True)
                for term, freq in term_frequency:
                    file.write(str(term) + ":   " + str(freq) + '\n')

            with open("stats/document_frequency_" + str(n) + ".txt", "w") as file:
                document_frequency = sorted(document_frequency.items())
                for term, freq in document_frequency:
                    file.write(str(term) + "  ")
                    for doc in index[term]:
                        for k, v in doc.items():
                            file.write(str(k) + ',')
                    file.write(":  " + str(freq) + "\n")


obj = Stats()



