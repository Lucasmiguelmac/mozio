# Dev
dev:
	python manage.py runserver

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

dump:
	python manage.py dumpdata > data.json

load:
	python manage.py loaddata data.json

reset_db:
	@python manage.py reset_db --noinput
	@python manage.py migrate

check: check.print
	@echo  "\033[92m** Manage.py Check**\033[0m"
	@python3 manage.py check
	@echo  "\033[92m**Make Check**\033[0m"
	@echo  "\033[92mRunning Isort Check...\033[0m"
	@isort .
	@echo "\033[92mRunning Black Check...\033[0m"
	@black .
	@echo "\033[92mRunning Flake8 Check...\033[0m"
	@flake8 .
	@echo "\033[92mRunning Mypy Check...\033[0m"
	@mypy .


check.print:
	@echo  "\033[92m** Print and TODO Checks**\033[0m"
	./checks.sh

test:
	pytest -x --cov -vv

shell:
	python manage.py shell_plus --ipython

reset_migrations:
	@find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	@find . -path "*/migrations/*.pyc" -delete