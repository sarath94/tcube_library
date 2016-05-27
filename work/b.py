from whoosh.index import create_in,open_dir
from whoosh.fields import *
from .models import File
import os

from whoosh.qparser import QueryParser
def search(query):
	ix = open_dir("work/static/indexdir")
	with ix.searcher() as searcher:
		query = QueryParser("content", ix.schema).parse(query)
		results = searcher.search(query)
		result_list = []
		for result in results:
#			print result['title']
			file_obj = File.objects.raw('SELECT file_id,file_name from `file` where txt_path="'+result['title']+'"')
			for obj in file_obj:
	    			result_list.append(obj.file_name)
	return result_list
#search(query="sarath")
