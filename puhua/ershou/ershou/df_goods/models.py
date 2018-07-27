#coding=utf-8
from django.db import models
#from tinymce.models import HTMLField

class TypeInfo(models.Model):
	ttitle=models.CharField(max_length=20)
	isDelete=models.BooleanField(default=False)

	def  __str__(self):
		return self.ttitle

class GoodsInfo(models.Model):
	gtitle=models.CharField(max_length=50)
	gpic=models.ImageField(upload_to='goods')
	gprice=models.DecimalField(max_digits=10,decimal_places=2)
	isDelete=models.BooleanField(default=False)
	gunit=models.CharField(max_length=20,default='')
	gclick=models.IntegerField(default=1)
	gjianjie=models.CharField(max_length=200)
	gkucun=models.IntegerField(default=1)
	#gcontent=HTMLField()
	gtype=models.ForeignKey(TypeInfo)

	def  __str__(self):
		return self.gtitle
