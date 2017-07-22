import os.path
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import datetime

from base.log import init_logging
from base.modules import DoubanGroup
from base.service import Service
from crawler.spider import DoubanGroupSpider
import time


class SpiderService(Service):
    def __init__(self):
        super(SpiderService, self).__init__()
        self.interval = datetime.timedelta(seconds=int(self.config['Spider']['interval']))
        name_and_urls = self.config['Spider']['group'].split("\n")
        self.groups = []

        for line in name_and_urls:
            line = line.rstrip().lstrip()
            if line == '':
                continue
            group = DoubanGroup()
            group.name, group.url = list(map(lambda x: x.rstrip().lstrip(), line.split(',')))
            self.groups.append(group)

    def run(self):
        next_time = datetime.datetime.now()

        while True:
            current_time = datetime.datetime.now()
            if current_time < next_time:
                time.sleep((next_time - current_time).seconds)
                continue

            next_time = current_time + self.interval

            threads = [DoubanGroupSpider(self.config, group) for group in self.groups]
            for thread in threads:
                thread.start()
                thread.join()



if __name__ == "__main__":
    init_logging("DEBUG")
    s = SpiderService()
    s.run()
