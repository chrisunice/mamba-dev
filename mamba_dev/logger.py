import logging

fmt = [
    '%(name)s',
    '%(filename)s',
    '%(funcName)s',
    'Process: %(process)d',
    'Thread: %(thread)d',
    '%(message)s'
]

logging.basicConfig(
    format=' - '.join(fmt),
    level=logging.DEBUG
)

werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)

logger = logging.getLogger('MambaLogger')
