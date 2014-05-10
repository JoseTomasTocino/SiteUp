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
        process = subprocess.Popen(["ping", "-c3", "-W2", target], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Get the output
        ping_raw_response, ping_raw_error = process.communicate()

    except Exception as e:
        # There was a problem executing the ping command, log the error
        logger.error("PING PROCESS ERROR")
        logger.error(e)
        logger.error("END PING PROCESS ERROR")

        return {'valid': False, 'error': "Couldn't launch process"}

    # Compile regular expression to parse ping's output
    matcher = re.compile(r"""
^PING \s+                            # Header
(?P<host>.*?) \s+                    # Host
\((?P<ip>.*?)\)                      # IP address

.*?                                  # Ignore individual pings

(?P<transmitted>\d+) \s+ packets       .*?       # Packets transmitted
(?P<received>\d+) \s+ received         .*?       # Packets received
ms                                     \s*       # Ending of the statistics line
(                                    # Non-capturing group for the numerical statistics (that may not appear)
rtt .* = \s+                         # Separator
(?P<min>[^/]*)/                      # Min time
(?P<avg>[^/]*)/                      # Avg time
(?P<max>[^/]*)/                      # Max time
(?P<mdev>.*?) \s ms                  # Mdev
)?

""", re.DOTALL | re.IGNORECASE | re.MULTILINE | re.VERBOSE)

    # Run the regular expression to parse ping's output
    results = matcher.match(ping_raw_response)

    # If it doesn't match (due to an error)
    if not results:
        logger.error("PING OUTPUT ERROR, follows response and error output")
        logger.error(ping_raw_response)
        logger.error(ping_raw_error)
        logger.error("END OF PING OUTPUT ERROR")

        # Most usual kind of error is bad host
        if "unknown host" in ping_raw_response:
            return {'valid': False, 'error': 'Unknown host'}
        else:
            return {'valid': False, 'error': 'Unknown error'}

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
