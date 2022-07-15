===========================
django-codenerix-extensions
===========================

Codenerix Extensions is a module that enables `CODENERIX <https://www.codenerix.com/>`_ to set extensions on several platforms in a general manner.

.. image:: https://github.com/codenerix/django-codenerix/raw/master/codenerix/static/codenerix/img/codenerix.png
    :target: https://www.codenerix.com
    :alt: Try our demo with Codenerix Cloud

********
Features
********

* django-codenerix-extensions.corporate: Model for managing business's information
* django-codenerix-extensions.files: Abstract models and helpfull classes to simplify file handling
* django-codenerix-extensions.geodata: Models for geolocation (Continents, Countries, Regions, cities, time zones, etc) and data gotten from https://www.maxmind.com/

****
Demo
****

You can have a look to our demos online:

* `CODENERIX Simple Agenda DEMO <http://demo.codenerix.com>`_.
* `CODENERIX Full ERP DEMO <https://erp.codenerix.com>`_.

You can find some working examples in GITHUB at `django-codenerix-examples <https://github.com/codenerix/django-codenerix-examples>`_ project.

**********
Quickstart
**********

1. Install this package::

    For python 2: sudo pip2 install django-codenerix-extensions
    For python 3: sudo pip3 install django-codenerix-extensions

2. Add "codenerix_extensions" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'codenerix_extensions',
    ]

3. Add the param in setting:
	# list of languages available for the translation of the content of the models
	LANGUAGES_DATABASES = ['ES', 'EN']

4. Since Codenerix Extensions is a library, you only need to import its parts into your project and use them.

*************
Documentation
*************

Coming soon... do you help us?

You can get in touch with us `here <https://codenerix.com/contact/>`_.

*******
Credits
*******

Several technologies have been used to build CODENERIX EXTENSIONS:

=================================== =================== =========================== =========================================================
Project name                        License             Owner                       Link to project
=================================== =================== =========================== =========================================================
crypto-js                           MIT                 Jakub Zapletal              https://github.com/jakubzapletal/crypto-js         
=================================== =================== =========================== =========================================================
