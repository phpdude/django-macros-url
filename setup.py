#!/usr/bin/env python
import os

from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='django-macros-url',
    version=__import__('macrosurl').get_version(),
    author='Alexandr Shurigin',
    author_email='alexandr.shurigin@gmail.com',
    description='Macros Url library for django',
    license='MIT',
    keywords='django macros url pattern regex',
    url='https://github.com/phpdude/django-macros-url',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    test_suite='tests',
    long_description=read("README.markdown"),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Pre-processors'
    ],
    install_requires=['django']
)
