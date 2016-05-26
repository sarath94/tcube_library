from whoosh.index import create_in,open_dir
from whoosh.fields import *
import os

from whoosh.qparser import QueryParser
def search(query):
	ix = open_dir("work/indexdir")
	with ix.searcher() as searcher:
		query = QueryParser("content", ix.schema).parse(query)
		results = searcher.search(query)
		result_list = []	
		for result in results:
			result_list.append([result['title'],result['url']])
	return result_list
#search(query="sarath")
