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


def getQuestionDetails(fileName):
    questionDetails = readCSVAsList(fileName)
    return [{"id": getIdFromCSVText(r[0]), "dateSubmitted": r[1], "questionCreator": r[2], "subject": r[3], "worksheetId": r[5], "worksheetName": r[4], "numberOfPartsToQuestion": r[6]} for r in questionDetails]


def getGCSEQuestions(questionDetails):
    return [r for r in questionDetails if r["worksheetName"][0:4] == "GCSE"]


def getQuestionsWithIds(questionDetails, ids):
    return [r for r in questionDetails if r["id"] in ids]


def removeQuestionsWithIds(questionDetails, ids):
    return [r for r in questionDetails if r["id"] not in ids]


def removeBlankRows(list):
    return [r for r in list if len(r) > 0]


def printList(list):
    for r in list:
        print r


approvedPhysicsQuestions = readCSVAsList("apq.csv")[1:]

ids = [r[0] for r in approvedPhysicsQuestions]

questionDetails = getQuestionDetails("qcd.csv")
gcseQuestions = getGCSEQuestions(questionDetails)
approvedGCSEQuestions = getQuestionsWithIds(gcseQuestions, ids)

print len(approvedGCSEQuestions)

output = []

for question in approvedGCSEQuestions:
    worksheetId = [r for r in approvedPhysicsQuestions if r[0] == question["id"]][0][3]

    output.append([question["id"], question["worksheetId"], question["worksheetName"]])

printList(output)

writeListAsCSV(output, "output.csv")
