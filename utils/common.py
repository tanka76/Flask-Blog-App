import os
from .http_code import HTTP_201_CREATED,HTTP_200_OK

def generate_response(data=None, message=None, status=400):
    """
    It takes in a data, message, and status, and returns a dictionary with the data, message, and status
    """
    if status == HTTP_200_OK or status == HTTP_201_CREATED:
        status_bool = True
    else:
        status_bool = False

    return {
        "data": data,
        "message": modify_slz_error(message, status_bool),
        "status": status_bool,
    }, status

def modify_slz_error(message, status):
    """
    It takes a message and a status, and returns a list of errors

    """
    final_error = list()
    if message:
        if type(message) == str:
            if not status:
                final_error.append({"error": message})
            else:
                final_error = message
        elif type(message) == list:
            final_error = message
        else:
            for key, value in message.items():
                final_error.append({"error": str(key) + ": " + str(value[0])})
    else:
        final_error = None
    return final_error

