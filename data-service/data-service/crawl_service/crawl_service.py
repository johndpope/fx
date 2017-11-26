from abc import abstractmethod, ABCMeta


class CrawlService(metaclass=ABCMeta):
    @abstractmethod
    def get(self, time, num_bars):
        pass