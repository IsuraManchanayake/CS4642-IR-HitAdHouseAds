# run following commands to scrape the data to data/houses.json
cd scraper
:>../data/houses.json && :>info.log && scrapy crawl houses -o ../data/houses.json --logfile 'info.log'

# optional: to add an id field for each json document run following commands
cd ../data
python append_index.py
