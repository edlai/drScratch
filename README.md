drScratch
=========

drScratch is an analytical tool that evaluates your Scratch projects in a variety of computational areas to provide feedback on aspects such as abstraction, logical thinking, synchronization, parallelization, flow control, user interactivity and data representation. This analyzer is a helpful tool to evaluate your own projects, or those of your Scratch students.

You can try a beta version of drScratch at http://drscratch.org

---

Installation and Running
========================

Running in `Ubuntu 18.04` as an example.

## Requirement

```
# sudo apt update
# sudo apt install python-pip
# pip install -r requirements.txt
```

## Running

```
# django-admin compilemessages (Optional for Multilingual)
# python manage.py migrate
# python manage.py runserver
```

## Development

### Multilingual

using `zh_Hant` as an example

```
# sudo apt install gettext
# django-admin makemessages -l zh_Hant
```
Add translation to `drscratch/drScratch/locale/zh_Hant/LC_MESSAGES/django.po`, then run below command to product `.mo` file

```
# django-admin compilemessages
```
