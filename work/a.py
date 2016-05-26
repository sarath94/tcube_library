from whoosh.index import create_in,open_dir
from whoosh.fields import *
import os
def create_index():
	schema = Schema(title=TEXT(stored=True,unique=True),content=TEXT)
	ix = create_in("indexdir", schema)
	writer = ix.writer()
	for root, dirs, files in os.walk("work/static/txt/"):
		path = root.split('/')
		for tfile in files:
			#if not (tfile.endswith('.txt') or tfile.endswith('.srt')):
			#	continue
			#	print(tfile)
			print "Indexing: ", os.path.join(os.path.abspath(root),tfile)
			title = tfile
			content = open(os.path.join(os.path.abspath(root),tfile),'r').read()
			content = content.decode("utf-8", "replace")
			writer.add_document(title=unicode(title,'utf-8'),url=unicode(url,'utf-8'),content=unicode(content))
			print "Done: ", tfile

	writer.commit()
#create_index()
def update_index(filepath):
	ix = open_dir("indexdir")
	writer = ix.writer()
	root = "work/static/txt/"
	print "Indexing: ", os.path.join(os.path.abspath(root),filepath)
	title = filepath
	url = filepath
	content = open(os.path.join(os.path.abspath(root),filepath),'r').read()
	content = content.decode("utf-8", "replace")
	writer.add_document(title=unicode(title,'utf-8'),url=unicode(url,'utf-8'),content=unicode(content))
	print "Done: ", filepath
	writer.commit()
#update_index('sarat')
