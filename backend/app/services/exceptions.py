class ServiceException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundException(ServiceException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)

class ValidationException(ServiceException):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)

class UnauthorizedException(ServiceException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401)

class ForbiddenException(ServiceException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=403)

class ConflictException(ServiceException):
    def __init__(self, message: str):
        super().__init__(message, status_code=409)
