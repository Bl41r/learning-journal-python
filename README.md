# learning-journal-python
Repo of my learning journal from Code Fellows Python 401

heroku link:

### tox output
============================= test session starts ==============================
platform linux2 -- Python 2.7.12, pytest-3.0.1, py-1.4.31, pluggy-0.3.1
rootdir: /home/david/codefellows/401/website, inifile: pytest.ini
plugins: cov-2.3.1
collected 18 items

website/tests.py ..................

---------- coverage: platform linux2, python 2.7.12-final-0 ----------
Name                                   Stmts   Miss  Cover   Missing
--------------------------------------------------------------------
website/__init__.py                        8      0   100%
website/models/__init__.py                22     12    45%   16, 20-22, 46-49, 59-68
website/models/meta.py                     5      0   100%
website/models/mymodel.py                  8      0   100%
website/routes.py                          6      0   100%
website/scripts/__init__.py                0      0   100%
website/scripts/initializedb.py           26     16    38%   22-25, 29-45
website/views/__init__.py                  0      0   100%
website/views/default.py                  27      1    96%   54
website/views/notfound.py                  4      2    50%   6-7
--------------------------------------------------------------------
TOTAL                                    106     31    71%


========================== 18 passed in 0.89 seconds ===========================
py35 inst-nodeps: /home/david/codefellows/401/website/.tox/dist/website-0.0.zip
py35 installed: beautifulsoup4==4.5.1,coverage==4.2,Jinja2==2.8,Mako==1.0.4,MarkupSafe==0.23,PasteDeploy==1.5.2,py==1.4.31,Pygments==2.1.3,pyramid==1.7.3,pyramid-debugtoolbar==3.0.4,pyramid-jinja2==2.6.2,pyramid-mako==1.0.2,pyramid-tm==0.12.1,pytest==3.0.1,pytest-cov==2.3.1,repoze.lru==0.6,six==1.10.0,SQLAlchemy==1.0.14,transaction==1.6.1,translationstring==1.3,venusian==1.0,waitress==0.9.0,WebOb==1.6.1,website==0.0,WebTest==2.0.23,zope.deprecation==4.1.2,zope.interface==4.2.0,zope.sqlalchemy==0.7.7
py35 runtests: PYTHONHASHSEED='331056941'
py35 runtests: commands[0] | py.test website/tests.py --cov=website website/tests.py --cov-report term-missing
============================= test session starts ==============================
platform linux -- Python 3.5.2, pytest-3.0.1, py-1.4.31, pluggy-0.3.1
rootdir: /home/david/codefellows/401/website, inifile: pytest.ini
plugins: cov-2.3.1
collected 18 items

website/tests.py ..................

----------- coverage: platform linux, python 3.5.2-final-0 -----------
Name                                   Stmts   Miss  Cover   Missing
--------------------------------------------------------------------
website/__init__.py                        8      0   100%
website/models/__init__.py                22     12    45%   16, 20-22, 46-49, 59-68
website/models/meta.py                     5      0   100%
website/models/mymodel.py                  8      0   100%
website/routes.py                          6      0   100%
website/scripts/__init__.py                0      0   100%
website/scripts/initializedb.py           26     16    38%   22-25, 29-45
website/views/__init__.py                  0      0   100%
website/views/default.py                  27      1    96%   54
website/views/notfound.py                  4      2    50%   6-7
--------------------------------------------------------------------
TOTAL                                    106     31    71%

