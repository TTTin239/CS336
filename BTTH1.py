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
import string

lucene.initVM()
directory = RAMDirectory()
analyzer = StandardAnalyzer()
cf = IndexWriterConfig(analyzer)
cf.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
writer = IndexWriter(directory, cf)

doc = Document()
tua = StringField('tua', 'Modern Computer Architecture', Field.Store.YES)
tacgia = TextField('tacgia', 'James Harrison', Field.Store.YES)
noidung = TextField('noidung', 'computer architecture, modern RAM, CPU speed, hard drive capacity, easy to use.', Field.Store.NO)
doc.add(tua)
doc.add(tacgia)
doc.add(noidung)
writer.addDocument(doc)

doc = Document()
tua = StringField('tua', 'Fashion in Use', Field.Store.YES)
tacgia = TextField('tacgia', 'James Smith', Field.Store.YES)
noidung = TextField('noidung', 'white shirt, hard hat, modern hair styles, easy to work', Field.Store.NO)
doc.add(tua)
doc.add(tacgia)
doc.add(noidung)
writer.addDocument(doc)

doc = Document()
tua = StringField('tua', 'Safety in Transportation', Field.Store.YES)
tacgia = TextField('tacgia', 'Smith Johnson', Field.Store.YES)
noidung = TextField('noidung', 'drunk driver, high speed vehicle architectures, carelessly drive, modern designed cars, smith', Field.Store.NO)
doc.add(tua)
doc.add(tacgia)
doc.add(noidung)
writer.addDocument(doc)
writer.close()
	     
reader = DirectoryReader.open(directory)
searcher = IndexSearcher(reader)
parser = QueryParser('noidung', analyzer)
query = parser.parse('speed')
doclist = searcher.search(query, 3)
docs = doclist.scoreDocs
count = 0
print(len(docs))
for item in docs:
    print(item)

for i in docs:
    doc = searcher.doc(i.doc)
    print(doc.get('tua'), doc.get('tacgia'), i.score)
for j in docs:
    if j.doc == 2:
        count = count + 1
print(count)
