import logging
from logging import LogRecord
import re

__all__ = ['LogstopFilter']

FILTERED_STR = '**********'
FILTERED_URL_STR = r'\1**********\2'

CREDIT_CARD_REGEX = r'\b[3456]\d{15}\b'
CREDIT_CARD_REGEX_DELIMITERS = r'\b[3456]\d{3}[\s+-]\d{4}[\s+-]\d{4}[\s+-]\d{4}\b'
EMAIL_REGEX = r'\b[\w]([\w+.-]|%2B)+(?:@|%40)[a-z\d-]+(?:\.[a-z\d-]+)*\.[a-z]+\b'
IP_REGEX = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
PHONE_REGEX = r'\b(?:\+\d{1,2}\s)?\(?\d{3}\)?[\s+.-]\d{3}[\s+.-]\d{4}\b'
E164_PHONE_REGEX = r'(?:\+|%2B)[1-9]\d{6,14}\b'
SSN_REGEX = r'\b\d{3}[\s+-]\d{2}[\s+-]\d{4}\b'
URL_PASSWORD_REGEX = r'((?:\/\/|%2F%2F)\S+(?::|%3A))\S+(@|%40)'
MAC_REGEX = r'\b[0-9a-f]{2}(?:(?::|%3A)[0-9a-f]{2}){5}\b'


class LogstopFilter(logging.Filter):
    def __init__(self, ip: bool = False, mac: bool = False, url_password: bool = True, email: bool = True, credit_card: bool = True, phone: bool = True, ssn: bool = True) -> None:
        self._ip = ip
        self._mac = mac
        self._url_password = url_password
        self._email = email
        self._credit_card = credit_card
        self._phone = phone
        self._ssn = ssn

    def filter(self, record: LogRecord) -> bool:
        # same logic as getMessage
        msg = str(record.msg)
        if record.args:
            msg = msg % record.args
            record.args = ()

        # order filters are applied is important
        if self._url_password:
            msg = re.sub(URL_PASSWORD_REGEX, FILTERED_URL_STR, msg)

        if self._email:
            msg = re.sub(EMAIL_REGEX, FILTERED_STR, msg, flags=re.IGNORECASE)

        if self._credit_card:
            msg = re.sub(CREDIT_CARD_REGEX, FILTERED_STR, msg)
            msg = re.sub(CREDIT_CARD_REGEX_DELIMITERS, FILTERED_STR, msg)

        if self._phone:
            msg = re.sub(E164_PHONE_REGEX, FILTERED_STR, msg)
            msg = re.sub(PHONE_REGEX, FILTERED_STR, msg)

        if self._ssn:
            msg = re.sub(SSN_REGEX, FILTERED_STR, msg)

        if self._ip:
            msg = re.sub(IP_REGEX, FILTERED_STR, msg)

        if self._mac:
            msg = re.sub(MAC_REGEX, FILTERED_STR, msg, flags=re.IGNORECASE)

        record.msg = msg

        return True
