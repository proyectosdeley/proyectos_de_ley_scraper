Scraper for Congress data. Uses Scrapy.

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
    "crawlera_enabled": "false"
}
```
