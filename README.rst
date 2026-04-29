|Project continuation| |Pypi package| |Pypi status| |Python versions| |License|


Aldryn News & Blog for django CMS
=================================

Continuation of the deprecated project `Divio Aldryn News&Blog <https://github.com/divio/aldryn-newsblog>`_.

Aldryn News & Blog is an `Aldryn <http://aldryn.com>`_-compatible news and
weblog application for `django CMS <http://django-cms.org>`_.

**Content editors** looking for documentation on how to use the editing
interface should refer to our `user manual`_ section.

**Django developers** who want to learn more about django CMS, as well as
how to install, configure and customize it for their own projects should
refer to the `documentation`_ sections.

Aldryn News & Blog is intended to serve as a model of good practice for
development of django CMS and Aldryn applications.

.. _user manual: http://aldryn-newsblog.readthedocs.io/en/latest/


======================
Installation & Updates
======================

Please head over to our `documentation`_ for all the details on how to install,
configure and use Aldryn News & Blog.

You can also find instructions on `how to upgrade`_ from earlier versions.

----------
Quick Help
----------

.. code:: python

    pip install djangocms-aldryn-newsblog


Add into ``INSTALL_APPS``:

.. code:: python

    'aldryn_apphooks_config',
    'aldryn_categories',
    'aldryn_common',
    'aldryn_newsblog',
    'aldryn_people',
    'aldryn_translation_tools',
    'sortedm2m',
    'taggit',


.. _documentation: http://aldryn-newsblog.readthedocs.io/en/latest/
.. _how to upgrade: http://aldryn-newsblog.readthedocs.io/en/latest/upgrade.html


============
Contributing
============

This is a an open-source project. We'll be delighted to receive your
feedback in the form of issues and pull requests. Before submitting your
pull request, please review our `contribution guidelines
<http://docs.django-cms.org/en/latest/contributing/index.html>`_.

We're grateful to all contributors who have helped create and maintain this package.
Contributors are listed at the `contributors <https://github.com/divio/aldryn-newsblog/graphs/contributors>`_
section.


.. |Project continuation| image:: https://img.shields.io/badge/Continuation-Divio_Aldryn_News&Blog-blue
    :target: https://github.com/CZ-NIC/djangocms-aldryn-newsblog
    :alt: Continuation of the deprecated project "Divio Aldryn News&Blog"
.. |Pypi package| image:: https://img.shields.io/pypi/v/djangocms-aldryn-newsblog.svg
    :target: https://pypi.python.org/pypi/djangocms-aldryn-newsblog/
    :alt: Pypi package
.. |Pypi status| image:: https://img.shields.io/pypi/status/djangocms-aldryn-newsblog.svg
   :target: https://pypi.python.org/pypi/djangocms-aldryn-newsblog
   :alt: status
.. |Python versions| image:: https://img.shields.io/pypi/pyversions/djangocms-aldryn-newsblog.svg
   :target: https://pypi.python.org/pypi/djangocms-aldryn-newsblog
   :alt: Python versions
.. |License| image:: https://img.shields.io/pypi/l/djangocms-aldryn-newsblog.svg
    :target: https://pypi.python.org/pypi/djangocms-aldryn-newsblog/
    :alt: license
