import csv
import argparse


def getIdFromCSVText(text):
    return text[2:-1]


def readCSVAsList(fileName):
    rows = []

    with open(fileName, "rb") as fileObject:
        csvReader = csv.reader(fileObject)

        for row in csvReader:
            rows.append(row)

    return rows


def writeListAsCSV(list, fileName):
    with open(fileName, "wb") as fileObject:
        csvWriter = csv.writer(fileObject)

        for row in list:
            csvWriter.writerow(row)


app = readCSVAsList("app.csv")
qcd = readCSVAsList("qcd.csv")

notInWorksheetIds = [row[0] for row in app if row[2] == "FALSE"]
unassignedQuestions = []

for row in qcd:
    id = getIdFromCSVText(row[0])

    if id in notInWorksheetIds and row[4][0:4] != "GCSE":
        unassignedQuestions.append(row)

for row in unassignedQuestions:
    print row

print len(unassignedQuestions)

writeListAsCSV(unassignedQuestions, "output.csv")