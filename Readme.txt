Scrapy
------

This project and readme its in github: https://github.com/guilhermetavares/myscrapy
In the url https://www.fara.gov/quick-search.html, click on "Active Foreign Principals".

This url "https://efile.fara.gov/pls/apex/f?p=171:130:0::NO:RP,130:P130_DATERANGE:N" is the starts url in Scrapy.

With the startup url set, i inspect the page and she loads a POST in javascript for pagination the results, and this POST is the navigations pages for Scrapy.

The POST url "https://efile.fara.gov/pls/apex/wwv_flow.show" navigates on all data pages avaible.

The item has the structure: ::
	
	{
		'address': '150 Broomielaw 5 Atlantic Quay',
		'country_name': 'UNITED KINGDOM',
		'date': '05/01/2012',
		'exhibit_url': 'http://www.fara.gov/docs/6334-Exhibit-AB-20160106-1.pdf',
		'foreign_principal': 'Scottish Development International',
		'registration': 'Development Counsellors International',
		'registration_date': '03/12/1993',
		'registration_number': '4777',
		'state': '',
		'url': 'https://efile.fara.gov/pls/apex/f?p=171:200:6624565563159::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:4777,Exhibit%20AB,UNITED%20KINGDOM'
	}

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
