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

logger = logging.getLogger('MambaLogger')
