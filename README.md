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
learning_journal/models/mymodel.py             8      0   100%
learning_journal/routes.py                     9      0   100%
learning_journal/scripts/__init__.py           0      0   100%
learning_journal/scripts/initializedb.py      13      3    77%   47-50
learning_journal/security.py                  26      1    96%   25
learning_journal/views/__init__.py             0      0   100%
learning_journal/views/default.py             60     12    80%   19-20, 57-67
learning_journal/views/notfound.py             4      0   100%
------------------------------------------------------------------------
TOTAL                                        160     17    89%
```

### Python 2.7
```
---------- coverage: platform darwin, python 2.7.10-final-0 ----------
Name                                       Stmts   Miss  Cover   Missing
------------------------------------------------------------------------
learning_journal/__init__.py                  13      1    92%   9
learning_journal/models/__init__.py           22      0   100%
learning_journal/models/meta.py                5      0   100%
learning_journal/models/mymodel.py             8      0   100%
learning_journal/routes.py                     9      0   100%
learning_journal/scripts/__init__.py           0      0   100%
learning_journal/scripts/initializedb.py      13      3    77%   47-50
learning_journal/security.py                  26      1    96%   25
learning_journal/views/__init__.py             0      0   100%
learning_journal/views/default.py             60     12    80%   19-20, 57-67
learning_journal/views/notfound.py             4      0   100%
------------------------------------------------------------------------
TOTAL                                        160     17    89%
```

=======
## Authors:
Maelle Vance
With early contributions from Amos Boldor
