import abc
import argparse
import asyncio

from aiohttp import web

from base.configparse import DoubanGroupConfig
from base.log import init_logging


class Service():
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--config', type=str, required=True, help='src config file')

        args = vars(parser.parse_args())
        config_file = args['config']
        config = DoubanGroupConfig(config_file)

        init_logging(config.get('LogLevel'))
        self.config = config

    @abc.abstractmethod
    def run(self):
        pass


class WebService(Service):
    def __init__(self):
        super(WebService, self).__init__()

        self.host, self.port = self.config.get("listen", section='WEB').split(":")
        self.routes = []
        self.loop = asyncio.get_event_loop()
        self.app = web.Application(loop=self.loop)

    @property
    def router(self):
        return self.app.router

    def run(self):
        async def init(loop, app):
            srv = await loop.create_server(app.make_handler(), self.host, self.port)
            print('Server started at http://{}:{}...'.format(self.host, self.port))
            return srv

        self.loop.run_until_complete(init(self.loop, self.app))
        self.loop.run_forever()


if __name__ == '__main__':
    config = DoubanGroupConfig("./config.ini")
