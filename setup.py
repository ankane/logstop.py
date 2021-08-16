from setuptools import setup

setup(
    name='logstop',
    version='0.1.1',
    description='Keep personal data out of your logs',
    url='https://github.com/ankane/logstop.py',
    author='Andrew Kane',
    author_email='andrew@ankane.org',
    license='MIT',
    packages=[
        'logstop'
    ],
    python_requires='>=3.6',
    zip_safe=False
)
