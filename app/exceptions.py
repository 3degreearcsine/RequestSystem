from fastapi import HTTPException, status
class CredentialsException(Exception):
    def __init__(self):
        pass

class ForbiddenException(Exception):
    def __init__(self):
        pass

