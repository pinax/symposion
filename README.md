# Symposion

A conference management solution from Eldarion.

Built with the generous support of the Python Software Foundation.

See http://eldarion.com/symposion/ for commercial support, customization and hosting

## Getting started

Get your environment set up:

    $ virtualenv pycona-2013-web-env
    $ . pyconca-2013-web-env/bin/activate
    $ git clone git://github.com/pyconca/2013-web.git pyconca-2013-web
    $ cd pyconca-2013-web

If you're using XCode 4 on Snow Leopard:

    export ARCHFLAGS="-arch i386 -arch x86_64"

If you're still using Python 2.6 (stop that, use 2.7!):

    $ pip install importlib

Install requirements and reset the development environment:

    $ make reset
    ...
    -----------------------------------------
    User 'admin@example.com' created with password 'asdf'
    -----------------------------------------

Start the server! Go to `http://localhost:6544/`; you can log in with
`admin@example.com`/`asdf`.

    $ make run
    ./manage.py runserver 127.0.0.1:6544
    Validating models...

    0 errors found
    Django version 1.4.3, using settings 'symposion_project.settings'
    Development server is running at http://127.0.0.1:6544/
    Quit the server with CONTROL-C.

For internationalization/i18n, either do:

    $ make i18n

...or the good old way:

    # change the symposion_project directory
    $ cd symposion_project
    $ django-admin.py makemessages -a

    # now make changes to generated .po files ...
    $ django-admin.py compilemessages

    # go back to project root directory
    $ cd "$(git rev-parse --show-toplevel)"

    # also need to change symposion directory
    $ cd symposion
    $ django-admin.py makemessages -a

    # now make changes to generated .po files ...
    $ django-admin.py compilemessages

To build documentation::

    $ make docs

## Deploying

    $ ssh pycon.ca
    $ cd /data/web/2013.pycon.ca/pyconca
    $ . /data/virtualenvs/2013.pycon.ca/bin/activate
    $ git pull # Note the hash, I usually push a deploy tag from my local repo pointed at this hash
    $ make restart_prod

## Translation

- `python manage.py makemessages -a -l fr`
- `python manage.py compilemessages`
