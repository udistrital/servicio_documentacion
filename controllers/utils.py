import pprint
import iso8601

def filter_json_array(json_array, query):
	#pprint.pprint(json_array)
	for key, value in query.items():
		data = None
		data = [obj for obj in json_array if(globals()[str(value["operator"])](obj[key], value["value"]))]
		json_array = data
	return json_array

def equal(param1, param2):
	#print (str(param1)+"="+str(param2))
	if len(param2)>0:
		for key in param2:
			try:
				object_target = iso8601.parse_date(param1)
				object_compare = iso8601.parse_date(key)
			except:
				object_target = str(param1)
				object_compare = str(key)

			if object_target == object_compare:
				return True
	else:
		try:
			object_target = iso8601.parse_date(param1)
			object_compare = iso8601.parse_date(param2)
		except:
			object_target = str(param1)
			object_compare = str(param2)

		if object_target == object_compare:
			return True
	return False

def between(param1, param2):
	#print (str(param1)+"="+str(param2))
	try:
		object_target = iso8601.parse_date(param1)
		object_less = iso8601.parse_date(param2[0])
		object_great = iso8601.parse_date(param2[1])
	except:
		object_target = str(param1)
		object_less = str(param2[0])
		object_great = str(param2[1])

	if object_less <= object_target <= object_great:
		return True
	return False

def contains(param1, param2):
	#print (str(param1)+"="+str(param2))
	if len([x for x in param1 if x[param2["key"]] in param2["values"]]) > 0:
		return True
	return False

def l_than(param1, param2):
	#print (str(param1)+"="+str(param2))
	try:
		object_target = iso8601.parse_date(param1)
		object_compare = iso8601.parse_date(param2)
	except:
		object_target = str(param1)
		object_compare = str(param2)

	if object_target < object_compare:
		return True
	return False

def g_than(param1, param2):
	#print (str(param1)+"="+str(param2))
	try:
		object_target = iso8601.parse_date(param1)
		object_compare = iso8601.parse_date(param2)
	except:
		object_target = str(param1)
		object_compare = str(param2)

	if object_target > object_compare:
		return True
	return False
	