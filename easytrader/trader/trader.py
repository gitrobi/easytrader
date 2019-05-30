import abc


class BaseTrader(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def prepare(self):
        """"""

    @abc.abstractmethod
    def balance(self):
        """"""

    @abc.abstractmethod
    def position(self):
        """"""

    @abc.abstractmethod
    def buy(self):
        """"""

    @abc.abstractmethod
    def sell(self):
        """"""

    @abc.abstractmethod
    def cancel_entrusts(self):
        """"""

    @abc.abstractmethod
    def cancel_entrust(self):
        """"""

    @abc.abstractmethod
    def exit(self):
        """"""
