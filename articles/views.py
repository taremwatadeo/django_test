from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.core import serializers
from django.template import Context
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import json
from freestyle_module_1 import *
from freestyle_module_2 import *
from models import *
import roundabout


data=[]
full_dict =  dict()
result_dict = dict()
final_dict=dict()
json_str = ""
json_dict = ""


def getPlaces(data):
	global full_dict
	global result_dict
	#print full_dict
	for i in data:
		if(i in full_dict.keys()):
			result_dict[i] = full_dict[i]
			
			
@csrf_exempt
def Feature2(request):
	if request.method=="POST":
		l = request.body.split("::")
		location = l[0]
		radius = l[1][0:-2]
		json_places = roundabout.feature2(location,int(radius)*1000)
		print json_places
		return HttpResponse(json.dumps(json_places))
	
@csrf_exempt
def Feature1_Module2(request):
 	global final_dict
 	global json_dict
 	global result_dict
 	if request.method=="GET":
 	    print '--------------------GET--------------------'
 	    json_dict =json.dumps(final_dict,sort_keys=True,indent=4,separators=(',',': ')) 
 	    print '--------------------GET--------------------'
 	    print '\n\n'
 	    return HttpResponse('{ "route" :['+  json_dict+ "\n]}") #Back to front end
 	else:
 	    print '--------------------POST--------------------'
 	    data =  request.body[1:-1].split(",")
 	    #data = [x.strip(' ') for x in data]
 	    #print data
 	    getPlaces(data[2:])
 	    #print result_dict
 	    final_dict = run(data[0],data[1],result_dict)  #Goes into Feature1_Module2
 	    print '--------------------POST--------------------'
 	    print '\n\n'
 	    return HttpResponse(data)

@csrf_exempt	
def Feature1_Module1(request):
	global full_dict
	global json_str
	if request.method=="GET":
		print '--------------------GET--------------------'
		print '--------------------GET--------------------'
		print '\n\n'
		return HttpResponse(json_str) #Back to front end
	else:
		print '--------------------POST--------------------'
		data =  request.body.split("::")
		print data[0],'\n',data[1]
		#print full_dict
		full_dict = get_points_of_interest(data[0],data[1]) #Goes into Feature1_Module1
		json_str = json.dumps(full_dict,sort_keys=True,indent=4,separators=(',',': '))
		print '--------------------POST--------------------'
		print '\n\n'
		return HttpResponse("Success")
		
def Feature3_create_new_user(request):
	if request.method=="POST":
		name, age, phone_numbsser, date_creation, photo_url = request.body.split("::")
		create_new_user(name,int(age), phone_number, date_creation, photo_url)		
		return HttpResponse("Success")
		
def Feature3_create_new_group(request):
	if request.method=="POST":
		name, destination, date_creation = request.body.split("::")
		g_id = create_new_group(name, destination, date_creation)
		return HttpResponse(g_id)
		
def Feature3_add_members_to_group(request):
	if request.method=="POST":
		g_id, phone_number_list = request.body.split("::")		
		invalid_phone_numbers = add_members_to_group(int(g_id), phone_number_list)
		return HttpResponse(invalid_phone_numbers)

def Feature3_make_admin(request):
	if request.method=="POST":
		g_id, phone_number = request.body.split("::")
		make_admin(int(g_id), phone_number)
		return HttpResponse("Success")
		
def Feature3_send_message_to_group(request):
	if request.method=="POST":
		phone_number, g_id, video_url, photo_url, text = request.body.split("::")				
		send_message_to_group(phone_number, int(g_id), video_url, photo_url, text)		 
		return HttpResponse("Success")
		
def Feature3_get_member_coordinates(request):
	if request.method=="POST":
		g_id = request.body				
		L = get_member_coordinates(int(g_id))		 
		return HttpResponse(L)

def Feature3_is_user_in_group(request):
	if request.method=="POST":
		phone_number = request.body				
		status = is_user_in_group(phone_number)	 
		return HttpResponse(status)
	
	
def Feature3_delete_group(request):
	if request.method=="POST":
		phone_number = request.body				
		delete_group(phone_number)	 
		return HttpResponse("Success")	
		
def Feature3_update_user_location(request):
	if request.method=="POST":
		phone_number, latitude, longitude = request.body.split("::")						
		update_user_location(phone_number, float(latitude), float(longitude))
		return HttpResponse("Success")



		
