from articles.models import *
from django.core import serializers
from django.db import IntegrityError
from django.http import *
from django.shortcuts import render
from django.template import Context
from django.template import RequestContext
from django.template.loader import get_template
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from models import *
from random import randrange
from random import shuffle
from gen_diary import get_diary
from queries import (on_start_trip, on_finish_trip, 
        check_in, display_trip_details, view_trips, 
        check_if_trip_exists, insert_review, get_places)
import datetime
import freestyle
import json
import re
import roundabout
import functions

try:
    import urllib2
except:
    print("Run with python2")

@csrf_exempt
def homepage(request):
    now = datetime.datetime.now()
    html = """<!doctype html><html><body style="background-image:url('https://impythonist.files.wordpress.com/2015/06/1666323.png'); background-size:cover; background-repeat: no-repeat;"><h3>Welcome to EGM's backend Django server! <br><br>It is now %s. </h3> """  % now + """

<h4> Views for feature 1 (that should be implemented but haven't) <h4>
<pre>
@csrf_exempt
def freestyle_getroute(request):
    ''' Get source, destination, and some points of interest. Return an optimal route json for rendering at the front end '''
    exec("source  = request.%s['source']" %request.method)
    exec("dest    = request.%s['dest']" %request.method)
    exec("json_waypoints    = json.loads(request.%s['json_waypoints'])" %request.method)
    #json_waypoints = request.body
    optimal_route = freestyle.get_best_route(source, dest, json_waypoints)

    return HttpResponse(json.dumps(optimal_route, indent=4), content_type="application/json")

@csrf_exempt
def freestyle_getpoints(request):
    ''' Get source and destination from user, and return points of interest '''
    exec("source  = request.%s['source']" %request.method)
    exec("dest    = request.%s['dest']" %request.method)
def Feature2(request):
    if request.method == "POST":
        l = request.body.split("::")
        no_users = len(l) - 1
        if no_users > 2:
            location = l[0:1] + l[2:]
        else:
            location = l[0]
        radius = l[1][0:-2]
        json_places = roundabout.feature2(
            location, int(radius) * 1000, no_users)
        return HttpResponse(json.dumps(json_places))

@csrf_exempt
def Feature1_Module2(request):
    data = request.body[1:-1].split(",")
    final_dict = freestyle.get_best_route(
        data[0], data[1], data[2:])  # Goes into Feature1_Module2
    json_dict = json.dumps(final_dict, sort_keys=True,
                           indent=4, separators=(',', ': '))
    return HttpResponse('{ "route" :[' + json_dict + "\n]}")

    points_of_interest = freestyle.get_points_of_interest(source, dest)
    return HttpResponse(json.dumps(points_of_interest, indent=4))
    </pre>
</body></html>"""

    return HttpResponse(html)


@csrf_exempt
def Feature2(request):
    if request.method == "POST":
        l = request.body.split("::")
        print(request.body)
        no_users = len(l) - 1
        if no_users > 1:
            location = l[0:1] + l[2:]
        else:
            location = [l[0]]
        radius = l[1][0:-2]
        json_places = roundabout.feature2(
            location, int(radius) * 1000, no_users)
        print(json_places)
        return HttpResponse(json.dumps(json_places))

@csrf_exempt
def Feature1_Module2(request):
    data = request.body.split("::")
    #print(json.loads(data[2]))
    if(len(data)>2):
        final_dict = freestyle.get_best_route(data[0], data[1], json.loads(data[2]))  # Goes into Feature1_Module2
    else:
        print(request.body)
        final_dict = freestyle.get_best_route(data[0], data[1], None)

    src_coord = freestyle.get_geocoded_address(data[0])
    src_dict = {'lat':src_coord[0], 'lng':src_coord[1]};
    dst_coord = freestyle.get_geocoded_address(data[1])
    dst_dict = {'lat':dst_coord[0], 'lng':dst_coord[1]};

    json_dict = json.dumps({"src" : src_dict, "dst" : dst_dict, "route" : [final_dict]}, sort_keys=True,
                           indent=4, separators=(',', ': '))

    print("LENGTH: ", len(json_dict))

    return HttpResponse(json_dict)


@csrf_exempt
def Feature1_Module1(request):
    try:

        data = request.body.split("::")
        print data
        full_dict = freestyle.get_points_of_interest(
            data[0], data[1])  # Goes into Feature1_Module1
        json_str = json.dumps(full_dict, sort_keys=True,
                              indent=4, separators=(',', ': '))
        return HttpResponse(json_str)
    except:
        return HttpResponse("")


'''
Feature4 Views
'''

# input_dict={"Op":"7","phoneNumber":"hello","tripId":5,"placeName":"mumbai"}
# : was used for testing
import json
import re
try:
    import urllib2
except:
    print("Run with python2")


@csrf_exempt
def index(request):
    output_dict = {}
    print request.body
    if request.method == 'POST':
        input_dict = json.loads(request.body)
    op_code = input_dict["Op"]
    if op_code == "1":
        phone_number = input_dict["phNo"]

        trip_id = on_start_trip(phone_number)
        print trip_id
        output_dict["Op"] = op_code
        output_dict["trip_id"] = trip_id
        print output_dict
        return HttpResponse(json.dumps(output_dict))

    elif op_code == "2":
        place_name = input_dict["placeName"]
        trip_id = input_dict["tripId"]
        check_in(place_name, trip_id)
        output_dict["Op"] = op_code
        return HttpResponse(json.dumps(output_dict))

    elif op_code == "3":
        trip_id = input_dict["tripId"]
        d = {}
        d = display_trip_details(trip_id)
        # startTime=d["startTime"]
        count = d["count"]
        output_dict["Op"] = op_code
        # output_dict["startTime"]=startTime
        output_dict["count"] = count
        return HttpResponse(json.dumps(output_dict))

    elif op_code == "4":
        # gen diary
        phone_number = input_dict["phNo"]
        trip_id = input_dict["tripId"]
        on_finish_trip(trip_id, phone_number)
        # gen diary

        trip_id = input_dict["tripId"]
        places = get_places(trip_id)
        trip_review = get_diary(places)

        insert_review(trip_id, trip_review)
        output_dict["Op"] = op_code
        output_dict["review"] = trip_review
        # output_dict["places"]=places
        return HttpResponse(json.dumps(output_dict))

    elif op_code == "5":
        phone_number = input_dict["phNo"]
        d = {}
        d = view_trips(phone_number)
        output_dict["Op"] = op_code
        output_dict["Trips"] = d
        return HttpResponse(json.dumps(output_dict))

    elif op_code == "6":
        trip_id = input_dict["tripId"]
        phone_number = input_dict["phNo"]
        c = check_if_trip_exists(trip_id, phone_number)
        if c:
            d = {}
            d = display_trip_details(trip_id)
            # startTime=d["startTime"]
            count = d["count"]
            output_dict["Op"] = op_code
            # output_dict["startTime"]=startTime
            output_dict["count"] = count
            return HttpResponse(json.dumps(output_dict))
        else:
            output_dict["Op"] = op_code
            output_dict["count"] = -1
            return HttpResponse(json.dumps(output_dict))

    elif op_code == "7":
        # gen diary

        trip_id = input_dict["tripId"]
        places = get_places(trip_id)
        trip_review = get_diary(places)

        insert_review(trip_id, trip_review)
        output_dict["Op"] = op_code
        output_dict["review"] = trip_review
        # output_dict["places"]=places
        return HttpResponse(json.dumps(output_dict))


@csrf_exempt
def login(request):
    input_dict = json.loads(request.body)
    op = int(input_dict["op"])
    print input_dict
    if op == 0:
        name = input_dict["name"]
        pwd = input_dict["password"]
        phone = input_dict["phone"]
        regid = input_dict["regid"]
        try:
            functions.Feature3_create_new_user(name, phone, pwd,regid)
        except IntegrityError:
            return HttpResponse("User Already Exists")
        return HttpResponse("User created")

    elif op == 1:
        phone = input_dict["phone"]
        pwd = input_dict["password"]
        status = functions.sign_in(phone, pwd)

        if status == 1:
            n = User.objects.get(phone_number=phone)
            print "1::"+n.name+"::"+str(n.date_creation).split()[0]
            return HttpResponse("1::"+n.name+"::"+str(n.date_creation).split()[0])
        elif status == 2:
            return HttpResponse("2::User does not exist")
        elif status == 3:
            return HttpResponse("3::Incorrect password")
        elif status == 4:
            return HttpResponse("4::Already Logged In")
        else:
            return HttpResponse("Error")

    elif op == 2:
        phone = input_dict["phone"]
        try:
            response = functions.sign_out(phone)
            return HttpResponse(response)
        except:
            print("Unknown Error")
        return HttpResponse("Error")


@csrf_exempt
def chatroom(request):
	print "CHAT PLS"
	input_dict = json.loads(request.body)
	print input_dict
	phone = input_dict["phone"]
	message = input_dict["message"]
	functions.send_message(phone,message)
	return HttpResponse("Success")

@csrf_exempt
def group_activity(request):
    print request.body
    input_dict = json.loads(request.body)
    op = int(input_dict["op"])
    # 0 - create group
    # TODO -polling if already part of group in this intent
    # 1 - view members
    # 2 - group chat
    # 3 - exit group
    # 4 - check if group
    # 5 - map
    if op == 0:
        phone = input_dict["phone"];
        gname = input_dict["gname"]
        gdest = input_dict["gdest"]
        members = input_dict["members"][1:-1].split(",")
        #data = request.body[1:-1].split(",")
        group = Group.objects.create(name=gname, destination=gdest)
        user = User.objects.get(phone_number=phone)
        UserIsGroupMember.objects.create(g_id=group, phone_number=user)
        UserIsAdminGroup.objects.create(g_id=group, phone_number=user)
        for member in members:
            print member
            t = member
            t=(''.join(re.findall("[0-9]+", t))[-10:])
            user = User.objects.get(phone_number=t)
            print type(user)
            UserIsGroupMember.objects.create(g_id=group, phone_number=user)
        return HttpResponse("Success")
    if op == 4:
        print "came here"
        phone = input_dict["phone"]
        lat = input_dict["lat"]
        lng = input_dict["lng"]
        user = User.objects.get(phone_number=phone)
        json_response = {}
        try:
            member = UserIsGroupMember.objects.get(phone_number=user)
        except:
            json_response["status"] = 0
            print json_response
            return HttpResponse(json.dumps(json_response))
            
        if(member):
            member.latitude = lat
            member.longitude = lng
            member.save()
            group = member.g_id
            members = UserIsGroupMember.objects.filter(g_id=group)
            lats = []
            lngs = []
            for member in members:
                lats.append(member.latitude)
                lngs.append(member.longitude)
            json_response["dest"] = group.destination
            json_response["name"] = group.name
            json_response["lats"] = lats
            json_response["lngs"] = lngs
            json_response["status"] = 1
            return HttpResponse(json.dumps(json_response))
            ##TODO : Parse on Front End, Display Route to Destination, Add Available Markers(Check for 0.0)
            

    if op == 1:
        phone = input_dict["phone"]
        user = User.objects.get(phone_number=phone)
        g_id = UserIsGroupMember.objects.get(phone_number=user).g_id.g_id
        group = Group.objects.get(g_id=g_id)
        members = UserIsGroupMember.objects.filter(g_id=group)
        phones = []
        names = []
        for member in members:
            phones.append(member.phone_number.phone_number)
            names.append(member.phone_number.name)
        json_response = {}
        json_response["member_names"] = ";".join(names)
        json_response["member_phones"] = ";".join(phones)
        print json_response
        return HttpResponse(json.dumps(json_response))
    # if op==2:
    if op==5:
        phone = input_dict["phone"]
        lat = input_dict["lat"]
        lng = input_dict["lng"]
        phones = []
        names = []
        json_response={}
        user = User.objects.get(phone_number=phone)
        member = UserIsGroupMember.objects.get(phone_number=user)
        member.latitude = lat
        member.longitude = lng
        member.save()
        g_id = member.g_id.g_id
        group = Group.objects.get(g_id=g_id)
        members = UserIsGroupMember.objects.filter(g_id=group)
        lats=[];lngs=[]
        for member in members:
            lats.append(member.latitude)
            lngs.append(member.longitude)
            phones.append(member.phone_number.phone_number)
            names.append(member.phone_number.name)
        json_response["member_lats"]= ";".join(lats)
        json_response["member_lngs"]= ";".join(lngs)
        json_response["member_names"]= ";".join(names)
        return HttpResponse(json.dumps(json_response))
        #TODO : Parse and display markers on front end
            
        
        

    if op == 3:
        phone = input_dict["phone"]
        user = UserIsGroupMember.objects.get(phone_number=phone)
        user.delete()
        return HttpResponse("Success")
