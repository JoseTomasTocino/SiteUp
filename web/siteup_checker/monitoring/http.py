import logging
logger = logging.getLogger(__name__)

import requests

def check_http_header(target, status_code=200):
    """Checks if a certain http URL returns the correct status code."""

    return_obj = {}

    try:
        r = requests.head(target)
        return_obj['valid'] = True
        return_obj['status_code'] = r.status_code
        return_obj['status_ok'] = r.status_code == status_code
    except Exception as e: # TODO: add the proper exception type
        logger.error(e)
        return_obj['valid'] = False

    return return_obj


def check_http_content(target, content_string=''):
    """Checks if a certain http URL contains the specified string."""

    return_obj = {}

    try:
        r = requests.get(target)
        return_obj['valid'] = True
        return_obj['status_ok'] = content_string in r.text
    except Exception as e:
        logger.error(e)
        return_obj['valid'] = False

    return return_obj