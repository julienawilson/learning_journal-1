# Learning Journal


This is a learning journal blog-like application.  
It was created using Pyramid sqlAlchemy.  

Right now it needs a lot more tests but it has some cool features


## Features:
- a postgres database to persist posts
- display posts list in home page
- each post has a detail page
- you can create new posts
- you can edit existing posts


## Deployment:
It is deployed on Heroku at http://maellevance.herokuapp.com


## Know Issues:
I was unable to get Tox to work so this app was only tested for python 3

## Coverage:

``
---------- coverage: platform darwin, python 3.5.2-final-0 -----------
Name                                       Stmts   Miss  Cover
--------------------------------------------------------------
learning_journal/__init__.py                  11      0   100%
learning_journal/models/__init__.py           22      0   100%
learning_journal/models/meta.py                5      0   100%
learning_journal/models/mymodel.py             8      0   100%
learning_journal/routes.py                     7      0   100%
learning_journal/scripts/__init__.py           0      0   100%
learning_journal/scripts/initializedb.py      29     18    38%
learning_journal/views/__init__.py             0      0   100%
learning_journal/views/default.py             47     13    72%
learning_journal/views/notfound.py             4      0   100%
--------------------------------------------------------------
TOTAL                                        133     31    77%
``

## Authors:
Maelle Vance
Amos Boldor
