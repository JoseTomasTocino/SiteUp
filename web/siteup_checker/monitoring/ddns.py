import logging
logger = logging.getLogger(__name__)

import dns.exception, dns.resolver


def check_dns(target, record_type, expected_address):
    """Checks if a certain domain has a DNS record (of the proper type) that matches the expected address"""

    if record_type not in ('A', 'AAAA', 'CNAME', 'MX', 'TXT'):
        return {'valid': False}
        # raise ValueError(_("Wrong record type"))

    return_obj = {}

    try:
        # Launch the query
        answer = dns.resolver.query(target, record_type)

        # The query finished properly
        return_obj['valid'] = True
        return_obj['status_ok'] = False

        # Check if any of the results matches the expected address
        for single_result in answer.rrset:
            if expected_address.strip() == single_result.to_text().strip():
                return_obj['status_ok'] = True

    # On timeout, or any other problem, just return false
    except dns.resolver.NoAnswer as e:
        logger.error(e)
        return_obj['valid'] = False # TODO

    except Exception, e:  # TODO: add the proper exception type
        logger.error(e)
        return_obj['valid'] = False

    return return_obj