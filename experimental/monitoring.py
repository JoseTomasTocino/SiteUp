#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import re
import dns.resolver

def check_ping(location):
    """Sends a ping to the given location, and returns a dictionary with the results

    :param location: the computer to ping, identified with either an IP or a domain name

    :returns whatever
    
    Returns a dictionary with the different fields"""

    # Launch ping process and get stdout's content
    ping_raw_response = subprocess.Popen(["ping", "-c3", "-w10", location], stdout=subprocess.PIPE).stdout.read()

    # Compile regular expression
    matcher = re.compile(r"""
^PING \s+                            # Header
(?P<host>.*?) \s+                    # Host
\((?P<ip>.*?)\)                      # IP address
.*?                                  # Ignore information about each ping package
(?P<transmitted>\d+) \s+ packets .*? # Packets transmitted
(?P<received>\d+) \s+ received   .*? # Packets received
= \s+                                # Separator
(?P<min>[^\/]*)\/                    # Min time
(?P<avg>[^\/]*)\/                    # Avg time
(?P<max>[^\/]*)\/                    # Max time
(?P<mdev>.*?) \s ms                  # Mdev
""", re.DOTALL | re.IGNORECASE | re.MULTILINE | re.VERBOSE)

    # Parse ping's output
    results = matcher.search(ping_raw_response).groupdict()

    # Cast the times to float
    for field in ['min', 'avg', 'max', 'mdev']:
        results[field] = float(results[field])

    # Cast the other numbers to int
    for field in ['transmitted', 'received']:
        results[field] = int(results[field])
        
    return results

def check_dns(domain_name, register_type, expected_address):
    """Checks if a certain domain has a DNS register (of the proper type) that
    matches the expected address"""
    
    try:
        # Launch the query
        answer = dns.resolver.query(domain_name, register_type)

    # On timeout, or any other problem, just return false
    except:
        return False

    # Check if any of the results match the expected address
    for single_result in answer.rrset:
        if expected_address.strip() == single_result.to_text().strip():
            return True

    return False
    

if __name__ == '__main__':
#    check_ping('localhost')
    print check_dns('josetomastocino.com', 'A', '78.47.140.228')


