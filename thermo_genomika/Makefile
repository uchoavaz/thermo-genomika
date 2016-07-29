clean:
	find . -name "*.pyc" -exec rm -rf {} \;
	find . -name "*.log" -exec rm -rf {} \;

deps:
	pip install -r requirements.txt

setup:
	./manage.py makemigrations
	./manage.py migrate

run:
	./manage.py runserver --insecure

restart:

	./manage.py migrate
	./manage.py createsuperuser
user:
	./manage.py createsuperuser
