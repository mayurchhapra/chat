from django.shortcuts import render
from .models import UserData as ud
from .models import Chat
from django.http import HttpResponse, Http404
import logging
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def login(request):
	return render(request,'login.html')

def register_redirect(request):
	save(request)
	return render(request,'register_redirect.html')


def register(request):
	context={}
	'''if 'name' in request.POST:
		context = {
		'name': request.POST['name'],
		'username':request.POST['username'],
		'address1':request.POST['address1'],
		'address2':request.POST['address2'],
		'gender':request.POST['gender'],
		'city':request.POST['city'],
		'state':request.POST['state'],
		'pincode':request.POST['pincode'],
		'email':request.POST['email'],
		'dob':request.POST['dob'],
		'contact':request.POST['contact'],
		'password':request.POST['password']
		}'''
	return render(request,'register.html',context)


def save(request):
	data = ud()
	if 'name' in request.POST:
		data.name = request.POST['name']
		data.username = request.POST['login']
		data.address1 = request.POST['address1']
		data.address2 = request.POST['address2']
		data.gender = request.POST['gender']
		data.city = request.POST['city']
		data.state = request.POST['state']
		data.pincode = request.POST['pincode']
		data.email = request.POST['email']
		data.dob = request.POST['dob']
		data.contact = request.POST['contact']
		data.password = request.POST['password']
		data.save()

def handle_exception(e):
    print(e)

def logout(request):
	file = "logout.html"
	if 'user' in request.session:
		del request.session['user']
		del request.session['id']
	else:
		file = "login.html"
	return render(request,file)

def after_login(request):
	context = {}
	file = 'after_login.html'
	username_from_form=""
	password_from_form=""
	user = ""

	try:
		if "username" in request.POST and "password" in request.POST:
			username_from_form = request.POST['username']
			password_from_form = request.POST['password']
		user = ud.objects.get(username = username_from_form,password = password_from_form)
	except Exception as e:
		handle_exception(e)

	if user:
		context={
		'id':user.id,
		'username': user.username,
		'password': user.password,
		}
		request.session['id'] = user.id
		request.session['user'] = user.username
	else:
		context={
		'username': "Not Found."
		}
		file = "login.html"


	return render(request,file,context)

def check_user(request):
	return render(request,"check_user.html")

def navigation(request):
	return render(request,"navigation.html")

def hackers(request):
	return render(request,"hackers.html")

def chat(request):
	obj_chat = Chat.objects.all()

	context={
		'data1': obj_chat
	}
	return render(request,'chat.html',context)

def chat_sender(request):
	obj_chat = Chat()
	chat = request.session['user']+'\n---------------------\n'+request.GET['chat']
	obj_chat.uid = request.session['id']
	obj_chat.chat = chat
	obj_chat.save()
	return render(request,'chat_sender.html')

def fetch(request):
	
	obj_chat = Chat.objects.all()

	context={
		'data1': obj_chat
	}
	return render(request,"fetch_chat.html",context)

#----------------------------- R & D -----------------------------

def check_login(request):

	if request.method == "GET":
		raise Http404("URL doesn't exists")
	else:
		response_data = {}
		login = request.POST["login"]
		user = None
		try:
			try:
				user = ud.objects.get(username = login)
			except ObjectDoesNotExist as e:
				pass
			except Exception as e:
				raise e
			if not user:
				response_data["is_success"] = True
			else:
				response_data["is_success"] = False
		except Exception as e:
			response_data["is_success"] = False
			response_data["msg"] = "Some error occurred. Please let Admin know."
	return JsonResponse(response_data)


def test(request):
	return render(request,"test_user.html",{})


