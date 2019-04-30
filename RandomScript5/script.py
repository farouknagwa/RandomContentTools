from csvtools import *

rel = readCSVAsList("rel.csv")
ids = readCSVAsList("ids.csv")

print len(rel)
print len(ids)

ids = [r[0] for r in ids]

rel = [[getIdFromCSVText( r[0]), getIdFromCSVText( r[2])] for r in rel]


print len(rel)

mat = [r for r in rel if r[0] in ids]

app = []

for r in mat:
    if r not in app:
        app.append(r)

print len(app)

output = []

for r in ids:
    output.append([ [a for a in mat if a[0] == r][0][1]])

writeListAsCSV(output, "output.csv")
