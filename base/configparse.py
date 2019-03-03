# -*- coding:utf-8 -*-
import configparser


class ConfigFile:
    def __init__(self, path):
        self.config = configparser.ConfigParser()
        self.config.read(path,encoding="utf-8-sig")

    def get(self, itemKey, section='DEFAULT'):
        return self[section][itemKey]

    def getbool(self, itemKey, section='DEFAULT'):
        return self.config.getboolean(section, itemKey)


    def __getattr__(self, item):
        return self.config[item]

    def __getitem__(self, item):
        return self.__getattr__(item)


class DoubanGroupConfig(ConfigFile):
    def get_keywords(self, itemKey, section='DEFAULT') -> dict:
        value = self[section][itemKey]

        d = {}

        lines = value.split('\n')
        for line in lines:
            line = line.rstrip().lstrip()
            if line == "":
                continue

            name_and_score = line.split("=")
            name, score = name_and_score[0], int(name_and_score[1])
            d[name] = score

        return d


def test_ConfigFile():
    import os.path
    PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))

    f = DoubanGroupConfig(os.path.join(PROJECT_DIR, 'config.ini'))
    loglevel = f['DEFAULT']['LogLevel']

    assert isinstance(loglevel, str)

    kc = f.get_keywords('keywords')
    assert isinstance(kc, dict) and len(kc) > 0


if __name__ == '__main__':
    test_ConfigFile()
