from whoosh.index import create_in,open_dir
from whoosh.fields import *
import os
import codecs

def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))

def create_index():
	schema = Schema(title=ID(unique=True,stored=True),content=TEXT)
	ix = create_in("./static/indexdir", schema)
	writer = ix.writer()
	for root, dirs, files in os.walk("./static/txt/"):
		path = root.split('/')
		for tfile in files:
			#if not (tfile.endswith('.txt') or tfile.endswith('.srt')):
			#	continue
			#	print(tfile)
			print "Indexing: ", os.path.join(os.path.abspath(root),tfile)
			title = tfile
			with codecs.open(os.path.join(os.path.abspath(root),filepath), "r","utf-8") as f:
	   			content = f.read()
			writer.add_document(title=title,content=content)
			print "Done: ", tfile

	writer.commit()
#create_index()
def update_index(filepath):
	ix = open_dir("work/static/indexdir")
	writer = ix.writer()
	root = "work/static/txt/"
	print "Indexing: ", os.path.join(os.path.abspath(root),filepath)
	title = filepath
	with codecs.open(os.path.join(os.path.abspath(root),filepath), "r","utf-8") as f:
   		content = f.read()
	writer.add_document(title=title,content=content)
	print "Done: ", filepath
	writer.commit()
#update_index('sarat')
