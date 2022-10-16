from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class shop_admin(models.Model):
	user = models.OneToOneField(User,default=None,on_delete=models.CASCADE)
	role =models.CharField(default='owner',max_length=5)
	phone = models.CharField(max_length=12,default=None)
	name = models.CharField(max_length=50)
	email = models.EmailField()
	shop_name = models.CharField(max_length=1000)
	shop_id = models.CharField(default=True,max_length=50,)
	
	def __str__(self):
		return self.name

class customer(models.Model):
	user = models.OneToOneField(User,default=None,on_delete=models.CASCADE)
	role =models.CharField(default='customer',max_length=8)
	name = models.CharField(max_length=50)
	email = models.EmailField()
	phone = models.CharField(max_length=12)
	customer_id = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class shop(models.Model):
	shop_name = models.CharField(max_length=1000)
	shop_id = models.IntegerField()
	customer_id = models.CharField(max_length=50)

	def __str__(self):
		return self.shop_name

class customer_history(models.Model):
	customer_id = models.CharField(default=None,max_length=12)
	customer_name = models.CharField(default=None,max_length=50)
	shop_name = models.CharField(max_length=1000)
	shop_id = models.IntegerField(default=None)
	purchase_item = models.CharField(max_length=1000)
	purchase_date = models.DateTimeField(default=timezone.now,null=True)
	item_price = models.IntegerField()
	purchase_mode = models.BooleanField(default=True)
	duedate = models.DateTimeField(default=None,null=True,blank=True)
	msg = models.BooleanField(default=False)
	def __str__(self):
		return str(self.customer_name)