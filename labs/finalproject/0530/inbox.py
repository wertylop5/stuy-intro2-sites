#!/usr/bin/python
print 'content-type: text/html\n'
import Cookie,os,cgi,pickle,sys,cgitb,hashlib
cgitb.enable()

sys.path.insert(0, "../modules")
import stdStuff

head = '''<!DOCTYPE html>
<html>
<head><title>Profile</title>
</head>
<body>
   '''
body = ""
foot = '''
</body>
</html>
'''



form = cgi.FieldStorage()

def authenticate(u,ID,IP):
	loggedIn = open(stdStuff.directory + stdStuff.logFile,'r').read().split('\n')
	loggedIn = [each.split(',') for each in loggedIn]
	loggedIn.remove([''])
	for a in loggedIn:
		if a[0] == username:
			return a[1]==str(ID) and a[2]==IP
	return False

#gordons code
def poster():
	return '''<form action = "inbox.py" method = "GET">
Recipient: <input name="messageTarget" type="textfield" value="Watch your casing!">
<br>
Title: <input name="messageTitle" type="textfield">
<br>
Text: <textarea name="messageBody" rows="10" cols="15">
</textarea>
<br>
<input name="sendMessage" type="submit" value="Send Message">
</form>'''

def displayUnreadMessages(cookie):
	res = "<br><br><br>"
	currentUser = cookie["username"].value
	userDict = stdStuff.objFileToList(stdStuff.directory,
								stdStuff.userFile, byName=True)
	res += """<a href='inbox.py?markRead='all'&unread="hey">Mark all as read</a>"""
	for message in userDict[currentUser].inbox.messages:
		if message.viewed == False:
			res += message.display()
			res += "<a href='inbox.py?markRead='" + str(message.id) + \
	"'&unread='hey'>Mark as read</a>"
	return res

def displayReadMessages(cookie):
	res = "<br><br><br>"
	currentUser = cookie["username"].value
	userDict = stdStuff.objFileToList(stdStuff.directory,
								stdStuff.userFile, byName=True)
	res += "<a href='inbox.py?markUnread='all'&read='hey'>Mark all as unread</a>"
	for message in userDict[currentUser].inbox.messages:
		if message.viewed == True:
			res += message.display()
			res += "<a href='inbox.py?markUnread='" + str(message.id) + \
	"'&read='hey'>Mark as unread</a>"
	return res


def makePage(cookie, showRead):
	res = ""
	res += poster()
	res += "<br><br>"
	if showRead:
		res += \
"""
<form method="GET" action="inbox.py">
	<input name="unread" type="submit" value="View unread messages">
</form>
"""
		res += displayReadMessages(cookie)
	else:
		res += \
"""
<form method="GET" action="inbox.py">
	<input name="read" type="submit" value="View read messages">
</form>
"""
		res += displayUnreadMessages(cookie)
	return res

if 'HTTP_COOKIE' in os.environ:
	cookie_string=os.environ.get('HTTP_COOKIE')
	c = Cookie.SimpleCookie()
	c.load(cookie_string)
	##print all the data in the cookie
	#body+= "<h1>cookie data</h1>"
	#for each in c:
	#	body += each+":"+str(c[each].value)+"<br>"


	
	if 'username' in c and 'ID' in c:
		username = c['username'].value
		ID = c['ID'].value
		IP = os.environ['REMOTE_ADDR']
		
		if authenticate(username,ID,IP):
			currentUser = c["username"].value
			userDict = stdStuff.objFileToList(stdStuff.directory,
								stdStuff.userFile, byName=True)
			body += """<form method="GET" action="homepage.py">
<input name="logOut" type="submit" value="Log out">
</form>
<form method="GET" action="addFriend.py">
<input name="addFriend" type="submit" value="Add a friend">
</form>
<a href="profile.py">Go back to profile</a>
"""
			if "sendMessage" in form:
				recipient = form.getvalue("messageTarget")
				try:
					userDict[currentUser].inbox.sendMessage(
											recipient,
											form.getvalue("messageTitle"),
											form.getvalue("messageBody"))
				except KeyError:
					body += "<h1>" + recipient + "is not a registered user</h1>"
			
			if "markRead" in form:
				targetMessage = form.getvalue("markRead")
				if targetMessage == "all":
					for message in userDict[currentUser].inbox.messages:
						message.viewed = True
				else:
					for message in userDict[currentUser].inbox.messages:
						if message.id == int(targetMessage):
							message.viewed == True
							break
				stdStuff.objListToFile(userDict, stdStuff.directory,
										stdStuff.userFile, isDict=True)
			elif "markUnread" in form:
				targetMessage = form.getvalue("markUnread")
				if targetMessage == "all":
					for message in userDict[currentUser].inbox.messages:
						message.viewed = False
				else:
					for message in userDict[currentUser].inbox.messages:
						if message.id == int(targetMessage):
							message.viewed == False
							break
				stdStuff.objListToFile(userDict, stdStuff.directory,
										stdStuff.userFile, isDict=True)
			
			
			if "read" in form:
				body+=makePage(c, True)
			else:
				body+=makePage(c, False)
			
			body += """<br><a href="profile.py">Go back to profile</a>"""
		else:
			body+="Failed to Authenticate cookie<br>\n"
			body+= 'Go Login <a href="login.py">here</a><br>'
	else:
		body+= "Your information expired<br>\n"
		body+= 'Go Login <a href="login.py">here</a><br>'
else:
	body+= 'You seem new<br>\n'
	body+='Go Login <a href="login.py">here</a><br>'


print head
print body
print foot




