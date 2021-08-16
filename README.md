# Logstop.py

:fire: Keep personal data out of your logs

```python
logger.info('Hi test@example.org!')
# Hi **********!
```

By default, scrubs:

- email addresses
- phone numbers
- credit card numbers
- Social Security numbers (SSNs)
- passwords in URLs

Works even when data is URL-encoded with plus encoding

[![Build Status](https://github.com/ankane/logstop.py/workflows/build/badge.svg?branch=master)](https://github.com/ankane/logstop.py/actions)

## Installation

Run:

```sh
pip install logstop
```

And add it to your logger:

```python
from logstop import LogstopFilter

logger.addFilter(LogstopFilter())
```

## Options

To scrub IP addresses (IPv4), use:

```python
LogstopFilter(ip=True)
```

## Notes

- To scrub existing log files, check out [scrubadub](https://github.com/datascopeanalytics/scrubadub)
- To scan for unencrypted personal data in your database, check out [pdscan](https://github.com/ankane/pdscan)

## History

View the [changelog](CHANGELOG.md)

## Contributing

Everyone is encouraged to help improve this project. Here are a few ways you can help:

- [Report bugs](https://github.com/ankane/logstop.py/issues)
- Fix bugs and [submit pull requests](https://github.com/ankane/logstop.py/pulls)
- Write, clarify, or fix documentation
- Suggest or add new features

To get started with development:

```sh
git clone https://github.com/ankane/logstop.py.git
cd logstop.py
pip install -r requirements.txt
pytest
```
