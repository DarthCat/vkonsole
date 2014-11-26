#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import login
import getpass
import urllib2
from urllib import urlencode
import json
import urwid

DIALOGS_COUNT = 25
FRIENDS_COUNT = 15
email = raw_input("Email: ")
password = getpass.getpass()
client_id = "4034599" # Vk application ID
token, user_id = login.auth(email, password, client_id, "friends,messages")

friends_cache = list()
friends_dict = dict()
dialogs_cache = list()

def call_api(method, params, token):
	params["access_token"]= token
	url = "https://api.vk.com/method/%s?%s" % (method, urlencode(params))
	try:
		return json.loads(urllib2.urlopen(url).read())["response"]
	except KeyError: 
		print json.loads(urllib2.urlopen(url).read())
		return


def getFriends(id, skip=0):
	global friends_cache
	global friends_dict
	if not friends_cache:
		ids = call_api('getFriends', {'user_id':id, 'order': 'hints'}, token)
		ids = [str(id) for id in ids]
		content = call_api('users.get', {'user_ids': ",".join(ids), 'fields': 'screen_name'}, token)
		friends = list()	
		for friend in content:
			option = dict()
			option['name'] = ' '.join((friend['first_name'], friend['last_name']))
			option['uid'] = friend['uid']
			friends_dict[option['uid']] = option['name']
			friends.append(option)
		friends_cache = friends 
	return friends_cache[skip:skip+FRIENDS_COUNT]

def getName(uid): 
	global friends_dict
	if isinstance(uid, list):
		ids = [str(id) for id in uid]
		uid = ",".join(ids)
	content = call_api('users.get', {'user_ids': uid, 'fields': 'screen_name'}, token)
	name = "*username*"
	for user in content: 
		friends_dict[user['uid']] = ' '.join((user['first_name'], user['last_name']))
		name = friends_dict[user['uid']]
	return name

log = open('log.txt', 'a')

def getDialogs(id, skip=0):
	global dialogs_cache
	response = call_api('messages.getDialogs', {'count':DIALOGS_COUNT, 'offset':skip, 'preview_length': 0}, token)
	dialogs = list()
	response = response[1:]
	dialogs_cache = dialogs_cache + response
	for dialog in response: 
		current = {}
		name = dialog['title']
		uid = dialog['uid']	
		if '...' in dialog['title']:
			if uid in friends_dict.keys(): 
				name = friends_dict[uid]
			else: 
				print uid
				name = getName(uid)
		body = dialog['body']
		if 'chat_id' in dialog: 
			current['chat'] = True
			current['id'] = dialog['chat_id']
		else:
			current['id'] = dialog['uid']
		current['title'] = name
		current['preview'] = dialog['body']
		dialogs.append(current)
	return dialogs

def friendsMenu(id, skip=0, title="Список друзей"):
	global friends_cache
	friends = getFriends(id, skip)
	body = [urwid.Text(title), urwid.Divider()]
	if skip >= FRIENDS_COUNT: 
		button = urwid.Button('Предыдущие 15')
		urwid.connect_signal(button, 'click', drawFriendsMenuWrapper, skip - FRIENDS_COUNT)
		body.append(urwid.AttrMap(button, None, focus_map='reversed'))
	for friend in friends: 
		button = urwid.Button(friend['name'])    	
		urwid.connect_signal(button, 'click', friend_chosen, friend)
		body.append(urwid.AttrMap(button, None, focus_map='reversed'))
	if len(friends_cache) - skip > FRIENDS_COUNT:
		button = urwid.Button('Следующие 15')
		urwid.connect_signal(button, 'click', drawFriendsMenuWrapper, skip+FRIENDS_COUNT)
		body.append(urwid.AttrMap(button, None, focus_map='reversed'))
	return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def showchat(button, args):
	pass


def dialogsMenu(id, skip=0, title="Диалоги"):
	global dialogs_cache
	dialogs = getDialogs(id, skip)
	body = [urwid.Text(title), urwid.Divider()]
	#if skip >= FRIENDS_COUNT: 
		#button = urwid.Button('Предыдущие 15')
		#urwid.connect_signal(button, 'click', drawFriendsMenuWrapper, skip - FRIENDS_COUNT)
		#body.append(urwid.AttrMap(button, None, focus_map='reversed'))
	for dialog in dialogs: 
		button = urwid.Button(dialog['title']+"    "+dialog['preview'])    	
		urwid.connect_signal(button, 'click', showchat, dialog['id'])
		body.append(urwid.AttrMap(button, None, focus_map='reversed'))
	#if len(friends_cache) - skip > FRIENDS_COUNT:
		#button = urwid.Button('Следующие 15')
		#urwid.connect_signal(button, 'click', drawFriendsMenuWrapper, skip+FRIENDS_COUNT)
		#body.append(urwid.AttrMap(button, None, focus_map='reversed'))
	return urwid.ListBox(urwid.SimpleFocusListWalker(body))


def drawFriendsMenuWrapper(button, skip):
	drawFriendsMenu(skip=skip)

def drawFriendsMenu(skip=0):
	main = urwid.Padding(friendsMenu(user_id, skip), left=0, right=0)
	top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
	    align='center', width=('relative', 100),
	    valign='middle', height=('relative', 100),
	    min_width=20, min_height=9)
	urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()

def drawDialogMenu(skip=0):
	main = urwid.Padding(dialogsMenu(user_id, skip), left=0, right=0)
	top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    	align='center', width=('relative', 100),
    	valign='middle', height=('relative', 100),
    	min_width=20, min_height=9)
	urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run() 
def friend_chosen(button, friend):
	print "\a"


def exit_program(button):
	raise urwid.ExitMainLoop()

getFriends(user_id)
print friends_dict
#drawFriendsMenu()
getDialogs(user_id)
drawDialogMenu()