from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import requests,json

def index(request) :
	cursor = connection.cursor()
	uri = 'http://api.football-data.org/v2/matches/'
	headers = { 'X-Auth-Token': 'f376990520ea475b8d1a91341ee2c75a' }
	r = cursor.execute("SELECT * FROM Matches;")
	l = []
	d = {}
	context = {}
	while True :
		x = cursor.fetchone()
		if x == None :
			break
		l.append(x)
	for i in l :
		d['match' + str(i[0])] = {'matchId':i[0],'compCode':i[1],'compName':i[2],'homeName':i[3],'awayName':i[4],"homeId":i[5],'awayId':i[6],'status':i[7]}
		uril = uri + str(i[0])
		response = requests.get(uril,headers=headers)
		#print(response)
		match = response.json()['match']
		status = match['status']
		if status != "SCHEDULED" :
			cursor.execute("UPDATE  Matches set status={}".format(status))
	context['matches'] = d
	# for i in context['matches'] :
	#  	print(context['matches'][i])
	if request.method == "POST" :
		pass
		#cursor.execute("INSERT INTO matches(Home_team,Away_team,Home_score,Away_score) values('{}','{}','{}','{}')".format(HomeTeam,AwayTeam,HomeScore,AwayScore))
	cursor.close()
	return render(request,'football/index.html',context=context)
