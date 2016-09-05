Scraper for Congress data. Uses Scrapy.

## Cronjobs: 

```shell
scrapy crawl pdfurl >> scraping_pdf_url_log.txt 2>&1
scrapy crawl proyecto >> scraping_proyecto.log.txt 2>&1
scrapy crawl seguimientos >> scraping_seguimientos.log.txt 2>&1
scrapy crawl iniciativa >> scraping_iniciativas.log.txt 2>&1
scrapy crawl updater >> scraping_updater.log.txt 2>&1
scrapy crawl expediente >> scraping_expediente.log.txt 2>&1
python proyectos_de_ley/manage.py update_index --age=24 --settings=proyectos_de_ley.settings.production   >> updating_index.log.txt 2>&1
```

## Configure
You need a ``config.json`` file with credentials for the PostgreSQL so PDL can
save the scraped data.

```javascript
{                                                                                
    "drivername": "postgresql",                                                  
    "username": "username for postgresql database",                                                
    "password": "my password",                                                  
    "host": "localhost",                                                         
    "port": "5432",                                                              
    "database": "pdl",                                                           
    "crawlera_user": "optional",                                                    
    "crawlera_pass": "optional",
    "crawlera_enabled": "false",
    "legislature": "2016"
}
```