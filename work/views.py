from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.views.decorators.cache import cache_control
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from .models import Admin, Course, Discipline, File, Keyword, TempKeyword
from . import b
from multiprocessing import Process
import subprocess
import md5,os

def test(request):
    return render(request, 'test5.html', {})

def convert_video(name):
    file_name, file_extension = os.path.splitext(name)
    os.system("https_proxy='https://nareshk16:nareshk16*@proxy.cse.iitb.ac.in:80' http_proxy='http://nareshk16:nareshk16*@proxy.cse.iitb.ac.in:80' ftp='ftp://nareshk16:nareshk16*@proxy.cse.iitb.ac.in:80' socks='socks://nareshk16:nareshk16*@proxy.cse.iitb.ac.in:80' autosub work/static/files/"+name)
    os.system("mv work/static/files/"+file_name+".srt work/static/txt/")
    #print "sudo mv work/static/files/"+file_name+".srt work/static/files/text"
    print "done"

def convert_pdf(name):
    file_name, file_extension = os.path.splitext(name)
    os.system("pdftotext -layout work/static/files/"+name)
    os.system("sudo mv work/static/files/"+file_name+".txt work/static/txt/")
    print "done"

def convert_ppt(name):
    file_name, file_extension = os.path.splitext(name)
    os.system("libreoffice --headless --convert-to pdf --outdir work/static/txt/ work/static/files/"+name)
    os.system("pdftotext -layout work/static/txt/"+file_name+".pdf")
    os.system("mv work/static/txt/"+file_name+".txt work/static/txt/")
    os.system("rm work/static/txt/"+file_name+".pdf")
    print "done"

def search(request):
#    print request.GET.get('query','')
    results = b.search(request.GET.get('query',''))
#    print results
    return render(request, 'test5.html', {'results':results,'query':True})

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
        	file_list = File.objects.raw('select course.course_id,course.course_name,file.file_id,file.file_name,file.file_type from course,file where course.course_id=file.course_id_fk')
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
		upfile = request.FILES['datafile'].name
		filedb=File()
		filedb.file_type=request.POST['file_type']
		filedb.actual_path=request.FILES['datafile']
		filedb.txt_path='fhvg'
		filedb.file_name=request.FILES['datafile'].name
		filedb.course_id_fk=Course.objects.get(course_name=request.POST['course'])
		try:
			filedb.save()
			name=request.FILES['datafile'].name
			if request.POST['file_type']=='video':
                		p = Process(target=convert_video,args=(name,))
                		p.start()
            		if request.POST['file_type']=='ppt':
                		p=Process(target=convert_ppt,args=(name,))
                		p.start()
            		if request.POST['file_type']=='pdf':
                		p=Process(target=convert_pdf,args=(name,))
                		p.start();
			file_obj = File.objects.raw("SELECT file_id from file where file_name='%s'" %request.FILES['datafile'].name)
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
