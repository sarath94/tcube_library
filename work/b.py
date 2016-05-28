from whoosh.index import create_in,open_dir
from whoosh.fields import *
from work.models import File
import os
import codecs

from whoosh.qparser import QueryParser
def search(query,pagenum):
	ix = open_dir("work/static/indexdir")
	with ix.searcher() as searcher:
		query = QueryParser("content", ix.schema).parse(query)
		results = searcher.search_page(query,pagenum,pagelen=10)
		result_data = {}
		has_next = True
		has_previous = True
		if(pagenum < 2):
			has_previous = False
		if(pagenum >= results.pagecount):
			has_next = False
		result_data['page_data'] = {'pagenum':pagenum, 'pagecount':results.pagecount, 'resultnum':results.offset+1, 'resultcount':results.offset+results.pagelen, 'totalresult':results.total, 'has_previous':has_previous, 'has_next':has_next}
		result_list = []
		for result in results:
			filecontents = ""
			with codecs.open(os.path.join("work/static/txt/",result['title']), "r","utf-8") as f:
	   			    filecontents = f.read()
			file_obj = File.objects.raw('SELECT file_id,file_name from `file` where txt_path="'+result['title']+'"')
			for obj in file_obj:
	    			result_list.append([obj.file_name,result.highlights("content", text=filecontents, top=3)])
		result_data['result_list'] = result_list
	return result_data
#search(query="sarath")
