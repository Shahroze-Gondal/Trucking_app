from rest_framework import status


class CustomExceptionHandler(Exception):
    def __init__(self, message="Something went wrong.", status=status.HTTP_400_BAD_REQUEST):
        super().__init__()
        self.message = message
        self.status = status


def UseralreadyExists(name=''):
    return CustomExceptionHandler(
        message='already exists %s' % (name),
        status=status.HTTP_409_CONFLICT,
    )


def InvalidUser():
    return CustomExceptionHandler(
        message='This user does not exists in the system',
        status=status.HTTP_404_NOT_FOUND,
    )
