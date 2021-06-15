import csv

def count_rows(csvpath):
    with open(csvpath,'r') as csvfile:
        reader = csv.reader(csvfile)
        print(len([x for x in reader])-1)


if __name__ == "__main__":
    csvpath = ""
    count_rows(csvpath)