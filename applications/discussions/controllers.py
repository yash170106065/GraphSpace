from sqlalchemy.exc import IntegrityError
import applications.discussions.dal as db
from graphspace.exceptions import ErrorCodes, BadRequest
from graphspace.wrappers import atomic_transaction


@atomic_transaction
def add_discussion(request, message=None, description=None, group_id=None, is_resolved=0, owner_email=None,
                   parent_discussion_id=None):
    # Construct new comment to add to database
    discussion = db.add_discussion(request.db_session, message=message, description=description,
                                   owner_email=owner_email,
                                   group_id=group_id, is_resolved=is_resolved,
                                   parent_discussion_id=parent_discussion_id)
    # Add comment edges

    return discussion


def get_discussion_by_group_id(request, group_id):
    return db.get_discussion_by_group_id(request.db_session, group_id=group_id)


def search_discussions_by_group_id(request, group_id=None):
	if group_id is None:
		raise Exception("Atleast one group id is required.")
	return db.get_discussion_by_group_id(request.db_session, group_id=group_id)