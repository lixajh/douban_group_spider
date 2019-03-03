echo run.sh
python3 ./service/web.py --config config.ini & python3 ./service/spider.py --config config.ini
