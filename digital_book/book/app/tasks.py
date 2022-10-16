from __future__ import absolute_import,unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from . models import shop_admin,shop,customer,customer_history
from datetime import datetime,timedelta
import os
from django.core.mail import send_mail
from .models import shop_admin,customer_history,customer,shop
import time
@shared_task
def track():
	c = customer_history.objects.filter(purchase_mode=False,msg=False)
	print(c)
	t = datetime.now()
	for i in c:
		if(str((t.date())) == str(i.duedate.date())):
			c = customer.objects.filter(customer_id=i.customer_id).first()
			print(c)
			email = c.email
			print(email)
			send_email.delay(email,i.purchase_item,i.purchase_date,i.shop_name)
			i.msg = True
			i.save()


@shared_task
def send_email(name,item_name,date,shop):
	date = str(date).split('T')
	send_mail(
			f'{shop} shop',
			f'please pay your due for purchase of {item_name} on {date[0]} from {shop} shop',
			settings.EMAIL_HOST,
			[name]
		)


while(True):
	track.delay()
	time.sleep(86400)