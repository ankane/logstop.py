import logging
import re

FILTERED_STR = '**********'
FILTERED_URL_STR = r'\1**********\2'

CREDIT_CARD_REGEX = r'\b[3456]\d{15}\b'
CREDIT_CARD_REGEX_DELIMITERS = r'\b[3456]\d{3}[\s+-]\d{4}[\s+-]\d{4}[\s+-]\d{4}\b'
EMAIL_REGEX = r'\b[\w]([\w+.-]|%2B)+(?:@|%40)[a-z\d-]+(?:\.[a-z\d-]+)*\.[a-z]+\b'
IP_REGEX = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
PHONE_REGEX = r'\b(?:\+\d{1,2}\s)?\(?\d{3}\)?[\s+.-]\d{3}[\s+.-]\d{4}\b'
SSN_REGEX = r'\b\d{3}[\s+-]\d{2}[\s+-]\d{4}\b'
URL_PASSWORD_REGEX = r'((?:\/\/|%2F%2F)\S+(?::|%3A))\S+(@|%40)'


class LogstopFilter(logging.Filter):
    def __init__(self, ip=False):
        self._ip = ip

    def filter(self, record):
        msg = record.msg

        # order filters are applied is important
        msg = re.sub(URL_PASSWORD_REGEX, FILTERED_URL_STR, msg)
        msg = re.sub(EMAIL_REGEX, FILTERED_STR, msg, flags=re.IGNORECASE)
        msg = re.sub(CREDIT_CARD_REGEX, FILTERED_STR, msg)
        msg = re.sub(CREDIT_CARD_REGEX_DELIMITERS, FILTERED_STR, msg)
        msg = re.sub(PHONE_REGEX, FILTERED_STR, msg)
        msg = re.sub(SSN_REGEX, FILTERED_STR, msg)

        if self._ip:
            msg = re.sub(IP_REGEX, FILTERED_STR, msg)

        record.msg = msg

        return True
