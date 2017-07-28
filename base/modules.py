import datetime
import logging
import re

TIME_OUT_OF_DATE = 1
TOPPIC_EXIST = 2
NO_LIMIT = 0


class DoubanGroup:
    def __init__(self):
        self.id = None
        self.url = None
        self.name = None

    def __setattr__(self, key, value):
        if key == 'url' and isinstance(value, str):
            super(DoubanGroup, self).__setattr__(key, value)
            self.id = re.match(r'https://www.douban.com/group/([\d\w+]+)', value).group(1)
        else:
            super(DoubanGroup, self).__setattr__(key, value)


class Toppic:
    TIME_DETAIL_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
    TIME_SIMPLE_FORMAT = "%Y-%m-%d %H:%M"

    def __init__(self):
        self.toppic_id = None
        self.group_name = None
        self.link = None
        self.title = None
        self.score = None
        self.time = None

    def __repr__(self):
        return repr(self.__dict__)

    def to_dict(self):
        return self.__dict__

    def load_from(self, d: dict):
        for k, v in d.items():
            if hasattr(self, k):
                setattr(self, k, v)
        return self

    def __eq__(self, other):
        for k, _ in self.__dict__.items():
            if getattr(self, k) != getattr(other, k):
                return False

        return True

    def __setattr__(self, key, value):
        if key == 'time' and isinstance(value, str):
            self.time = datetime.datetime.strptime(value, self.TIME_DETAIL_FORMAT)
        elif key == 'link' and isinstance(value, str):
            super(Toppic, self).__setattr__(key, value)
            try:
                self.toppic_id = int(re.match(r'https://www.douban.com/group/topic/(\d+)', value).group(1))
            except AttributeError as ex:
                logging.error("Fail to set toppic id:%s", str(ex))
        else:
            super(Toppic, self).__setattr__(key, value)
