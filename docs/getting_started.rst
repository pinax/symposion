Getting Started
===============

Get your environment set up::

    virtualenv pycona-2013-web-env
    . pyconca-2013-web-env/bin/activate
    git clone git://github.com/pyconca/2013-web.git pyconca-2013-web
    cd pyconca-2013-web

If you're using XCode 4 on Snow Leopard::

    export ARCHFLAGS="-arch i386 -arch x86_64"


Reset the development environment::

    # If you're still using Python 2.6 (stop that, use 2.7!)
    pip install importlib
    make reset

Go test it out::

    make run
    # Go to http://localhost:6544/
    # You can login as 'admin@example.com' with password 'asdf'

For internationalization/i18n::

    cd symposion_project
    django-admin.py makemessages -a
    # now make changes to generated .po files ...
    django-admin.py compilemessages

To build documentation::
    
    make docs
