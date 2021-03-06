import requests
import logging
logger = logging.getLogger("debugging")


def check_http_header(target, status_code=200):
    """Checks if a certain http URL returns the correct status code."""

    return_obj = {}

    try:
        # Don't follow redirections if status_code is in the 30x family
        if status_code / 10 == 30:
            r = requests.head(target, timeout=10)
        else:
            r = requests.head(target, allow_redirects=True, timeout=10)

        return_obj['valid'] = True
        return_obj['status_code'] = r.status_code
        return_obj['status_ok'] = r.status_code == status_code

    except ValueError as e:
        logger.error(e)
        return_obj['valid'] = False
        return_obj['error'] = 'Error in the target'

    except requests.exceptions.RequestException as e:
        logger.error(e)
        return_obj['valid'] = False
        return_obj['error'] = 'Error in the request'

    except Exception as e:
        logger.error(e)
        return_obj['valid'] = False
        return_obj['error'] = 'Unknown error'

    return return_obj


def check_http_content(target, content_string=''):
    """Checks if a certain http URL contains the specified string."""

    return_obj = {}

    try:
        r = requests.get(target, timeout=10)
        return_obj['valid'] = True
        return_obj['status_ok'] = content_string.lower() in r.text.lower()

    except ValueError as e:
        logger.error(e)
        return_obj['valid'] = False
        return_obj['error'] = 'Error in the target'

    except requests.exceptions.RequestException as e:
        logger.error(e)
        return_obj['valid'] = False
        return_obj['error'] = 'Error in the request'

    except Exception as e:
        logger.error(e)
        return_obj['valid'] = False
        return_obj['error'] = 'Unknown error'

    return return_obj
