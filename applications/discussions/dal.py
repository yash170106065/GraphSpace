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
	group.discussions.append(discussion)
	db_session.add(discussion)
	return discussion


@with_session
def get_discussion_by_group_id(db_session, group_id):
	query = db_session.query(Discussion).filter(Discussion.group_id == group_id)
	return query.count(), query.all()

@with_session
def get_user_emails_by_group_id(db_session, group_id):
	query = db_session.query(Discussion, User, GroupToUser)
	query = query.filter(Discussion.group_id == group_id)
	query = query.filter(GroupToUser.group_id == group_id)
	query = query.filter(User.id == GroupToUser.user_id)
	return query.all()

@event.listens_for(Discussion, 'after_insert')
def send_discussion(mapper, connection, discussion):
	users_list = get_user_emails_by_group_id(Database().session(), discussion.serialize()['group_id'])
	socket.send_discussion(discussion=discussion, type="private", users=users_list)
