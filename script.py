import csv


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

qcd = readCSVAsList("qcd.csv")
sif = readCSVAsList("sif.csv")

allPhysicsQuestions = []
questionIdsAndWorksheetTitles = []
inFlowPhysicsQuestions = []

for row in qcd:
    if row[3] == "Physics" and row[4][0:4] == "GCSE":
        allPhysicsQuestions.append([getIdFromCSVText(row[0]), row[2], row[3], row[4]])
        questionIdsAndWorksheetTitles.append([ getIdFromCSVText(row[0]), row[4]])

for question in allPhysicsQuestions:
    print question

writeListAsCSV(questionIdsAndWorksheetTitles, "questionIdsAndWorksheetTitles.csv")

for row in sif:
    if row[1][0:4] == "GCSE" and (row[2] == "benjamin.milnes@nagwa.com" or row[2] == "simeon.every@nagwa.com"):
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
