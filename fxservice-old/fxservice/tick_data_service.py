from abc import abstractmethod, ABCMeta


class TickDataService(metaclass=ABCMeta):
    @abstractmethod
    def get_lasted_bar(self, default_value):
        pass

    @abstractmethod
    def get_bars(self, start, end):
        pass

    @abstractmethod
    def get_count(self):
        pass

    @abstractmethod
    def push_data(self, candles):
        pass
