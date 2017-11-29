from abc import abstractmethod, ABCMeta


class BrokerService(metaclass=ABCMeta):
    @abstractmethod
    def get_bar(self, time, num_bars):
        pass
