from Domain.entitate import Entitate
from Domain.undoRedoOperation import UndoRedoOperation
from Repository.repository import Repository


class CascadeDelete(UndoRedoOperation):
    def __init__(self, repository1: Repository, repository2: Repository,
                 obiectSters: Entitate, obiecteSterse: list[Entitate]):
        self.__repository1 = repository1
        self.__repository2 = repository2
        self.__obiectSters = obiectSters
        self.__obiecteSterse = obiecteSterse

    def doUndo(self):
        self.__repository1.adauga(self.__obiectSters)

        for entitate in self.__obiecteSterse:
            self.__repository2.adauga(entitate)

    def doRedo(self):

        self.__repository1.sterge(self.__obiectSters.idEntitate)

        for entitate in self.__obiecteSterse:
            self.__repository2.sterge(entitate.idEntitate)
