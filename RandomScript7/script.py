import sqlite3
from tabulate import tabulate

gcseWorksheets = []

with open("gcse_worksheets.txt") as fileObject:
    gcseWorksheets = fileObject.readlines()

gcseWorksheets = [w.strip() for w in gcseWorksheets]

def numberOfWorksheetsAttachedToLessons(cursor):

    cursor.execute("SELECT COUNT(DISTINCT qcd.WorksheetName) FROM lie LEFT JOIN llqpq ON lie.LessonID = llqpq.LessonID LEFT JOIN qcd ON llqpq.QuestionID = qcd.QuestionID WHERE lie.Subject = 'Physics' AND lie.gvalue < 11 ORDER BY qcd.WorksheetName")

    return cursor.fetchone()[0]

def worksheetsAttachedToLessons(cursor):

    cursor.execute("SELECT DISTINCT qcd.WorksheetName FROM lie LEFT JOIN llqpq ON lie.LessonID = llqpq.LessonID LEFT JOIN qcd ON llqpq.QuestionID = qcd.QuestionID WHERE lie.Subject = 'Physics' AND lie.gvalue < 11 ORDER BY qcd.WorksheetName")

    return [str(r[0]) for r in  cursor.fetchall()]

def rogueWorksheets(cursor):

    worksheets = worksheetsAttachedToLessons(cursor)

    return [w for w in worksheets if w not in gcseWorksheets]

def unusedWorksheets(cursor):

    worksheets = worksheetsAttachedToLessons(cursor)

    return [w for w in gcseWorksheets if w not in worksheets]


connection = sqlite3.connect("Database/nagwa.db")
cursor = connection.cursor()

cursor.execute("SELECT lie.LessonID, lie.LessonTitle, lie.WorksheetId, lie.Subject, lie.gvalue, lie.Live, llqpq.QuestionID, qcd.WorksheetName FROM lie LEFT JOIN llqpq ON lie.LessonID = llqpq.LessonID LEFT JOIN qcd ON llqpq.QuestionID = qcd.QuestionID WHERE lie.Subject = 'Physics' AND lie.gvalue < 11")

rows = cursor.fetchall()

# print tabulate(rows)


print

print "Worksheets used in lesson that aren't in the tracker: {0}".format(", ".join( rogueWorksheets(cursor)))
print "Worksheets in the tracker that aren't used in lessons: {0}".format(", ".join( unusedWorksheets(cursor)))

print

print "Number of GCSE worksheets in tracker: {0}".format(len(gcseWorksheets))
print "Number of GCSE worksheets in database: {0}".format(numberOfWorksheetsAttachedToLessons(cursor))

connection.close()