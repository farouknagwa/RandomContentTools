import csv
import argparse
import datetime

physicsGroup = ["benjamin.milnes@nagwa.com", "simeon.every@nagwa.com"]
chemistryGroup = ["nathan.march@nagwa.com", "chris.jones@nagwa.com"]


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


def getChemistryWorksheetTitles(fileName="chemistryWorksheetTitles.txt"):
    lines = []

    with open(fileName, "rb") as fileObject:
        lines = fileObject.readlines()

    return [l.strip() for l in lines]


def getPhysicsQuestionStats():
    qcd = readCSVAsList("qcd.csv")
    sif = readCSVAsList("sif.csv")

    allPhysicsQuestions = []
    questionIdsAndWorksheetTitles = []
    inFlowPhysicsQuestions = []

    for row in qcd:
        if row[3] == "Physics" and row[4][0:4] == "GCSE":
            allPhysicsQuestions.append([getIdFromCSVText(row[0]), row[2], row[3], row[4]])
            questionIdsAndWorksheetTitles.append([getIdFromCSVText(row[0]), row[4]])

    for question in allPhysicsQuestions:
        print question

    writeListAsCSV(questionIdsAndWorksheetTitles, "questionIdsAndWorksheetTitles.csv")

    for row in sif:
        if row[1][0:4] == "GCSE" and row[2] in physicsGroup:
            inFlowPhysicsQuestions.append([getIdFromCSVText(row[0]), row[1], row[2], row[4], row[8]])

    for question in inFlowPhysicsQuestions:
        print question

    approvedQuestions = [q for q in allPhysicsQuestions if q[0] not in [r[0] for r in inFlowPhysicsQuestions]]

    print "Approved Questions: "

    for question in approvedQuestions:
        print question

    writeListAsCSV(approvedQuestions, "approvedQuestions.csv")

    print "Total number of GCSE physics questions that have been uploaded: {0}".format(len(allPhysicsQuestions))
    print "Number of GCSE physics questions that remain in flow: {0}".format(len(inFlowPhysicsQuestions))
    print "Number of GCSE physics questions that have been approved: {0}".format(len(approvedQuestions))


def getChemistryQuestionStats():
    chemistryWorksheetTitles = getChemistryWorksheetTitles()

    qcd = readCSVAsList("qcd.csv")
    sif = readCSVAsList("sif.csv")

    allChemistryQuestions = []
    inFlowChemistryQuestions = []

    for row in qcd:
        if row[3] == "Chemistry" and row[2] in chemistryGroup and row[4] in chemistryWorksheetTitles:
            allChemistryQuestions.append([getIdFromCSVText(row[0]), row[2], row[3], row[4]])

    for question in allChemistryQuestions:
        print question

    for row in sif:
        if row[2] in chemistryGroup and row[1] in chemistryWorksheetTitles:
            inFlowChemistryQuestions.append([getIdFromCSVText(row[0]), row[1], row[2], row[4], row[8]])

    for question in inFlowChemistryQuestions:
        print question

    approvedQuestions = [q for q in allChemistryQuestions if q[0] not in [r[0] for r in inFlowChemistryQuestions]]

    print "Total number of GCSE chemistry questions that have been uploaded: {0}".format(len(allChemistryQuestions))
    print "Number of GCSE chemistry questions that remain in flow: {0}".format(len(inFlowChemistryQuestions))
    print "Number of GCSE chemistry questions that have been approved: {0}".format(len(approvedQuestions))


def getAllChemistryWorksheetTitles():
    qcd = readCSVAsList("qcd.csv")
    titles = []
    gcseTitles = []

    for row in qcd:
        if row[3] == "Chemistry" and row[4] not in [title[0] for title in titles]:
            titles.append([row[4], datetime.datetime.strptime(row[1], "%m/%d/%Y %I:%M:%S %p")])

    titles = sorted(titles, key=lambda title: title[1])

    for title in titles:
        print title
        if title[1] > datetime.datetime(2018, 07, 19, 0, 0, 0):
            gcseTitles.append(title[0] + "\n")

    with open("chemistryWorksheetTitles.txt", "wb") as fileObject:
        fileObject.writelines(gcseTitles)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("subject")

    arguments = parser.parse_args()

    if arguments.subject == "physics":
        getPhysicsQuestionStats()

    if arguments.subject == "chemistry":
        getChemistryQuestionStats()
