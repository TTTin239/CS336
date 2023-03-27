import os
import lucene
from org.apache.lucene.store import RAMDirectory
from java.nio.file import Paths, Path
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.analysis.core import StopAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.index import IndexReader
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search import IndexSearcher, TopDocs
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.analysis.en import EnglishAnalyzer

lucene.initVM()
directory = RAMDirectory()
analyzer = StopAnalyzer()
cf = IndexWriterConfig(analyzer)
cf.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
writer = IndexWriter(directory, cf)

list1 = []
for i in range(1, 1401):
    f = open(f"C:\BTTH\CS336\Cranfield\{i}.txt", "r")
    temp = f.readline()
    list1.append(temp)
    f.close()

quer = []
with open("C:\BTTH\CS336\TEST\query.txt") as f1:
    lines = f1.readlines()
for i in range(len(lines)):
    lines[i] = lines[i].replace('\t', '')
    lines[i] = lines[i].replace('\n', '')
    quer.append(lines)

res = []
for x in range(1, 226):
    pathr = "C:/BTTH/CS336/TEST/RES/" + str(x) + ".txt"
    with open(pathr) as f1:
        lines1 = f1.readlines()
    for j in range(len(lines1)):   
        lines1[j] = lines1[j].split()
    res.append(lines1)

for i in range(0, 1400):
    doc = Document()
    tua = StringField('tua', str(i+1), Field.Store.YES)
    noidung = TextField('noidung', list1[i], Field.Store.NO)
    doc.add(tua)
    doc.add(noidung)
    writer.addDocument(doc)

writer.close()
	     
test = []
for m in range(len(res)):
    temp = []
    for n in range(len(res[m])):
        temp.append(res[m][n][1])
    test.append(temp)

reader = DirectoryReader.open(directory)
search = IndexSearcher(reader)
parser = QueryParser('noidung', analyzer)


anslist30 = []
for i in range(len(quer[0])):
    query = parser.parse(quer[0][i])
    doclist = search.search(query, 30)
    score = doclist.scoreDocs
    rpath = r'C:/BTTH/CS336/TEST/RES1' + str(i+1) + '.txt'

    with open(rpath, 'w') as res:
        ans = []
        for j in score:
            tmpdoc = search.doc(j.doc)
            ans.append(tmpdoc.get('tua'))
            tmpres = str(str(i+1) + ' ' + tmpdoc.get('tua')) + '\t' + str(round(j.score))
            res.write(tmpres)
        anslist30.append(ans)
    res.close

anslist5 = []
for i in range(len(quer[0])):
    query = parser.parse(quer[0][i])
    doclist = search.search(query, 5)
    docs = doclist.scoreDocs
    temper = []
    for item in docs:
        doc = search.doc(item.doc)
        temper.append(doc.get('tua'))
    anslist5.append(doc.get('tua'))


F1 = []
AP = []
for i in range(225):
    cnt = 0
    P_cnt = []
    for j in range(len(anslist30[i])):
        if anslist30[i][j] in test[i]:
            cnt = cnt + 1
            P_cnt.append(cnt/(j+1))
    if len(P_cnt) == 0:
        AP.append(0)
    else:
        AP.append(sum(P_cnt)/len(P_cnt))

    R = cnt/len(test[i])
    P = cnt/len(anslist30[i])
    if P+R == 0:
        F1.append(0)
    else:
        F1.append(round((2*P*R) / (P+R), 3))

Pa5  = []
for i in range(225):
    cnt = 0
    for j in range(len(anslist5[i])):
        if anslist5[i][j] in test[i]:
            cnt = cnt + 1
    Pa5.append(cnt/len(anslist5[i]))

MAP = sum(AP)/len(AP)
print("MAP của công cụ tìm kiếm: ", round(MAP,3))
#inp = int(input('Nhập số thứ tự câu truy vấn trong list TEST: '))

#print("F1 : ", F1[inp-1])
#print("P@5: ", Pa5[inp-1])
print('No.   ',' F1   ','P@5  ')

for i in range(225):
    if i < 9:
        print('',i+1, '  ',F1[i], ' ',Pa5[i])
    else:
        print(i+1, '  ',F1[i], ' ',Pa5[i])