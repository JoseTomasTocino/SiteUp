#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import re
import dns.resolver, dns.exception
import requests
import logging
import os

logger = logging.getLogger(__name__)

from django.utils.translation import ugettext, ugettext_lazy as _

DEVNULL = open(os.devnull, 'wb')


def check_ping(target):
    """Sends a ping to the given target, and returns a dictionary with the
    fields of the result."""

    try:
        # Launch ping process
        p = subprocess.Popen(["ping", "-c3", "-w10", target], stdout=subprocess.PIPE, stderr=DEVNULL)
        ping_raw_response = p.stdout.read()
    except:
        # There was a problem executing the ping command, WAT
        return {'valid': False}

    # Compile regular expression to parse ping's output
    matcher = re.compile(r"""
^PING \s+                            # Header
(?P<host>.*?) \s+                    # Host
\((?P<ip>.*?)\)                      # IP address
.*?                                  # Ignore individual pings
(?P<transmitted>\d+) \s+ packets .*? # Packets transmitted
(?P<received>\d+) \s+ received   .*? # Packets received
= \s+                                # Separator
(?P<min>[^/]*)/                      # Min time
(?P<avg>[^/]*)/                      # Avg time
(?P<max>[^/]*)/                      # Max time
(?P<mdev>.*?) \s ms                  # Mdev
""", re.DOTALL | re.IGNORECASE | re.MULTILINE | re.VERBOSE)

    # Run the regular expression to parse ping's output
    results = matcher.search(ping_raw_response)

    # If it doesn't match (due to an error)
    if not results:
        return {'valid': False}

    # Get fields
    results = results.groupdict()
    results['valid'] = True

    # Cast the numeric fields to float
    for field in ['min', 'avg', 'max', 'mdev', 'transmitted', 'received']:
        results[field] = float(results[field])

    return results


def check_dns(target, record_type, expected_address):
    """Checks if a certain domain has a DNS record (of the proper type) that matches the expected address"""

    if record_type not in ('A', 'AAAA', 'CNAME', 'MX', 'TXT'):
        raise ValueError(_("Wrong record type"))

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
        return_obj['valid'] = False # TODO

    except Exception, e:  # TODO: add the proper exception type
        return_obj['valid'] = False

    return return_obj


def check_http_header(target, status_code):
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


def check_http_content(target, content_string):
    """Checks if a certain http URL contains the specified string."""

    return_obj = {}

    try:
        r = requests.get(target)
        return_obj['valid'] = True
        return_obj['status_ok'] = content_string in r.text
    except:
        return_obj['valid'] = False

    return return_obj


if __name__ == '__main__':
    print check_ping('localhost')
    print check_dns('josetomastocino.com', 'A', '78.47.140.228')
    print check_http_header('http://josetomastocino.com/', 200)
    print check_http_content('http://josetomastocino.com', 'Ingeniero')
