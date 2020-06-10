from sqlalchemy import and_, or_, desc, asc, event
from sqlalchemy.orm import joinedload, subqueryload
from graphspace.wrappers import with_session
from applications.discussions.models import *
from applications.users.dal import *
from applications.users.models import *
import graphspace.signals as socket
from graphspace.database import *

@with_session
def add_discussion(db_session, message, description, group_id, owner_email=None, is_resolved=0, parent_discussion_id=None):
	discussion = Discussion(owner_email=owner_email, group_id=group_id,
				  is_resolved=is_resolved, parent_discussion_id=parent_discussion_id, message=message, description=description)
	group = get_group(db_session, group_id)
	group.group_discussions.append(discussion)
	db_session.add(discussion)
	return discussion


@with_session
def get_discussion_by_group_id(db_session, group_id):
	query = db_session.query(Discussion).filter(Discussion.group_id == group_id)
	query = query.filter(Discussion.parent_discussion_id == None)
	return query.count(), query.all()

@with_session
def get_owner_email_by_group_id(db_session, group_id):
	"""

	Parameters
	----------
	db_session: Object
		Database session.
	graph_id: Integer
		Unique ID of graph.

	Returns
	-------
	return value: List
		List of all User Objects.

	"""
	query = db_session.query(User, Group)
	query = query.filter(User.email == Group.owner_email)
	return query.all()

@with_session
def get_user_emails_by_group_id(db_session, group_id):
	query = db_session.query(User, GroupToUser)
	# query = query.filter(Discussion.group_id == group_id)
	query = query.filter(GroupToUser.group_id == group_id)
	query = query.filter(User.id == GroupToUser.user_id)
	return query.all()

@with_session
def get_discussion(db_session, id):
	"""
	Get group by group id.
	:param db_session: Database session.
	:param id: Unique ID of the group
	:return: Group if id exists else None
	"""
	return db_session.query(Discussion).filter(Discussion.id == id).one_or_none()

@event.listens_for(Discussion, 'after_insert')
def update_listener(mapper, connection, discussion):
	send_discussion(discussion, event="insert")

def send_discussion(discussion, event):
	# users_list = get_user_emails_by_group_id(Database().session(), discussion.group_id)
	# users_list = [ele[0] for ele in users_list]
	users_list = get_users_by_group(Database().session(), discussion.group_id)
	# owner_list = get_owner_email_by_group_id(Database().session(), discussion.group_id)
	# owner_list = [ele[0] for ele in owner_list]
	socket.send_discussion(discussion=discussion, type="private", users=users_list, event=event)


# def send_discussion(mapper, connection, discussion):
# 	users_list = get_user_emails_by_group_id(Database().session(), discussion.group_id)
# 	users_list = [ele[0] for ele in users_list]
# 	socket.send_discussion(discussion=discussion, type="private", users=users_list)
