from .roleerror import RoleError


class AlreadyLoggedError(RoleError):
    '''
    Simple exception class for situations when user had already logged in/out but
    somewhy tried to log in/out once again..
    '''
