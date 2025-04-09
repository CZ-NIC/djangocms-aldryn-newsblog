# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

from aldryn_newsblog import __version__


REQUIREMENTS = [
    'aldryn-apphooks-config',
    'djangocms-aldryn-categories',
    'djangocms-aldryn-common',
    'djangocms-aldryn-people',
    'djangocms-aldryn-search @ git+https://github.com/CZ-NIC/djangocms-aldryn-search@upgrade-cms',
    'djangocms-aldryn-translation-tools',
    'django-haystack',
    'backport-collections',
    'djangocms-text-ckeditor',
    'django-taggit',
    'python-dateutil',
    'lxml',
    'lxml_html_clean',
    'looseversion',
]

# https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Framework :: Django',
    'Framework :: Django :: 3.2',
    'Framework :: Django :: 4.0',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
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
    python_requires='>=3.7',
    install_requires=REQUIREMENTS,
    extras_require={
        'test': [
            'pytz',
        ]
    },
    classifiers=CLASSIFIERS,
    test_suite="test_settings.run",
)
