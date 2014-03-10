import logging
logger = logging.getLogger(__name__)

import dns.exception, dns.resolver


def check_dns(target, record_type, expected_address):
    """Checks if a certain domain has a DNS record (of the proper type) that matches the expected address"""

    logger.info(u"Check DNS, target: %s, record_type: %s, expected_address: %s" % (target, record_type, expected_address))

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
            ans = single_result.to_text().strip()
            logger.info(u"Record: %s" % ans)

            if expected_address.strip() == ans:
                return_obj['status_ok'] = True

    # On timeout, or any other problem, just return false
    except dns.resolver.NoAnswer as e:
        return_obj['valid'] = False # TODO

    except dns.resolver.NXDOMAIN as e:
        return_obj['valid'] = False # TODO

    except dns.resolver.DNSException as e:
        return_obj['valid'] = False # TODO

    except Exception, e:  # TODO: add the proper exception type
        return_obj['valid'] = False

    return return_obj