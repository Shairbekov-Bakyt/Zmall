all:
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

run_dev:
	python3 manage.py runserver --settings config.settings.local

run_prod:
	python3 manage.py runserver --settings config.settings.production

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

web:
	python3 manage.py web_scraping

# run_local:
#     ip = ifconfig | grep "inet " | grep -Fv 127.0.0.1 | awk '{print $2}'
#     python3 manage.py runserver --settings config.settings.local ifconfig | grep "inet " | grep -Fv 127.0.0.1 | awk '{print $2}':8000

create:
	python3 -m venv env

install:
	pip install -r requirements/local.txt
