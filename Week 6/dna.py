import csv
import sys
import re
import copy
from cs50 import get_string

# command line arguments einbauen

# open the files via open(filename)
# read the files via read()


def main():
    dictdata = {}  # csv dictionary
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        exit()

# read the database with DictReader
    try:
        database = csv.DictReader(open(sys.argv[1]))
        dictdata = database  # csv.dictionary

        database_without_names = csv.DictReader(open(sys.argv[1]))
        dictdata_without_names = database_without_names  # csv.dictionary

        # deletes the first item in row (eg. the name)
        for row in database_without_names:
            row.popitem(last=False)

    except:
        print("File not found")
        exit()

    try:
        file = open(sys.argv[2], 'r')  # open the file
        sample = file.read()  # parse sample is a string
    except:
        print("File not found")
        exit()

    # writing every header value in a string array
    headervalues = len(database.fieldnames)  # amount of headervalues

    STR_List = storeFieldNames(database, headervalues)  # create a List with each STR header

    valuedict = dict.fromkeys(STR_List)  # create a dictionary only with keys
    for key in valuedict:  # iterate through the dictionary
        valuedict[key] = countLongestSequence(sample, key)

    for row in dictdata:  # example Key[0] =
        name = row.get("name")
        counter = 0
        found = False
        lastelement = next(reversed(row))
        for key in row:
            sequnce_number = valuedict.get(key)  # data of the sequence-list
            try:
                csv_data = int(row.get(key))  # data of the csv
            except:
                csv_data = row.get(key)
                found = False
            if sequnce_number == csv_data:
                found = True
                if database.fieldnames[counter + 1] == next(reversed(row)):
                    print(name)
                    return
            else:  # not found
                continue
            counter += 1
    print("No match")


def storeFieldNames(database, headervalues):
    STR_List = []
    for i in range(1, headervalues):
        # print(database.fieldnames[i])
        STR_List.insert(i-1, database.fieldnames[i])

    return STR_List


def countLongestSequence(sample, sequence):
    Count = sample.count(sequence)  # occurencies in the String
    # building a decreasing loop to find the longest match
    for i in reversed(range(Count)):
        tosearch = (sequence * (i+1))
        if tosearch in sample:
            return tosearch.count(sequence)


main()
