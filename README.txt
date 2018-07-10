# run following commands to scrape the data to data/houses.json
cd scraper
:>../data/houses.json && :>info.log && scrapy crawl houses -o ../data/houses.json --logfile 'info.log'

# optional: to preprocess each json document for solr, run following commands
cd ../data
python preprocess_solr.py
