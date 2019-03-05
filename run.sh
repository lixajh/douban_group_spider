echo run
python3 ./service/web.py --config config.ini > a.log & python3 ./service/spider.py --config config.ini > b.log
