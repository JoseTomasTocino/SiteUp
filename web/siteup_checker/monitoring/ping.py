import subprocess
import re
import os
import logging
logger = logging.getLogger("debugging")

DEVNULL = open(os.devnull, 'wb')


def check_ping(target):
    """
    Sends a ping to the given target, and returns a dictionary with the parsed result.
    """

    logger.info(u"Check Ping, target: %s" % target)

    try:
        # Launch ping process
        process = subprocess.Popen(["ping", "-c3", "-w2", target], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Get the output
        ping_raw_response, ping_raw_error = process.communicate()

    except Exception as e:
        # There was a problem executing the ping command, log the error
        logger.error(e)

        return {'valid': False}

    # Compile regular expression to parse ping's output
    matcher = re.compile(r"""
^PING \s+                            # Header
(?P<host>.*?) \s+                    # Host
\((?P<ip>.*?)\)                      # IP address

.*?                                  # Ignore individual pings

(?P<transmitted>\d+) \s+ packets       .*?       # Packets transmitted
(?P<received>\d+) \s+ received         .*?       # Packets received

(?:                                  # Non-capturing group for the numerical statistics (that may not appear)
rtt min/avg/max/mdev = \s+           # Separator
(?P<min>[^/]*)/                      # Min time
(?P<avg>[^/]*)/                      # Avg time
(?P<max>[^/]*)/                      # Max time
(?P<mdev>.*?) \s ms                  # Mdev
)?

""", re.DOTALL | re.IGNORECASE | re.MULTILINE | re.VERBOSE)

    # Run the regular expression to parse ping's output
    results = matcher.search(ping_raw_response)

    # If it doesn't match (due to an error)
    if not results:
        logger.error("PING ERROR" + ping_raw_response)

        # Most usual kind of error is bad host
        if "unknown host" in ping_raw_response:
            return {'valid': False, 'error': 'unknown host'}
        else:
            return {'valid': False}

    # Get fields
    results = results.groupdict()
    results['valid'] = True

    # Cast the numeric fields to float
    for field in ('min', 'avg', 'max', 'mdev', 'transmitted', 'received'):
        if field in results and results[field] is not None:
            results[field] = float(results[field])
        else:
            results[field] = 0.0

    return results