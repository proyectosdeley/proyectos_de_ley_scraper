coverage:
	rm -rf pdl_scraper/cover
	rm -rf .coverage
	nosetests -w pdl_scraper --cover-package=pdl_scraper --cover-html --with-coverage --cover-inclusive --cover-erase

lint:
	flake8 pdl_scraper