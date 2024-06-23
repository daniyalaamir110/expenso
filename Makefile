VENV=venv
PYTHON=$(VENV)/bin/python
PROJ=expenso

venv:
	python3 -m venv $(VENV)

requirements:
	$(PYTHON) -m pip install -r requirements.txt

proj:
	$(PYTHON) -m django-admin startproject $(PROJ)

install:
	$(PYTHON) -m pip install $(PKG) && $(PYTHON) -m pip freeze > requirements.txt

shell:
	$(PYTHON) $(PROJ)/manage.py shell

run:
	$(PYTHON) $(PROJ)/manage.py runserver

app:
	cd $(PROJ) && ../$(PYTHON) manage.py startapp $(NAME)

migrate:
	$(PYTHON) $(PROJ)/manage.py migrate $(APP)

migrations:
	$(PYTHON) $(PROJ)/manage.py makemigrations $(APP)

superuser:
	$(PYTHON) $(PROJ)/manage.py createsuperuser

test:
	$(PYTHON) $(PROJ)/manage.py test $(APP)

cities-light:
	$(PYTHON) $(PROJ)/manage.py cities_light

schema:
	$(PYTHON) $(PROJ)/manage.py spectacular --color --file schema.yml

celery:
	cd $(PROJ) && ../$(PYTHON) -m celery -A $(PROJ).celery_app  worker --loglevel=DEBUG
