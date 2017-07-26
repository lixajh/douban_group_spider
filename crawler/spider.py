import datetime
import json
import logging
import os.path
import random
import threading
import time

import jieba
import mechanicalsoup
import requests
from bs4 import BeautifulSoup

from base.configparse import ConfigFile
from base.modules import DoubanGroup, Toppic
from base.serializer import load_data_file, save_data_file, data_file_path

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))


def parse_douban_group(text: str, min_time: datetime.datetime, check_func) -> (str, [Toppic]):
    toppics = []

    soup = BeautifulSoup(text, "html.parser")
    next = soup.select_one('.group-topics-more a')
    if not next:
        next = soup.select_one('span.next a')
        next_link = next.attrs['href']
    else:
        next_link = next.attrs['href']

    trs = soup.select('table.olt tr')

    all_count = 0
    out_of_date_count = 0

    for tr in trs[1:]:
        try:
            a = tr.select_one('td.title a')
            if not a:
                continue

            obj = Toppic()
            obj.link = a.attrs['href']
            obj.title = a.attrs['title']

            timestr = tr.select_one('td.time').text
            obj.time = datetime.datetime.strptime(timestr, "%m-%d %H:%M").replace(year=2017)

            check_func(obj)
            all_count += 1

            if obj.time < min_time:
                out_of_date_count += 1
                continue

        except AttributeError as ex:
            logging.error("Skip %s: %s" % (tr, ex))
            continue
        except ValueError as ex:
            logging.error("Skip %s: %s" % (tr, ex))
            continue

    if all_count > 0 and (out_of_date_count / all_count) > 0.5:
        return "", toppics
    else:
        return next_link, toppics


class DoubanGroupSpider(threading.Thread):
    def __init__(self, config, group: DoubanGroup):
        super(DoubanGroupSpider, self).__init__()

        self.group = group
        self.config = config

        self.account = config.get("account")
        self.password = config.get("password")

        self.data_file = data_file_path(group)

        self.all_toppics = load_data_file(self.data_file)
        self.all_toppics_id = set([info.toppic_id for info in self.all_toppics])

        self.init_crawl_hours_ago = int(config.get('hours_ago', section='Spider'))

        self.load_runtime_data()

    def _spider_runtime_data_path(self) -> str:
        return os.path.join(PROJECT_DIR, "data", self.group.id + '_spider.json')

    def load_runtime_data(self):
        config_path = self._spider_runtime_data_path()
        if os.path.exists(config_path):
            d = json.loads(open(config_path, 'r').read())
            self.min_time = datetime.datetime.strptime(d['last_time'], Toppic.TIME_SIMPLE_FORMAT)
        else:
            self.min_time = datetime.datetime.now() - datetime.timedelta(hours=self.init_crawl_hours_ago)

    def save_runtime_data(self):
        config_path = self._spider_runtime_data_path()
        with open(config_path, 'w') as f:
            d = {'last_time': self.min_time.strftime(Toppic.TIME_SIMPLE_FORMAT)}
            text = json.dumps(d)
            f.write(text)

    def _login(self) -> mechanicalsoup.StatefulBrowser:
        browser = mechanicalsoup.StatefulBrowser()

        browser.set_debug(True)
        browser.open("https://www.douban.com")
        # browser.select_form('#lzform')
        # browser["form_email"] = self.account
        # browser["form_password"] = self.password
        # resp = browser.submit_selected()
        # _ = browser.get_current_page()

        return browser

    def run(self):
        browser = self._login()
        next_link = self.group.url

        min_time = None
        while next_link:

            try:
                browser.open(next_link)
                page_text = str(browser.get_current_page())
            except requests.exceptions.ConnectionError as ex:
                logging.error("Get %s fail: %s", next_link, ex)
                time.sleep(10)
                continue

            def check_func(obj: Toppic):
                nonlocal min_time
                m = max(obj.time, self.min_time)
                if not min_time:
                    min_time = m
                elif m > min_time:
                    min_time = m

                    obj.group_name = self.group.name

            next_link, toppics = parse_douban_group(page_text, self.min_time, check_func)

            for tp in toppics:
                self.all_toppics.extend(toppics)
                self.all_toppics_id.add(tp.toppic_id)

            if next_link:
                time.sleep(random.randint(8, 12))

        self.all_toppics = filter_toppics(self.all_toppics, self.config)
        save_data_file(self.all_toppics, self.data_file)

        if min_time:
            self.min_time = min_time
        self.save_runtime_data()


def filter_toppics(tps: [Toppic], config: ConfigFile, recale_score=False) -> [Toppic]:
    filterKeywordsAndScores = config.get_keywords('keywords')

    for tp in tps:
        if tp.score is None or recale_score:
            tp.score = calulate_score(tp.title, filterKeywordsAndScores)

    tps = sorted(tps, key=lambda tp: tp.time, reverse=True)

    all_toppics_id = set()
    all_toppic_titles = set()
    all_toppics = []

    for tp in tps:
        if tp.toppic_id not in all_toppics_id and tp.title not in all_toppic_titles:
            all_toppics.append(tp)

        all_toppics_id.add(tp.toppic_id)
        all_toppic_titles.add(tp.title)

    score_min = int(config.get("score_min", section='Spider'))
    data_days = int(config.get('data_days', section='Spider'))

    def f(tp: Toppic) -> bool:
        return (tp.time > (datetime.datetime.now() - datetime.timedelta(days=data_days)) and tp.score >= score_min)

    if len(all_toppics) > 0:
        all_toppics = list(filter(f, all_toppics))

    return all_toppics


def calulate_score(title: str, expectedKeywords):
    keywords = list((jieba.cut_for_search(title)))
    s = set(keywords)
    Keywords = set(expectedKeywords.keys())

    selectedKeywords = Keywords.intersection(s)
    score = 0
    for key in selectedKeywords:
        score += expectedKeywords[key]

    return score
