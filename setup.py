from setuptools import setup, find_packages
import plaid


url = 'https://github.com/plaid/plaid-python-legacy'

setup(
    name='plaid-python-legacy',
    version=plaid.__version__,
    description="Python API client library for Plaid's legacy API",
    long_description='',
    keywords='api, client, plaid',
    url=url,
    download_url='{}/tarball/v{}'.format(url, plaid.__version__),
    license='MIT',
    packages=find_packages(exclude='tests'),
    package_data={'README': ['README.md']},
    install_requires=['requests==2.7.0'],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Web Environment",
    ]
)
