Scrapy
------

First, clone the project: ::

    git clone git@github.com:guilhermetavares/myscrapy.git


Install the requirements, on enviroment with ``Python >= 3.4.3``: ::
    
    pip install requirements.txt


To run the tests, cd ``/faragov/faragov/``: ::

    python3 tests.py

The response, running with coverage: ::
    
    Name                          Stmts   Miss Branch BrPart  Cover
	---------------------------------------------------------------
	faragov/__init__.py               0      0      0      0   100%
	faragov/middlewares.py           18     18      4      0     0%
	faragov/settings.py               4      4      0      0     0%
	faragov/spiders/__init__.py       0      0      0      0   100%
	faragov/spiders/fara.py         100      0     46      1    99%
	faragov/tests.py                 63      0      6      1    99%
	---------------------------------------------------------------
	TOTAL                           185     22     56      2    88%

For running the ``spider``: ::

    scrapy crawl fara -o faragov.json
