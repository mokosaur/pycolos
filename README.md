# pyColos

An examination platform implemented in python django. You can define closed multiple-choice questions and open questions. In the open questions students can type in their code as the answer, which is supported with python syntax highlighting. The language of the platform is Polish though it can be easily translated to another language.

### Dependencies

- **Python** (3 or higher)
- **Django** (recommended: 1.11)
- **django-bootstrap4**
- **django-markdownx**
- **pandas** 
- **requests**

### How to use it

To use our application you need to clone the code from this repo, and you need to have a database running on your computer. We recommend using MySQL as a database backend as it was used during the development. The username and password of your database should be stored in environment variables *DB_USER* and *DB_PASSWORD* respectively. You will also have to configure django settings, generate new secret key and turn off debug mode. If you don't know how to do that, [see here](https://docs.djangoproject.com/en/2.0/ref/settings/). Eventually, you need to migrate your database with the command: `python manage.py migrate` and apply translations with `python3 manage.py compilemessages`. 

#### Environmental variables needed:
1. *DB_USER* 
2. *DB_PASSWORD* 
3. *GITHUB_USERNAME*
4. *GITHUB_TOKEN*

Github token can be generated [here](https://github.com/settings/tokens), it is needed for accessing github API which is used to show markdown in a pretty and colored way.

### First steps after starting

1. Create a django superuser.
2. Log in as a superuser and create student accounts (you can do it through "Create users" button in the top right corner of your screen - USOS fileformat is also supported to generate all accounts at once).
3. Go to the admin panel (/admin) and create tests.
4. Now you can start the examination ;)
