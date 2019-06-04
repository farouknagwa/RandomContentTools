import sqlite3
from tabulate import tabulate
from csvtools import *
import re

gcseWorksheets = []
gcseLessons = []

with open("gcse_worksheets.txt") as fileObject:
    gcseWorksheets = fileObject.readlines()

gcseWorksheets = [w.strip() for w in gcseWorksheets]

with open("gcse_lessons.txt") as fileObject:
    gcseLessons = fileObject.readlines()

gcseLessons = [l.strip() for l in gcseLessons]

phase1 = readCSVAsList("phase1.csv")
phase2 = readCSVAsList("phase2.csv")

phase1 = phase1[1:]
phase2 = phase2[1:]

phase1 = [r for r in phase1 if r[2] != '']
phase2 = [r for r in phase2 if r[2] != '']

phase1 = [[r[2], r[3], r[9], r[19], r[20], r[21]] for r in phase1]
phase2 = [[r[2], r[3], r[9], r[19], "", ""] for r in phase2]

phases = phase1 + phase2



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


def physicsLessons(cursor):

    cursor.execute("SELECT lie.LessonID, lie.LessonTitle, lie.Subject, lie.gvalue, lie.Live FROM lie WHERE lie.Subject = 'Physics' AND lie.gvalue < 11 ORDER BY lie.LessonTitle")

    return tabulate(cursor.fetchall())

def physicsLessonsNames(cursor):

    cursor.execute("SELECT lie.LessonTitle FROM lie WHERE lie.Subject = 'Physics' AND lie.gvalue < 11 ORDER BY lie.LessonTitle")

    return [r[0] for r in  cursor.fetchall()]

def numberOfPhysicsLessons(cursor):

    cursor.execute("SELECT COUNT(*) FROM lie WHERE lie.Subject = 'Physics' AND lie.gvalue < 11 ORDER BY lie.LessonTitle")

    return cursor.fetchone()[0]

def unlinkedPhysicsQuestions(cursor):

    cursor.execute("SELECT qcd.QuestionId, qcd.WorksheetName, llqpq.LessonId FROM qcd LEFT OUTER JOIN llqpq ON qcd.QuestionId = llqpq.QuestionId WHERE llqpq.LessonId IS NULL AND qcd.Subject = 'Physics'")

    return cursor.fetchall()

def realLessons(cursor):

    cursor.execute("SELECT * FROM lessons")

    return cursor.fetchall()


connection = sqlite3.connect("Database/nagwa.db")
cursor = connection.cursor()

print

print "Worksheets used in lesson that aren't in the tracker: {0}".format(", ".join( rogueWorksheets(cursor)))
print "Worksheets in the tracker that aren't used in lessons: {0}".format(", ".join( unusedWorksheets(cursor)))

print

print "Number of GCSE worksheets in tracker: {0}".format(len(gcseWorksheets))
print "Number of GCSE worksheets in database: {0}".format(numberOfWorksheetsAttachedToLessons(cursor))

print 

print physicsLessons(cursor)

print
print "Number of GCSE physics lessons in tracker: {0}".format(len(gcseLessons))
print "Number of GCSE physics lessons in database: {0}".format(numberOfPhysicsLessons(cursor))

names = physicsLessonsNames(cursor)

print [x for x in names if x not in gcseLessons]
print [x for x in gcseLessons if x not in names]


rows = unlinkedPhysicsQuestions(cursor)
rows = [r for r in rows if r[1] in gcseWorksheets]

writeListAsCSV(rows, "uq.csv")

print tabulate(rows)

print "Number of unlinked questions: {0}".format( len(rows))


cursor.execute("DELETE FROM lessons")

for row in phases:
    sql = "INSERT INTO lessons VALUES ({0}, '{1}', {2}, '{3}', '{4}', '{5}')".format(row[0], re.sub(r"[']", "''", row[1]), row[2], re.sub(r"[']", "''",  row[3]), re.sub(r"[']", "''", row[4]), re.sub(r"[']", "''", row[5]))
    cursor.execute(sql)


cursor.execute("SELECT COUNT(qcd.QuestionId), qcd.WorksheetName FROM qcd LEFT OUTER JOIN llqpq ON qcd.QuestionId = llqpq.QuestionId WHERE llqpq.LessonId IS NULL AND qcd.Subject = 'Physics' GROUP BY qcd.WorksheetName")

unlinked = cursor.fetchall()

unlinked = [x for x in unlinked if x[1] in gcseWorksheets]

print tabulate(unlinked)

cursor.execute("SELECT lie.LessonID, lie.LessonTitle, lie.LessonQuestions, lessons.NumberOfQuestions, (lessons.NumberOfQuestions - lie.LessonQuestions) AS Difference, lessons.WorksheetName1, lessons.WorksheetName2, lessons.WorksheetName3 FROM lie LEFT JOIN lessons on lie.LessonID = lessons.LessonID WHERE lie.Subject = 'Physics' AND lie.gvalue < 11 AND lie.Live = 'True' ORDER BY lie.LessonTitle")

lessonStats = cursor.fetchall()
lessonStats2 = []

for s in lessonStats:
    a = 0

    if s[5] in [x[1] for x in unlinked]:
        a +=[x[0] for x in unlinked if x[1] == s[5]][0]

    if s[6] in [x[1] for x in unlinked]:
        a +=[x[0] for x in unlinked if x[1] == s[6]][0]
    
    if s[7] in [x[1] for x in unlinked]:
        a +=[x[0] for x in unlinked if x[1] == s[7]][0]

    lessonStats2.append( list( s[0:5]) + [a])

print tabulate(lessonStats2)

connection.close()