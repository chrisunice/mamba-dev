import logging

fmt = [
    '%(filename)s',
    '%(funcName)s',
    'Process: %(process)d',
    'Thread: %(thread)d',
    '%(message)s'
]

logging.basicConfig(
    format=' - '.join(fmt),
    level='DEBUG'
)

logger = logging.getLogger('MambaLogger')
