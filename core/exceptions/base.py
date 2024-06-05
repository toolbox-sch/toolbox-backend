class CustomException(Exception):
    code = 400
    error_code = "BAD_REQUEST"
    message = "BAD REQUEST"

    def __init__(self, message=None):
        if message:
            self.message = message
