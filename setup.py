from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='logstop',
    version='0.1.1',
    description='Keep personal data out of your logs',
    long_description=long_description,
    long_description_content_type='text/markdown',
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
