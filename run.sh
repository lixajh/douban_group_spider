echo run start
python3 ./service/web.py --config config.ini > web.log
& python3 ./service/spider.py --config config.ini > spider.log
