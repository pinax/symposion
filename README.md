# Symposion

A conference management solution from Eldarion.

Built with the generous support of the Python Software Foundation.

See http://eldarion.com/symposion/ for commercial support, customization and hosting

## Quickstart

- `pip install -r requirements.txt`
- `python manage.py syncdb`
- `python manage.py loaddata fixtures/*`

There are some extra pointers in [docs/getting_started.rst](https://github.com/pyconca/2013-web/blob/pyconca2013/docs/getting_started.rst)

## Translation

- `python manage.py makemessages -a -l fr`
- `python manage.py compilemessages`