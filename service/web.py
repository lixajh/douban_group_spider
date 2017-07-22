import os.path
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import logging

from watchdog.events import FileSystemEvent

from base.log import init_logging
from base.modules import Toppic
from base.serializer import load_data_file, data_dir_path
from base.service import WebService
from base.watcher import DirectoryWatcher

from aiohttp import web


class MyWebService(WebService):
    def __init__(self):
        super(MyWebService, self).__init__()

        self.toppics_for_group = {}
        self.all_toppics = {}
        self.all_toppic_titles = set()
        self.sorted_toppics_list = []

        self.data_dir = data_dir_path()
        self.watcher = DirectoryWatcher(self.data_dir, self._data_file_update)
        self.watcher.run()

        init_files = filter(lambda x: x.endswith('.json'), os.listdir(self.data_dir))
        for file in init_files:
            self._data_file_update(FileSystemEvent(os.path.join(self.data_dir, file)))

        self.router.add_route('GET', '/', self.index)
        self.router.add_route('GET', '/zufang/all', self.toppics)

    def _data_file_update(self, event):
        if not event.src_path.endswith('.json') or event.src_path.endswith('_spider.json'):
            return

        file_name = os.path.split(event.src_path)[1]
        group_name = os.path.splitext(file_name)[0]

        logging.info("load data file: %s", event.src_path)
        self.toppics_for_group[group_name] = load_data_file(event.src_path)
        for toppic in self.toppics_for_group[group_name]:
            #过滤掉不同豆瓣组的同一贴子（一般标题和内容完全相同）
            if toppic.title in self.all_toppic_titles:
                continue
            else:
                self.all_toppics[toppic.toppic_id] = toppic
                self.all_toppic_titles.add(toppic.title)

        self.sorted_toppics_list = sorted(self.all_toppics.values(), key=lambda toppic: toppic.time, reverse=True)

    async def index(self, request):
        return web.Response(body=b'Hello, home page!')

    async def toppics(self, request):
        template_html = open(os.path.join(os.path.dirname(__file__), 'toppic_list.html')).read()
        item_html = '''
        <li>
					<div class="list">
						<div class="zufang_content">
							<h5>{group_name} <a href="{link}"> {title} </a></h5>
							<a class="time">{time}</a>
						</div>

					</div>
				</li>
		'''

        l = [item_html.format(group_name='[%s]' % (toppic.group_name),
                              title="%s" % (toppic.title),
                              time=toppic.time.strftime(Toppic.TIME_SIMPLE_FORMAT),
                              link=toppic.link)
             for toppic in self.sorted_toppics_list]
        if len(l) == 0:
            return web.HTTPServiceUnavailable()

        return web.Response(content_type='text/html', text=template_html.replace("{content}", '\n'.join(l)))


if __name__ == "__main__":
    init_logging("INFO")
    s = MyWebService()
    s.run()
