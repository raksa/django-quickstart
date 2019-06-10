all: runcore

test:
	export DJANGO_SETTINGS_MODULE=core.settings.test; python -m pytest

runcore:
	export DJANGO_SETTINGS_MODULE=core.settings; python manage.py runserver 8001

pyclean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
