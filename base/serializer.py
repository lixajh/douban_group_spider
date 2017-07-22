import datetime
import json
import os

from base.modules import Toppic, DoubanGroup

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))


def serialize_instance(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime(Toppic.TIME_DETAIL_FORMAT)

    return obj


def data_file_path(group: DoubanGroup) -> str:
    return os.path.join(PROJECT_DIR, "data", group.id + '.json')


def data_dir_path() -> str:
    return os.path.join(PROJECT_DIR, "data/")


def load_data_file(file_path: str) -> [Toppic]:
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            text = f.read()
            if text == '':
                return []

            arr = json.loads(text)
            assert (isinstance(arr, list))

            arr = list(map(lambda a: Toppic().load_from(a), arr))
            return arr
    return []


def save_data_file(l: [Toppic], file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'w') as f:
        d = list(map(lambda obj: obj.to_dict(), l))
        text = json.dumps(d, default=serialize_instance)
        f.write(text)


def test_load_file():
    a = Toppic()
    a.toppic_id = 1
    a.link = "https://www.douban.com/group/topic/105114253"
    a.score = 1

    b = Toppic()
    b.toppic_id = 2
    b.link = "https://www.douban.com/group/topic/2354"
    b.score = 10
    b.time = datetime.datetime.now()

    tempfile = '._temp'
    save_data_file([a, b], tempfile)

    result = load_data_file(tempfile)
    os.remove(tempfile)

    assert result[0] == a and result[1] == b


if __name__ == '__main__':
    test_load_file()
