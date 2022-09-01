all:
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

run_dev:
	python3 manage.py runserver --settings config.settings.local

run_prod:
	python3 manage.py runserver

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

web:
	python3 manage.py web_scraping

run_local:
    python3 manage.py runserver --settings config.settings.local 192.168.31.119:8000

create:
	python3 -m venv env

install:
	pip install -r requirements/local.txt
