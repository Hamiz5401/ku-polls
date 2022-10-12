[![codecov](https://codecov.io/gh/Hamiz5401/ku-polls/branch/main/graph/badge.svg?token=2RBC036LEJ)](https://codecov.io/gh/Hamiz5401/ku-polls)
![build](https://github.com/Hamiz5401/ku-polls/actions/workflows/python-app.yml/badge.svg)

## Online Polls And Surveys

Web application for creating online polls and surveys based
on the [Django Tutorial project](https://docs.djangoproject.com/en/4.1/intro/tutorial01/), with
additional features.

App created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at Kasetsart University.

## Install and Run

First you need to clone this repository

```
https://github.com/Hamiz5401/ku-polls.git
```

After that you create a virtual environment in the directory

```
python -m venv env
```

Activate the virtual environment

```
. env/Scripts/activate
```

Then you need to install the requirement by using

```
pip install -r requirements.txt
```

After that you need to create ```.env``` file that have configuration according to ```sample.env```

Create a database by 

```
python manage.py migrate
```

Load data

```
python manage.py loaddata data/polls.json data/users.json
```

Now you can run the server by tying

```
py manage.py runserver
```

## Demo user

| Username  | Password  |
|-----------|-----------|
|   test   | password |
|   demo   | password |

## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home)

- [Vision Statement](../../wiki/Vision%20Statement)
- [Requirements](../../wiki/Requirements)
- [Project Plan](../../wiki/Development%20Plan)
- [Task Board](https://github.com/users/Hamiz5401/projects/4/views/1)
- [Iteration 1 Plan](../../wiki/Iteration%201%20Plan)
- [Iteration 2 Plan](../../wiki/Iteration%202%20%Plan)
- [Iteration 3 Plan](../../wiki/Iteration%20320%Plan)
- [Iteration 4 Plan](../../wiki/Iteration%20420%Plan)
