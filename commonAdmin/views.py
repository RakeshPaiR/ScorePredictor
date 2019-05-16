from django.shortcuts import render
import urllib.request
from django.db import connection
import requests,json
from django.http import HttpResponseRedirect
# Create your views here.
def index(request) :
	return render(request,'commonAdmin/admin.html')

l = []
m = []
context = {}
def getMatches(request) :
	uri = 'http://api.football-data.org/v2/competitions/'
	headers = { 'X-Auth-Token': 'f376990520ea475b8d1a91341ee2c75a' }
	if request.method == "POST" :
		code = request.POST.get('compCode')
		uri += code + '/matches'
		response = requests.get(uri,headers=headers)
		matches = response.json()['matches']
		del m[:]
		for match in matches :
			if match not in m :
				m.append(match)
		context['matches'] = m
		#context['competitions'] = l
		context['code'] = code
	else :
		response = requests.get(uri,headers=headers)
		competitions = response.json()['competitions']
		del l[:]
		for competition in competitions :
			if competition['plan'] == 'TIER_ONE' :
				if competition not in l :
					l.append(competition)
		context['competitions'] = l
		context['matches'] = None
		context['code'] = None
	
	return render(request,'commonAdmin/admin.html',context)

def storeMatches(request):
	cursor = connection.cursor()
	if request.method == "POST" :
		#print(context['code'])
		allMatches = request.POST.getlist('Match')
		#print(allMatches)
		for match in allMatches :
			compCode = context['code']
			matchId = int(match)
			for i in context['competitions'] :
				if i['code'] == compCode :
					compName = i['name']
					break
			for i in context['matches'] :
				#print(i['id'],match)
				if int(i['id']) == int(match) :
					#print('hello')
					homeId = int(i['homeTeam']['id'])
					homeName = i['homeTeam']['name']
					awayId = int(i['awayTeam']['id'])
					awayName = i['awayTeam']['name']
					status = i['status']
					break
			print(compCode,matchId,compName,homeId,homeName,awayId,awayName)
			cursor.execute("SELECT count(*) from Matches where match_id={}".format(matchId))
			r = cursor.fetchone()
			if (r[0] == 0) :
				cursor.execute("INSERT INTO Matches (match_id,compCode,compName,homeTeam,awayTeam,homeTeamId,awayTeamId,status) values('{}','{}','{}','{}','{}','{}','{}','{}')".format(matchId,compCode,compName,homeName,awayName,homeId,awayId,status))
	cursor.close()
	Next = request.POST.get('next','/')
	#print(Next)
	return HttpResponseRedirect(Next)