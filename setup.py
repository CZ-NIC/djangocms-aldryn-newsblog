# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

from aldryn_newsblog import __version__


REQUIREMENTS = [
    'aldryn-apphooks-config~=0.7',
    'djangocms-aldryn-categories~=2.0',
    'djangocms-aldryn-common~=2.0',
    'djangocms-aldryn-people~=3.0',
    'djangocms-aldryn-search~=3.0',
    'djangocms-aldryn-translation-tools~=1.0',
    'django-haystack~=3.3',
    'backport-collections~=0.1',
    'djangocms-text~=0.9',
    'django-taggit~=6.1',
    'python-dateutil~=2.9',
    'lxml~=6.0',
    'lxml-html-clean~=0.4',
    'looseversion~=1.3',
]

# https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Framework :: Django',
    'Framework :: Django :: 4.0',
    'Framework :: Django :: 5.0',
    'Framework :: Django CMS :: 4.1',
    'Framework :: Django CMS :: 5.0',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.12',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='djangocms-aldryn-newsblog',
    version=__version__,
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/CZ-NIC/djangocms-aldryn-newsblog',
    license='BSD',
    description='Adds blogging and newsing capabilities to django CMS.',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.10',
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    test_suite="test_settings.run",
)
