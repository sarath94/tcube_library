from django.contrib import admin

# Register your models here.
from .models import Course, Discipline, File , Keyword, Admin, TempKeyword

admin.site.register(Course)
admin.site.register(File)
admin.site.register(Discipline)
admin.site.register(Keyword)
admin.site.register(TempKeyword)
admin.site.register(Admin)
