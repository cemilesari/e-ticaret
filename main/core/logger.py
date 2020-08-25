from django.utils.encoding import force_text
import os,datetime
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def LogThat(level='ERROR',msg=""):
    if str(level) == 'DEBUG':
        logger.debug(str(msg))
    elif str(level) == 'CRITICAL':
        logger.critical(str(msg))
    elif str(level) == 'INFO':
        logger.info(str(msg))
    else:
        logger.error(str(msg))