from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.views.decorators.cache import cache_control
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from .models import Admin, Course, Discipline, File, Keyword, TempKeyword
from . import a,b,c
from multiprocessing import Process
import subprocess
import md5,os
from django.utils.html import strip_tags

def test(request):
    return render(request, 'advanced_search.html', {})

def convert_video(name):
    file_name, file_extension = os.path.splitext(name)
    os.system("https_proxy='https://nareshk16:nareshk16*@proxy.cse.iitb.ac.in:80' http_proxy='http://nareshk16:nareshk16*@proxy.cse.iitb.ac.in:80' ftp='ftp://nareshk16:nareshk16*@proxy.cse.iitb.ac.in:80' socks='socks://nareshk16:nareshk16*@proxy.cse.iitb.ac.in:80' autosub work/static/files/"+name)
    os.system("mv work/static/files/"+file_name+".srt work/static/txt/")
    a.update_index(file_name+".srt")
    print "done"

def convert_pdf(name):
    file_name, file_extension = os.path.splitext(name)
    os.system("pdftotext -enc UTF-8 -layout work/static/files/"+name)
    os.system("sudo mv work/static/files/"+file_name+".txt work/static/txt/")
    a.update_index(file_name+".txt")
    print "done"

def convert_ppt(name):
    file_name, file_extension = os.path.splitext(name)
    os.system("libreoffice --headless --convert-to pdf --outdir work/static/txt/ work/static/files/"+name)
    os.system("pdftotext -enc UTF-8 -layout work/static/txt/"+file_name+".pdf")
    os.system("mv work/static/txt/"+file_name+".txt work/static/txt/")
    os.system("rm work/static/txt/"+file_name+".pdf")
    a.update_index(file_name+".txt")
    print "done"

def file_txt_convert(file_path,file_txt):
    file_txt = file_txt.replace("<div>","\n")
    file_txt = strip_tags(file_txt)
    file_txt = file_txt.replace("&gt;",">")
    file_obj = open(file_path,"w")
    file_obj.write(file_txt)
    file_obj.close()
    print "done"

def basic_search(request):
    results = {}
    queryRequest = False
    empty = False
    query = request.POST.get('query','')
    if(len(query)!=0):
        queryRequest = True
        results = File.objects.raw("SELECT file.file_id,file.file_name,keyword.keyword from file,keyword where file.file_id=keyword.file_id_fk and keyword.keyword='%s'" %query)
        if(len(list(results))==0):
            empty = True
    return render(request, 'basic_search.html', {'results':results,'query':queryRequest,'input':query,'empty':empty})

def advanced_search(request):
    results_data = {}
    count = 0
    queryRequest = False
    query = request.GET.get('query','')
    pagenum = int(request.GET.get('page','1'))
    result_list = []
    page_data = []
    if(len(query)!=0):
        queryRequest = True
        results_data = b.search(query,pagenum)
        result_list = results_data['result_list']
        page_data = results_data['page_data']
    return render(request, 'advanced_search.html', {'page_data':page_data,'result_list':result_list,'queryRequest':queryRequest,'query':query})

def test_search(request):
    results_data = {}
    count = 0
    queryRequest = False
    query = request.GET.get('query','')
    pagenum = int(request.GET.get('page','1'))
    result_list = []
    page_data = []
    if(len(query)!=0):
        queryRequest = True
        results_data = c.search(query,pagenum)
        result_list = results_data['result_list']
        page_data = results_data['page_data']
    return render(request, 'test_search.html', {'page_data':page_data,'result_list':result_list,'queryRequest':queryRequest,'query':query})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
	if request.session.has_key('admin_id'):
		return redirect("/work/admin_page/")
	else:
		c = {}
		c.update((csrf(request)))
		return render_to_response("log in.html", c)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_page(request):
	if request.session.has_key('admin_id'):
		admin_id = request.session['admin_id']
		course_list=Course.objects.raw("Select course_id,course_name from course")
		discipline_list=Discipline.objects.all()
        	file_list = File.objects.raw('select course.course_id,course.course_name,file.file_id,file.file_name,file.file_type from course,file where course.course_id=file.course_id_fk and file_type="video"')
		keyword_list = File.objects.raw('SELECT file_id,file_name,keyword from `file`,(SELECT * FROM `temp_keyword`) as keytable where file.file_id=keytable.file_id_fk')

		data = {'admin_id':admin_id, 'course_list':course_list,'discipline_list':discipline_list,'keyword_list':keyword_list,'file_list':file_list}
		data.update((csrf(request)))
		return render_to_response("admin_page.html", data)
	else:
		return redirect("/work/admin_login/")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def auth_admin(request):
	if request.method == "POST":
		admin_id = request.POST['admin_id']
		admin_password = request.POST['admin_password']
		admin_password = md5.new(admin_password).hexdigest()
		user = Admin.objects.filter(admin_id=admin_id, admin_password=admin_password)
		if len(user)==0:
			msg = {'msg':'ID or password incorrect'}
			msg.update((csrf(request)))
			return render_to_response('log in.html', msg)
		user = Admin.objects.filter(admin_id=admin_id, admin_password=admin_password).first()
		request.session['admin_id']=admin_id
		return redirect("/work/admin_page/")
	else:
		return redirect("/work/admin_login/")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_logout(request):
	try:
		del request.session['admin_id']
	except Exception,e:
        	print str(e)
	return redirect("/work/admin_login/")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def upload_file(request):
	if request.session.has_key('admin_id'):
	        name = (request.FILES['datafile'].name).replace(" ","_")
	        name = name.replace("(",'')
	        name = name.replace(")",'')
	        file_name, file_extension = os.path.splitext(name)
		filedb=File()
		filedb.file_type=request.POST['file_type']
		filedb.actual_path=request.FILES['datafile']
        	if(request.POST['file_type']=='video'):
            		filedb.txt_path=file_name+".srt"
        	else:
            		filedb.txt_path=file_name+'.txt'
		filedb.file_name=name
		filedb.course_id_fk=Course.objects.get(course_name=request.POST['course'])
		try:
			filedb.save()
			if request.POST['file_type']=='video':
                		p = Process(target=convert_video,args=(name,))
                		p.start()
            		if request.POST['file_type']=='ppt':
                		p=Process(target=convert_ppt,args=(name,))
                		p.start()
            		if request.POST['file_type']=='pdf':
                		p=Process(target=convert_pdf,args=(name,))
                		p.start();
			file_obj = File.objects.raw("SELECT file_id from file where file_name='%s'" %name)
			if(len(request.POST['keywords']) != 0):
				keyword_list = request.POST['keywords']
		                keyword_list = keyword_list.split(',')
				for keyword in keyword_list:
					if(len(keyword) != 0):
						keyworddb = Keyword()
						keyworddb.file_id_fk = file_obj[0]
						keyworddb.keyword = keyword
						keyworddb.save()
			return HttpResponse("true")
		except Exception,e:
			print str(e)
			return HttpResponse("false")
	else:
		return redirect("/work/admin_login/")

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_course(request):
    if request.session.has_key('admin_id'):
        course_name = request.POST['course_type']
        course = Course()
        course.course_name = request.POST['course_name']
        course.type_of_course = request.POST['course_type']
        course.discipline = Discipline.objects.get(discipline = request.POST['discipline'])
        try:
            course.save()
            return HttpResponse("true")
        except Exception,e:
            print str(e)
            return HttpResponse("false")
    else:
        return redirect("/work/admin_login/")

def add_keyword(request):
    if request.session.has_key('admin_id'):
        keyworddb = Keyword()
        keyworddb.keyword = request.GET['keyword']
        keyworddb.file_id_fk = File.objects.get(file_id=request.GET['file_id_fk'])
        if(request.GET['add']=="true"):
            keyworddb.save()
        TempKeyword.objects.filter(keyword=request.GET['keyword'],file_id_fk=request.GET['file_id_fk']).delete()
        return HttpResponse("true")
    else:
        return HttpResponse("false")

def review_content(request):
	file_id = request.POST['file_id']
	file_obj=File.objects.get(file_id=file_id)

	file_name=file_obj.file_name
	file_text = []
    	with open("work/static/txt/"+file_obj.txt_path) as file:
        	file_text = file.readlines()
	data = {}
    	data['file_name'] = file_name
    	data['file_text'] = file_text
        data['file_txt'] = "work/static/txt/"+file_obj.txt_path
        data.update((csrf(request)))

	return render_to_response("admin_review.html", data)

def save_reviewed(request):
    text=request.POST['text']
    file_txt=request.POST['file_txt']
    p=Process(target=file_txt_convert,args=(file_txt,text))
    p.start();
    return redirect("/work/admin_page/")
