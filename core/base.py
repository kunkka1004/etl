from abc import ABC


class BaseWorker(ABC):

    def __init__(self, timestamp, **kwargs):
        pass

    def process(self):
        pass
