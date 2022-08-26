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


active:
	python3 -m venv env
	source env/bin/activate

install:
	pip install -r requirements/local.txt
