#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import login
import getpass
import urllib2
import requests
from urllib import urlencode
import signal
import sys

email = "Timur_makarchuk@mail.ru"#raw_input("Email: ")
password = "mypassword"#getpass.getpass()
client_id = "4034599" # Vk application ID
token, user_id = login.auth(email, password, client_id, "friends,messages")
friends_list = list()
STATE = "MENU"

def sigterm_handler():
	if stat=="MENU":
		sys.exit(0)
	else:
		show_list()

def call_api(method, params, token):
	params["access_token"]= token
	url = "https://api.vk.com/method/%s?%s" % (method, urlencode(params))
	r = requests.get(url)
	try:
		return r.json()["response"]
	except KeyError: 
		print r.json()
		return

def show_list():
	global friends_list
	#if len(friends_list)==0:
	friends_list = call_api('execute.getFriendChats', {'v':5.28}, token)
	for i, friend in enumerate(friends_list, 1):
		for message in friend['messages']:
			if message['read_state']==0 and message['out']==0:
				state="*"
			else:
				state=""
		print "%s\t%s%s"% (i, friend['name'], state) 
	display_dialog(select_dialog())	


def select_dialog():
	num = raw_input(">>>")
	global friends_list
	try:
		num = int(num)
		friend = friends_list[num-1]
	except:
		print "You are doing it wrong", num
		friend = select_dialog()
	return friend

def display_dialog(friend):
	while 1:
		try:
			clear()
			friend['messages'].sort(key=lambda x: x['date'])
			last_message = friend['messages'][-1]
			try:
				new_messages = call_api('messages.getHistory', {'start_message_id':last_message['id'], 'user_id':friend['id']}, token)[1:]#MAGIC
			except Exception, e:
				print last_message
				raise e
			#print new_messages
			for message in new_messages:
				message['id']=message['mid']
				del(message['mid'])
			new_messages.sort(key=lambda x: x['date'])
			if len(new_messages)>1:
				friend['messages'] +=new_messages[1:]
			#print friend['messages']
			for message in friend['messages']:
				if message['out']:
					author= u"Я"
				else:
					author= friend['first_name']
				print u"{0}:\t{1}".format(author, message['body'])
			message=raw_input(">>>")
			call_api('messages.send', {"message": message, "uid": friend['id']}, token)
		except KeyboardInterrupt:
			return

def clear():
	print chr(27) + "[2J"


if __name__ == '__main__':
	while 1:
		clear()
		show_list()