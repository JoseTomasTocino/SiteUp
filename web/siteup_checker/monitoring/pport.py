import socket
import logging
logger = logging.getLogger(__name__)

def check_port(host, port_number, content = None):
    logger.info(u"Port check, host: %s, port: %s, content: '%s'" % (host, port_number, content))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)

    # connect_ex returns an error number instead of raising an exception... in theory
    try:
        result = s.connect_ex((host, port_number))
    except Exception as e:
        logger.error(u"Error: %s" % e)
        return { 'valid': False }

    logger.info(u"Port check, connection errno: %i" % result)

    if result == 0:
        ret_obj = { 'status_ok': True, 'valid': True }

        if content:
            try:
                recv_content = s.recv(512)
            except Exception as e:
                logger.error(u"Error: %s" % e)
                return { 'valid': False }

            logger.info(u"Received: %s" % recv_content)

            if content.lower() not in recv_content.lower():
                ret_obj['status_ok'] = False

        return ret_obj

    else:
        return { 'valid': False }