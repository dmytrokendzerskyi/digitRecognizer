from rest_framework.views import exception_handler


def image_exception_handler(ext, context):
    # get standart error response
    response = exception_handler(ext, context)
    if response is not None:
        response.data['status'] = 'error'

    return response