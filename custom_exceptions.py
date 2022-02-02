from werkzeug.exceptions import HTTPException

class MissingArgumentError(HTTPException):
    code = 400
    description = 'Missing Argument'

class InvalidArgumentError(HTTPException):
    code = 400
    description = 'Invalid Argument'