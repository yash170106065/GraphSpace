from channels import Group

from json import dumps
import re
import graphspace.utils as utils


def send_message(group_name, type, message):
    group_name = utils.websocket_group_name(group_name)
    Group(group_name).send({'text': dumps({"type": type, "message": message})})


def send_comment(comment, type, users=None):
    comment = utils.serializer(comment)
    if type == 'private':
    	email_list = []
    	if users:
    		for user in users:
    			user = utils.serializer(user[1])
    			email_list.append(user['email'])
    		email_list.append(comment['owner_email'])
    		email_list = list(set(email_list))
    	for email in email_list:
        	send_message(group_name=email, type="comment", message=comment)
    elif type == 'public':
        if comment['owner_email'] == None:
            comment['owner_email'] = 'Anonymous'
        send_message(group_name='anonymous@anonymous.com', type="comment", message=comment)