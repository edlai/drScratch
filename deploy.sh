#!/bin/sh

sudo pip install -r requirements.txt
sudo python manage.py makemigrations  # (Optional for Migration)
sudo python manage.py migrate
django-admin compilemessages          # (Optional for Multilingual)
sudo python manage.py createsuperuser --username=joe --email=joe@example.com    # (Optional for Createsuperuser)
sudo python manage.py runserver 0.0.0.0:8000