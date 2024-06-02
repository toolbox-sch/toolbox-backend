from core.exceptions import CustomException


class PasswordDoesNotMatchException(CustomException):
    code = 401
    error_code = "USER__PASSWORD_DOES_NOT_MATCH"
    message = "password does not match"


class DuplicateEmailOrNicknameException(CustomException):
    code = 400
    error_code = "USER__DUPLICATE_EMAIL_OR_NICKNAME"
    message = "duplicate email or nickname"


class UserNotFoundException(CustomException):
    code = 404
    error_code = "USER__NOT_FOUND"
    message = "user not found"


class NullFileException(CustomException):
    code = 422
    error_code = "FILE__NULL_FILE"
    message = "file can't be null"


class RejectFileCreationException(CustomException):
    code = 500
    error_code = "FILE__REJECT_FILE_CREATION"
    message = "can't create file"
