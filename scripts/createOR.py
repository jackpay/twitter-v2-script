import csv

csvpath = ""
headerkey = "Concerns"
headerveh = "environment"

with open(csvpath, 'r') as csvfile:
    reader = csv.reader(csvfile)
    indx = next(reader).index(headerkey)
    print( "(" + " OR ".join([ "\\\"" + str(row[indx]) + "\\\"" for row in reader if len(row[indx]) > 0]) + ")")

