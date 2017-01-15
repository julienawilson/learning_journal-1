# Learning Journal


This is a learning journal blog-like application.  
It was created using Pyramid sqlAlchemy.


## Features:
- a postgres database to persist posts
- display posts list in home page
- each post has a detail page
- added security with permissions and csrf token
- If you are logged in:
    - you can create new posts
    - you can edit existing posts
    - you can delete existing posts
- api route returns a json object of all entries


## Installation:

note: you need a Postgres database for your learning journal. Your variable needs to point to this database.

- Clone this repo && CD into it
- `python3 -m venv .`
- Open `bin/activate` in your editor and pass your own environment variable as following :
    - export DATABASE_URL= *your own database url*
    - export AUTH_USERNAME= *your chosen username*
    - export AUTH_PASSWORD= *your chosen password hashed using passlibs*
    - export AUTH_SECRET= *your chosen secret*
    - export SESSION_SECRET= *your chosen session secret*
- `source bin/activate` to activate your environment
- `pip install -e .` to install the package
- `initialize_db development.ini` to initialize the database
- `pserve development.ini` and now check localhost!

## Testing:
You need a Postgres test database and have your variable point to this database.

- In tests.py, line 15, have the global variable `TEST_DB` point to your own test database
- Run `pip install -e .[testing]`
- Run `tox`

## Deployment:
It is deployed on Heroku at http://maellevance.herokuapp.com


## Coverage:

### Python 3.5
```
---------- coverage: platform darwin, python 3.5.2-final-0 -----------
Name                                       Stmts   Miss  Cover   Missing
------------------------------------------------------------------------
learning_journal/__init__.py                  13      1    92%   9
learning_journal/models/__init__.py           22      0   100%
learning_journal/models/meta.py                5      0   100%
learning_journal/models/mymodel.py            10      0   100%
learning_journal/routes.py                    11      0   100%
learning_journal/scripts/__init__.py           0      0   100%
learning_journal/scripts/initializedb.py      13      3    77%   47-50
learning_journal/security.py                  26      0   100%
learning_journal/views/__init__.py             0      0   100%
learning_journal/views/default.py             60      7    88%   54-64
learning_journal/views/notfound.py             4      0   100%
------------------------------------------------------------------------
TOTAL                                        164     11    93%
```

### Python 2.7
```
---------- coverage: platform darwin, python 2.7.10-final-0 ----------
Name                                       Stmts   Miss  Cover   Missing
------------------------------------------------------------------------
learning_journal/__init__.py                  13      1    92%   9
learning_journal/models/__init__.py           22      0   100%
learning_journal/models/meta.py                5      0   100%
learning_journal/models/mymodel.py            10      0   100%
learning_journal/routes.py                    11      0   100%
learning_journal/scripts/__init__.py           0      0   100%
learning_journal/scripts/initializedb.py      13      3    77%   47-50
learning_journal/security.py                  26      0   100%
learning_journal/views/__init__.py             0      0   100%
learning_journal/views/default.py             60      7    88%   54-64
learning_journal/views/notfound.py             4      0   100%
------------------------------------------------------------------------
TOTAL                                        164     11    93%
```

=======
## Authors:
Maelle Vance
With early contributions from Amos Boldor
