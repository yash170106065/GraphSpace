class ErrorCodes(object):
	"""
		A set of constants representing errors.  Error messages can change, but the codes will not.
		See the source for a list of all errors codes.
		Codes can be used to check for specific errors.
	"""
	class Validation(object):
		UserAlreadyExists = (1000, "User with `{0}` email id already exists!")

		MethodNotAllowed = (1000, "Incoming request is not allowed")
		BadRequest = (1001, "Bad Request")
		UserPasswordMisMatch = (1002, "User/Password not recognized")
		UserNotAuthorized = (1003, "You are not authorized to access this resource, create an account and contact resource's owner for permission to access this resource.")
		UserNotAuthenticated = (1004, "User authentication failed")

		# Graphs API
		IsPublicNotSet = (1005, "`is_public` is required to be set to True when `owner_email` and `member_email` are not provided.")
		NotAllowedGraphAccess = (1006, "User is not authorized to access private graphs created by {0}.")
		CannotCreateGraphForOtherUser = (1007, "Cannot create graph with owner email = `{0}`.")
		GraphIDMissing = (1008, "Graph ID is missing.")

		# Groups API
		NotAllowedGroupAccess = (1009, "User is not authorized to access groups they aren't part of. Set `owner_email` or `member_email` to {0}.")
		CannotCreateGroupForOtherUser = (1007, "Cannot create group with owner email = `{0}`.")

		# Layouts API
		NotAllowedLayoutAccess = (1010, "User is not authorized to access layouts which are not shared. Set `owner_email` to {0} or `is_shared` to 1.")
		CannotCreateLayoutForOtherUser = (1007, "Cannot create layout with owner email = `{0}`.")