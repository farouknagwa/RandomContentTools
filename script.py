import csv

def getIdFromCSVText(text):
    return text[2:-1]

class CSVFile (object):
    def __init__(self, fileName):
        self.fileName = fileName

    def __enter__(self):
        self.fileObject = open(self.fileName, "rb")
        self.csvReader = csv.reader(self.fileObject)
        return self.csvReader

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fileObject.close()


allPhysicsQuestions = []

with CSVFile("qcd.csv") as csvFile:
    for row in csvFile:
        if row[3] == "Physics" and row[4][0:4] == "GCSE":
            allPhysicsQuestions.append( [ getIdFromCSVText( row[0]), row[2], row[3], row[4]])

for question in allPhysicsQuestions:
    print question

print "Total number of GCSE physics questions that have been uploaded: {0}".format( len(allPhysicsQuestions))


inFlowPhysicsQuestions = []

with CSVFile("sif.csv") as csvFile:
    for row in csvFile:
        if  row[1][0:4] == "GCSE" and ( row[2] == "benjamin.milnes@nagwa.com" or row[2] == "simeon.every@nagwa.com"):
            inFlowPhysicsQuestions.append([ getIdFromCSVText( row[0]), row[1], row[2], row[4], row[8]])


for question in inFlowPhysicsQuestions:
    print question

n =  len( allPhysicsQuestions) -  len( inFlowPhysicsQuestions)

print "Total number of GCSE physics questions that have been uploaded: {0}".format( len(allPhysicsQuestions))
print "Number of GCSE physics questions that remain in flow: {0}".format( len( inFlowPhysicsQuestions))
print "Number of GCSE physics questions that have been approved: {0}".format(  n)
