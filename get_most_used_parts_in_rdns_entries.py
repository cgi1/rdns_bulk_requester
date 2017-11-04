from collections import Counter
import os
import glob



def count(filepath):

    with open(filepath, 'r') as myfile:
        data=myfile.read().replace('\n', '.')

    t = 'this is the textfile, and it is used to take words and count'

    counted_dict = dict(Counter(data.split('.')))
    ten_most_common_strings = dict(Counter(data.split('.')).most_common(10))

    print(ten_most_common_strings)


list_of_files = glob.glob(os.getcwd() + '/logs/*') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
count(filepath=latest_file)
