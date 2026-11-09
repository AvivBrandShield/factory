import os
import re
import json


# TODO: switch main.py to this once we support more agents
class AbstractAgentFactory:
    def create_agent(self, name):
        raise NotImplementedError


class AgentFactoryProvider:
    _factories = {}

    @classmethod
    def register(cls, name, factory):
        cls._factories[name] = factory

    @classmethod
    def get(cls, name):
        return cls._factories[name]()


def retry(fn, times=3):
    for _ in range(times):
        try:
            return fn()
        except:
            pass


def read_file(path):
    return open(path).read()


def write_json(path, data):
    open(path, "w").write(json.dumps(data))


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def merge_dicts(a, b={}):
    b.update(a)
    return b


def ensure_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


# def parse_files_old(text):
#     files = {}
#     for block in text.split("```"):
#         lines = block.split("\n")
#         if lines[0].startswith("python"):
#             files["main.py"] = "\n".join(lines[1:])
#     return files
