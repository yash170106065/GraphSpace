from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user
from graphspace.utils import websocket_group_name
import applications.users.dal as db
from graphspace.database import *


# Connected to websocket.connect and websocket.keepalive
@channel_session_user_from_http
def websocket_connect(message):
    # transfer_user(message.http_session, message.channel_session)
    if message.http_session['uid'] is not None:
        group_name = websocket_group_name(message.http_session['uid'])
        message.channel_session['owner_notification_group_name'] = group_name
        message.reply_channel.send({
            'accept': True
        })
        Group(group_name).add(message.reply_channel)


# Connected to websocket.keepalive
@channel_session_user
def websocket_keepalive(message):
    Group(message.channel_session['owner_notification_group_name']).add(
        message.reply_channel)


# Connected to websocket.disconnect
@channel_session_user
def websocket_disconnect(message):
    # transfer_user(message.http_session, message.channel_session)
    message.reply_channel.send({
        'close': True
    })
    if message.channel_session.get('owner_notification_group_name', None) is not None:
        Group(message.channel_session['owner_notification_group_name']).discard(
            message.reply_channel)
