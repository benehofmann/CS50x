import cs50
import csv
import sys
import re


def main():
    first = ""
    middle = ""
    last = ""
    # checking cmd arguments
    if len(sys.argv) != 2:
        print("3 Arguments needed!")
        exit()

    # opening the db
    db = cs50.SQL("sqlite:///students.db")
    db.execute("SELECT * from students")

    # opening the csv file
    with open(sys.argv[1], "r") as students:

        # create a DictReader
        reader = csv.DictReader(students)

        # Iterate over CSV file
        for row in reader:
            middle = None
            # check if 2 or 3 three names
            if len(row["name"].split()) == 3:
                first = row["name"].split()[0]
                middle = row["name"].split()[1]
                last = row["name"].split()[2]
            else:
                first = row["name"].split()[0]
                last = row["name"].split()[1]

            # get the house
            house = row["house"]
            # get the birthday
            birth = int(row["birth"])

            #insert in db
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       first, middle, last, house, birth)


main()