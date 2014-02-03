#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import re
import dns.resolver
import requests


def check_ping(target):
    """Sends a ping to the given target, and returns a dictionary with the
    results

    :param target: the computer to ping, identified with either an IP or a
        domain name

    :returns whatever

    Returns a dictionary with the different fields"""

    # Launch ping process and get stdout's content
    ping_raw_response = subprocess.Popen(["ping", "-c3", "-w10", target],
                                         stdout=subprocess.PIPE).stdout.read()

    # Compile regular expression
    matcher = re.compile(r"""
^PING \s+                            # Header
(?P<host>.*?) \s+                    # Host
\((?P<ip>.*?)\)                      # IP address
.*?                                  # Ignore individual pings
(?P<transmitted>\d+) \s+ packets .*? # Packets transmitted
(?P<received>\d+) \s+ received   .*? # Packets received
= \s+                                # Separator
(?P<min>[^/]*)/                    # Min time
(?P<avg>[^/]*)/                    # Avg time
(?P<max>[^/]*)/                    # Max time
(?P<mdev>.*?) \s ms                  # Mdev
""", re.DOTALL | re.IGNORECASE | re.MULTILINE | re.VERBOSE)

    # Run the regular expression to parse ping's output
    results = matcher.search(ping_raw_response)

    # If it doesn't match (due to an error)
    if not results:
        return {'valid': False}

    # Get different fields
    results = results.groupdict()
    results['valid'] = True

    # Cast the numbers to float
    for field in ['min', 'avg', 'max', 'mdev', 'transmitted', 'received']:
        results[field] = float(results[field])

    return results


def check_dns(target, register_type, expected_address):
    """Checks if a certain domain has a DNS register (of the proper type) that
    matches the expected address"""

    return_obj = {}

    try:
        # Launch the query
        answer = dns.resolver.query(target, register_type)

        # The query finished properly
        return_obj['valid'] = True
        return_obj['status_ok'] = False

        # Check if any of the results matches the expected address
        for single_result in answer.rrset:
            if expected_address.strip() == single_result.to_text().strip():
                return_obj['status_ok'] = True

    # On timeout, or any other problem, just return false
    except:
        return_obj['valid'] = False

    return return_obj


def check_http_header(target, status_code):
    return_obj = {}

    try:
        r = requests.head(target)
        return_obj['valid'] = True
        return_obj['status_code'] = r.status_code
        return_obj['status_ok'] = r.status_code == status_code
    except:
        return_obj['valid'] = False

    return return_obj


def check_http_content(target, content_string):
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
