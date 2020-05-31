. setup.sh
export FLASK_ENV='test'
python manage.py db downgrade
python manage.py db upgrade
python manage.py seed
python test_app.py
export FLASK_ENV='development'