import logging
from logstop import LogstopFilter
import pytest
from urllib.parse import quote_plus, unquote_plus


class TestFilter:
    def test_email(self):
        self.assert_filtered('test@example.org')
        self.assert_filtered('test123@example.org')
        self.assert_filtered('TEST@example.org')
        self.assert_filtered('test@sub.example.org')
        self.assert_filtered('test@sub.sub2.example.org')
        self.assert_filtered('test+test@example.org')
        self.assert_filtered('test.test@example.org')
        self.assert_filtered('test-test@example.org')
        self.assert_filtered('test@example.us')
        self.assert_filtered('test@example.science')

    def test_phone(self):
        self.assert_filtered('555-555-5555')
        self.assert_filtered('555 555 5555')
        self.assert_filtered('555.555.5555')
        self.refute_filtered('5555555555')

        # use 7 digit min
        # https://stackoverflow.com/questions/14894899/what-is-the-minimum-length-of-a-valid-international-phone-number
        self.refute_filtered('+123456')
        self.assert_filtered('+1234567')
        self.assert_filtered('+15555555555')
        self.assert_filtered('+123456789012345')
        self.refute_filtered('+1234567890123456')

    def test_credit_card(self):
        self.assert_filtered('4242-4242-4242-4242')
        self.assert_filtered('4242 4242 4242 4242')
        self.assert_filtered('4242424242424242')
        self.refute_filtered('0242424242424242')
        self.refute_filtered('55555555-5555-5555-5555-555555555555')  # uuid

    def test_ssn(self):
        self.assert_filtered('123-45-6789')
        self.assert_filtered('123 45 6789')
        self.refute_filtered('123456789')

    def test_ip(self):
        self.refute_filtered('127.0.0.1')
        self.assert_filtered('127.0.0.1', ip=True)

    def test_url_password(self):
        self.assert_filtered('https://user:pass@host', expected='https://user:**********@host')
        self.assert_filtered('https://user:pass@host.com', expected='https://user:**********@host.com')

    def test_mac(self):
        self.refute_filtered('ff:ff:ff:ff:ff:ff')
        self.assert_filtered('ff:ff:ff:ff:ff:ff', mac=True)
        self.assert_filtered('a1:b2:c3:d4:e5:f6', mac=True)
        self.assert_filtered('A1:B2:C3:D4:E5:F6', mac=True)

    def test_multiple(self):
        self.assert_filtered('test@example.org test2@example.org 123-45-6789', expected='********** ********** **********')

    def test_order(self):
        self.assert_filtered('123-45-6789@example.org')
        self.assert_filtered('127.0.0.1@example.org', ip=True)

    def test_object(self):
        logger = self.get_logger()
        caplog = self._caplog

        logger.info(None)
        assert 'None' == caplog.records[-1].msg

    def assert_filtered(self, msg, expected='**********', **kwargs):
        logger = self.get_logger(**kwargs)
        caplog = self._caplog

        caplog.clear()
        logger.info(f'begin {msg} end')
        assert f'begin {expected} end' == caplog.records[-1].getMessage()

        caplog.clear()
        logger.info(f'begin {quote_plus(msg)} end')
        assert f'begin {expected} end' == unquote_plus(caplog.records[-1].getMessage())

        caplog.clear()
        logger.info(f'begin %s end', msg)
        assert f'begin {expected} end' == caplog.records[-1].getMessage()

    def refute_filtered(self, msg):
        self.assert_filtered(msg, expected=msg)

    def get_logger(self, **kwargs):
        logger = logging.getLogger(__name__)
        logger.filters.clear()
        logger.addFilter(LogstopFilter(**kwargs))
        return logger

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        caplog.set_level(logging.INFO)
        self._caplog = caplog
