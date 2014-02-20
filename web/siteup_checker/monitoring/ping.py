import subprocess
import re
import os

DEVNULL = open(os.devnull, 'wb')


def check_ping(target):
    """Sends a ping to the given target, and returns a dictionary with the
    fields of the result."""

    try:
        # Launch ping process
        p = subprocess.Popen(["ping", "-c3", "-w10", target], stdout=subprocess.PIPE, stderr=DEVNULL)
        ping_raw_response = p.stdout.read()
    except Exception as e:
        # There was a problem executing the ping command, WAT
        logger.error(e)
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