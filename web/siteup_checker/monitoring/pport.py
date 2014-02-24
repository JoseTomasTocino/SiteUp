import socket
import logging
logger = logging.getLogger(__name__)

def check_port(host, port_number, content = None):
    logger.info("Port check, host: %s, port: %s, content: '%s'" % (host, port_number, content))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)

    # connect_ex returns an error number instead of raising an exception... in theory
    try:
        result = s.connect_ex((host, port_number))
    except Exception as e:
        return { 'valid': False }

    if result == 0:
        if not content:
            return { 'valid': True }
        else:
            recv_content = s.recv(512)
            logger.info("Received: %s" % recv_content)

            if content.lower() in recv_content.lower():
                return { 'valid': True }
            else:
                return { 'valid': False }

    else:
        return { 'valid': False }