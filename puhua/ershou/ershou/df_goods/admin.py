from django.contrib import admin

# Register your models here.
from . import models
class TypeInfoAdmin(admin.ModelAdmin):
	list_display = ['id','ttitle']


class GoodsInfoAdmin(admin.ModelAdmin):
	list_display = ['id','gtitle','gpic','gprice',
	        'isDelete','gunit','gclick','gjianjie',
	'gkucun','gtype']

admin.site.register(models.TypeInfo,TypeInfoAdmin)
admin.site.register(models.GoodsInfo,GoodsInfoAdmin)