PYTHON=python
AUTOPEP8=C:\Users\hp\Desktop\Vehicles_parking\.venv\Scripts\autopep8.exe

FLAKE8=$(PYTHON) -m flake8
BLACK=$(PYTHON) -m black
AUTOPEP8=$(PYTHON) -m autopep8


.PHONY: lint
lint:
	$(PYTHON) -m flake8 .

.PHONY: format
format:
	$(PYTHON) -m black .

.PHONY: autopep8
autopep8:
	$(AUTOPEP8) --in-place --aggressive --aggressive -r .
.PHONY: install
install:
	poetry install

.PHONY: init
init:
	poetry init
	
.PHONY: requirements
requirements:
	pip install -r requirements.txt

.PHONY: runserver
runserver:
	poetry run python manage.py runserver

.PHONY: shell 
shell: 
	poetry run python manage.py shell 

.PHONY: migrations
migrations:
	poetry run python manage.py makemigrations

.PHONY: migrate
migrate:
	poetry run python manage.py migrate

.PHONY: superuser
superuser:
	python manage.py createsuperuser

.PHONY: apply-migrations
apply-migrations:
		poetry run python manage.py makemigrations
		poetry run python manage.py migrate
		poetry run python manage.py runserver

.PHONY: runserver9000
runserver9000:
	python manage.py runserver 0.0.0.0:9000

# .PHONY: activateenv
# activateenv:
#     cmd /c ". env\Scripts\activate"

