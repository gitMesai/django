from django.contrib import admin

# Register your models here.
from . import models


class UserInfoAdmin(admin.ModelAdmin):
	list_display = ['id','uname','upwd','uemail','uphone']

admin.site.register(models.UserInfo,UserInfoAdmin)