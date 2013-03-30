Getting Started
===============

Get your environment set up::

    virtualenv pycona-2013-web-env
    . pyconca-2013-web-env/bin/activate
    git clone git://github.com/pyconca/2013-web.git pyconca-2013-web
    cd pyconca-2013-web

If you're using XCode 4 on Snow Leopard::

    export ARCHFLAGS="-arch i386 -arch x86_64"


Install requirements::

    pip install -r requirements.txt

    # If you're still using Python 2.6 (stop that, use 2.7!)
    pip install importlib

Create a local database::

    ./manage.py syncdb
    # (and create superuser)

Insert initial data (the site won't work otherwise)::

    ./manage.py loaddata fixtures/pyconca2013/*.json

Go test it out::

    ./manage.py runserver
    # Go to http://localhost:8000/

For internationalization/i18n:

    cd symposion_project
    django-admin.py makemessages -a
    # now make changes to generated .po files ...
    django-admin.py compilemessages

To build documentation:
    
    # Install requirements for docs first
    pip install -r requirements-docs.txt
    cd doc/
    make html
    open _build/html/index.html
