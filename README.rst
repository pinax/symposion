=========
Symposion
=========

This repository stores the Pinax Symposion conference starter project. 
This project is open source and the license can be found in LICENSE.


Installation
============

To get setup with symposion_project code you must have the following
installed:

 * Python 2.6+
 * virtualenv 1.4.7+
 * C compiler (for PIL)

Setting up environment
----------------------

Create a virtual environment where your dependencies will live::

    $ virtualenv --no-site-packages myconference
    $ source myconference/bin/activate
    (myconference)$

Make the project directory your working directory::

    $ cd symposion_project

Install conference project dependencies::

    (myconference)$ pip install -r requirements/project.txt

Setting up the database
-----------------------

This will vary for production and development. By default the project is set
up to run on a SQLite database. If you are setting up a production database
see the Configuration section below for where to place settings and get the
database running. Now you can run::

    (myconference)$ python manage.py syncdb

Running a web server
--------------------

In development you should run::

    (myconference)$ python manage.py runserver

For production, this project comes with a WSGI entry point located in
``deploy/wsgi.py`` and can be referenced by gunicorn with
``deploy.wsgi:application``.

Configuration
=============

You can create a ``local_settings.py`` file alongside ``settings.py`` to
override any setting that may be environment/instance specific. This file is
ignored in ``.gitignore``.
