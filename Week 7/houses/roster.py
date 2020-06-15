import cs50
import csv
import sys
import re


def main():

    # check cmd arguments
    if len(sys.argv) != 2:
        print("3 Arguments needed!")
        exit()
    house = sys.argv[1].lower().capitalize()

    # open database
    db = cs50.SQL("sqlite:///students.db")
    list = db.execute("SELECT * from students WHERE house = ? ORDER BY last, first", house)

    for row in list:
        if row.get("middle") is not None:
            print(row.get("first") + " " + row.get("middle") + " " + row.get("last") + ", " + "born " + str(row.get("birth")))
        else:
            print(row.get("first") + " " + row.get("last") + ", born " + str(row.get("birth")))


main()