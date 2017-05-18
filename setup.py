import logging
import sys
import getopt


_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s'))
_logger.addHandler(ch)


def init():
    _args = getopt.getopt(sys.argv[1:], '')
    print(_args)
    _logger.info('Beginning initial setup...')
    print(_args)