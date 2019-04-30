from csvtools import *

q1 = readCSVAsList("lessons.csv")

q1 = q1[1:]

q1 = [[q[0], q[1], q[2], q[3]] for q in q1 if q[3] == "Physics"]

writeListAsCSV(q1, "physicslessons.csv")
