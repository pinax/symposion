all: i18n docs static_css reset

.requirements-docs.txt-makeplaceholder: requirements-docs.txt
	pip install -r $?
	touch $@

_docs: .requirements-docs.txt-makeplaceholder
	make -C docs/ html
	open docs/_build/html/index.html

docs: _docs

i18n:
	cd symposion/; django-admin.py makemessages -a
	cd symposion/; django-admin.py compilemessages
	cd symposion_project/; django-admin.py makemessages -a
	cd symposion_project/; django-admin.py compilemessages

static_css:
	make -C symposion_project/static build

.requirements.txt-makeplaceholder: requirements.txt
	pip install -r $?
	touch $@

reset: .requirements.txt-makeplaceholder
	rm -r hacking || true
	mkdir hacking
	./manage.py syncdb --noinput
	./manage.py loaddata fixtures/pyconca2013/*.json
	./manage.py createsuperuser --username=admin --email=admin@example.com --noinput
	echo \
		'\nfrom django.contrib.auth.models import User\n'\
		'\nfor u in User.objects.all(): u.set_password("asdf"); u.save()\n'\
	| ./manage.py shell
	echo "-----------------------------------------\n"\
		 "\rUser 'admin@example.com' created with password 'asdf'\n"\
	     "\r-----------------------------------------"

hacking/dev.db:
	make reset

run: hacking/dev.db
	./manage.py runserver 127.0.0.1:6544

restart_prod:
	./manage.py collectstatic --noinput
	sudo supervisorctl restart gunicorn-2013-staging.pycon.ca
