import abc


class BaseTrader(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def prepare(self, **kwargs):
        """"""

    @property
    @abc.abstractmethod
    def balance(self):
        """"""

    @property
    @abc.abstractmethod
    def position(self):
        """"""

    @abc.abstractmethod
    def buy(self, **kwargs):
        """"""

    @abc.abstractmethod
    def sell(self, **kwargs):
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
