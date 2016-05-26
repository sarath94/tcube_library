from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^test/',views.test, name='test'),
    url(r'^search/',views.search, name='search'),

	url(r'^$', views.admin_page, name='admin_page_index'),
	url(r'^admin_login/', views.admin_login, name='admin_login'),
	url(r'^admin_page/', views.admin_page, name='admin_page'),
	url(r'^auth_admin/', views.auth_admin, name='auth_admin'),
	url(r'^admin_logout/', views.admin_logout, name='admin_logout'),
	url(r'^upload_file/', views.upload_file, name='upload_file'),
	url(r'^add_course/', views.add_course, name='add_course'),
	url(r'^add_keyword/', views.add_keyword, name='add_keyword'),
]
