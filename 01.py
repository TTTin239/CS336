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

for i in range(1, 256):
    f = open(f"{i}.txt", "r")
    temp = f.readline()
    list1.append(temp)
    f.close()

for i in range(0, 255):
    doc = Document()
    noidung = TextField('noidung', list1[i], Field.Store.NO)
    doc.add(noidung)
    writer.addDocument(doc)

writer.close()
	     
reader = DirectoryReader.open(directory)
searcher = IndexSearcher(reader)
parser = QueryParser('noidung', analyzer)
a = str("what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft")
query = parser.parse(a)
doclist = searcher.search(query, 30)
docs = doclist.scoreDocs
count = 0
print(len(docs))
for item in docs:
    if 0 <= item.doc <= 255:
        count = count + 1
    print(item)

dem = 0
a = 0
for i in docs:
    if a == 5:
        break;
    a = a + 1
    if 0 <= i.doc <= 255:
        dem = dem + 1

R = count / 30
P = count / len(docs)
F1 = (2*P*R) / (P+R)
print(f"F1 = {F1}")
print(f"P@5 = {dem/5}")