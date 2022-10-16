from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import shop_admin,shop,customer,customer_history
from django.contrib.auth.forms import UserCreationForm  
# Create your views here.
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import datetime,timedelta
from django.contrib.auth.decorators import login_required
#from django.contrib import messages


@login_required
def adminview(request):
	user=request.user
	sh=shop_admin.objects.filter(user=user).first()
	shops=sh.shop_id
	l=[]
	cus = customer_history.objects.filter(shop_id=shops)
	for i in cus:
		print(i)
		if str(i) not in str(l):
			l.append(i)
	return render(request,'app/vac.html',{'c':l})

def viewdept(request):
	user=request.user
	sh=shop_admin.objects.filter(user=user).first()
	shops=sh.shop_name
	l=[]
	cus = customer_history.objects.filter(shop_name=shops,purchase_mode=False)
	for i in cus:
		if(i.duedate==None):
			pass
		else:
			if str(i) not in str(l):
				l.append(i)
	return render(request,'app/debt.html',{'c':l})

def viewpaid(request):
	user=request.user
	sh=shop_admin.objects.filter(user=user).first()
	shops=sh.shop_name
	l=[]
	cus = customer_history.objects.filter(shop_name=shops,purchase_mode=True)
	for i in cus:
		if(i.duedate==None):
			if str(i) not in str(l):
				l.append(i)
			
	return render(request,'app/paid.html',{'c':l})



@login_required
def customer_view(request):
	try:
		user = request.user
		cu = customer.objects.filter(name=user.username).first()
		ch = customer_history.objects.filter(customer_id=cu.customer_id)
		return render(request,'app/customerview.html',{'c':ch})
	except:
		return redirect('login')

@login_required
def customer_details(request,cid):
	c = customer_history.objects.filter(customer_id=cid,shop_name=request.user.shop_admin.shop_name)
	print(c)
	return render(request,'app/purchase.html',{'c':c})

@login_required
def customer_debt_details(request,cid):
	if request.method == 'POST':
		cid = request.POST['cid']
		cusid   = cid.split(',')[0]
		user = request.user.username
		shop_id = shop_admin.objects.filter(name=user).first().shop_name 
		ch = customer_history.objects.filter(customer_id=cusid,shop_name=shop_id,id=cid.split(',')[1]).first()
		ch.duedate=None
		ch.purchase_mode=True
		ch.save()
	c = customer_history.objects.filter(customer_id=cid,shop_name=request.user.shop_admin.shop_name,purchase_mode=False)
	return render(request,'app/debtpurchase.html',{'c':c})	

@login_required
def customer_paid_details(request,cid):
	c = customer_history.objects.filter(customer_id=cid,shop_name=request.user.shop_admin.shop_name,purchase_mode=True)
	return render(request,'app/purchase.html',{'c':c})	


def adminregister(request):
    if request.method == 'POST':
    	d= {
	    			'name':request.POST['username'],
	    			'email':request.POST['email'],
	    			'phone':request.POST['phone'],
	    			'p1':request.POST['p1'],
	    			'p2':request.POST['p2'],
	    			'shop':request.POST['shop'],
	    }
    	if(User.objects.filter(username=request.POST['username']).exists()):
    		messages.error(request,f'username already exist')
    		d['username'] = ''
    		return render(request,"app/admin.html",{'i':d})
    	elif(User.objects.filter(email=request.POST['email']).exists()):
    		messages.error(request,f'email already exist')
    		d['email']=''
    		return render(request,"app/admin.html",{'i':d})
    	elif shop_admin.objects.filter(phone = request.POST['phone']).exists() or customer.objects.filter(phone = request.POST['phone']) :
    		messages.error(request,f'phone number already exist')
    		d['phone'] = ''
    		return render(request,"app/admin.html",{'i':d})
    	else:
    		if(request.POST['p1'] == request.POST['p2']):
	    		d= {
	    			'name':request.POST['username'],
	    			'email':request.POST['email'],
	    			'phone':request.POST['phone'],
	    			'p1':request.POST['p1'],
	    			'p2':request.POST['p2'],
	    			'shop':request.POST['shop'],
	    			}
	    		x =datetime.now()
	    		s = str(x).split(' ')
	    		sid=""
	    		for i in str(s[0]).split('-'):
	    			sid+=i
	    		for i in (s[1].split(':'))[0:2]:
	    			sid+=i
	    		User.objects.create_user(username=d['name'],email=d['email'],password=d['p1'])
	    		user = User.objects.filter(username=d['name']).first()
	    		shop_admin.objects.create(user=user,email=d['email'],name=user.username,phone=d['phone'],shop_name=d['shop'],shop_id=sid)
	    		messages.success(request,f'Account created for {user.username}')
	    		return redirect('login')
	    	else:
	    		messages.error(request,f'passwor doesnot match ')	
	    		return render(request,"app/customer.html")

    return render(request,"app/admin.html")


def customerregister(request):
	if request.method == 'POST':
		d= {
	    	'name':request.POST['username'],
	    	'email':request.POST['email'],
	    	'phone':request.POST['phone'],
	    	'p1':request.POST['p1'],
	    	'p2':request.POST['p2'],
	    }
		if(User.objects.filter(username=request.POST['username']).exists()):
			messages.error(request,f'username already exist')
			return render(request,"app/customer.html",{'i':d})
		elif(User.objects.filter(email=request.POST['email']).exists()):
			messages.error(request,f'email already exist')
			return render(request,"app/customer.html",{'i':d})
		elif customer.objects.filter(phone = request.POST['phone']).exists() or shop_admin.objects.filter(phone = request.POST['phone']):
			messages.error(request,f'phone number already exist')
			return render(request,"app/customer.html",{'i':d})
		else:
			if(request.POST['p1'] == request.POST['p2']):
				User.objects.create_user(username=d['name'],email=d['email'],password=d['p1'])
				user = User.objects.filter(username=d['name']).first()
				customer.objects.create(user=user,email=d['email'],name=user.username,phone=d['phone'],customer_id=d['phone'])
				messages.success(request,f'Account created for {user.username}')
				return redirect('login')
			else:
				messages.error(request,f'passwor doesnot match ')	
				return render(request,"app/customer.html",{'i':d})
	return render(request,"app/customer.html")


def loginuser(request):
	if request.method == 'POST':
		uname = request.POST['username']
		upass = request.POST['password']
		 
		user = authenticate(request,username=uname,password=upass)
		if user is not None:
			request.session['username'] = uname
			login(request,user)
			if(customer.objects.filter(name = request.user.username).exists()):
				return redirect('customerindex')
			else:
				return redirect('adminindex')
		else:
			messages.error(request, 'invalid username or password')
			return render(request,'app/login.html')
	return render(request,'app/login.html')

def home(request):
	return render(request,'app/index.html')

def addshop(request):
	if request.method == 'POST':
		try:
			user = request.user
			cid = customer.objects.filter(name=user.username).first().customer_id
			shop_id = request.POST['shop']
			if(shop_admin.objects.filter(shop_id=shop_id).exists()):
				sid = shop_admin.objects.filter(shop_id=shop_id).first()
				sid = sid.shop_name
				shop.objects.create(shop_name=sid,shop_id=shop_id,customer_id=cid)
				messages.success(request,'Shop Added')
				return redirect('customerindex') 
			else:
				messages.error(request, 'invalid Shop ID')
				return render(request,'app/addshop.html')
		except:
			return redirect('login')
	return render(request,'app/addshop.html')

def purchase(request):
	if request.method == 'POST':
		cid = request.POST['cid']
		item = request.POST['name']
		price = request.POST['price']
		qty = request.POST['qty']
		mode = request.POST['mode']
		due = request.POST['due']
		if(customer.objects.filter(customer_id=cid).exists()):
			cname = customer.objects.filter(customer_id=cid).first().name
			s= shop_admin.objects.filter(name=request.user.username).first()
			if(shop.objects.filter(customer_id=cid).exists()):
				if(mode=='True'):
					messages.success(request,'entry added')
					customer_history.objects.create(customer_name=cname,customer_id=cid,shop_name=s.shop_name,shop_id=s.shop_id,purchase_item=item,purchase_mode=mode,item_price=price)
				else:
					messages.success(request,'entry added')
					customer_history.objects.create(customer_name=cname,customer_id=cid,shop_name=s.shop_name,shop_id=s.shop_id,purchase_item=item,purchase_mode=mode,item_price=price,duedate=datetime.now()+timedelta(days=int(due)))
			else:
				messages.error(request,'Customer not added to shop')
				return render(request,'app/add.html')
		else:
			messages.error(request,'Inavlid Customer ID')
			return render(request,'app/add.html')
	return render(request,'app/add.html')


def customerindex(request):
	user = request.user.username
	i = customer.objects.filter(name=user).first().phone
	return render(request,'app/customerindex.html',{'name':user,'i':i})

def adminindex(request):
	user = request.user.username
	shopid = shop_admin.objects.filter(name=user).first().shop_id
	return render(request,'app/adminindex.html',{'name':user,'shopid':shopid})

def custom_logout(request):
    logout(request)
    return redirect("login")