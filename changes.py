def group_activity(request):
	input_dict = json.loads(request.body)
	op = int(input_dict["op"])
	#0 - create group
	#1 - view members
	#2 - group chat
	#3 - exit group
	if op==0:
		gname = input_dict["gname"]
		gdest = input_dict["gdest"]
		group = Group.objects.create(name=gname,destination=gdest)
		##TODO return ?(locations of users to plot on map)?
		return HttpResponse("Success")
		
		
	if op==1:
		phone = input_dict["phone"]
		g_id = UserIsGroupMember.objects.get(phone_number=user1).g_id.g_id
		group = Group.objects.get(g_id=g_id)
		members = UserIsGroupMember.objects.filter(g_id=group)
		phones=[]
		names=[]
		for member in members:
			phones.append(member.phone_number.phone_number)
			names.append(member.phone_number.name)
		json_response = {}
		json_response["member_names"] = ";".join(names)
		json_response["member_phones"] = ";".join(phones)
		return HttpResponse(json.dumps(json_response))
	if op==3:
		phone = input_dict["phone"]
		
		try:
			g_id = UserIsGroupMember.objects.get(phone_number=user1).g_id.g_id
			group = Group.objects.get(g_id=g_id)
			Group.objects.get(g_id=group.g_id).delete()
			return HttpResponse("Success")

			
