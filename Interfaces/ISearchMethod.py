from abc import ABCMeta, abstractmethod, abstractproperty


class ISearchMethod:
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self): raise NotImplementedError
