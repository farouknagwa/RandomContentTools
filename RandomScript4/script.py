from csvtools import *

def getQuestionDetails(fileName):
    questionDetails = readCSVAsList(fileName)
    return [{"id": getIdFromCSVText(r[0]), "dateSubmitted": r[1], "questionCreator": r[2], "subject": r[3], "worksheetId": r[5], "worksheetName": r[4], "numberOfPartsToQuestion": r[6]} for r in questionDetails]


def getGCSEQuestions(questionDetails):
    return [r for r in questionDetails if r["worksheetName"][0:4] == "GCSE"]


def getQuestionsWithIds(questionDetails, ids):
    return [r for r in questionDetails if r["id"] in ids]


def removeQuestionsWithIds(questionDetails, ids):
    return [r for r in questionDetails if r["id"] not in ids]

app = readCSVAsList("app.csv")
wsi = readCSVAsList("wsi.csv")

output = []

for row in app:
    matchingRows = [r for r in wsi if r[2].strip() == row[2].strip()]
    if len(matchingRows) > 0:
        worksheetId =  matchingRows[0]
        output.append([row[0], row[2], worksheetId[0], worksheetId[1]])
    else:
        output.append([row[0], row[2], ""])


printList(output)

print len(app)
print  len(output)

writeListAsCSV(output, "output.csv")