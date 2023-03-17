from Domain.entitate import Entitate
from Domain.undoRedoOperation import UndoRedoOperation
from Repository.repository import Repository


class MultiModifyOperation(UndoRedoOperation):
    def __init__(self, repositoy: Repository,
                 listObiecteVechi: list[Entitate],
                 listObiecteNoi: list[Entitate]):
        self.__repository = repositoy
        self.__listObiecteVechi = listObiecteVechi
        self.__listObiecteNoi = listObiecteNoi

    def doUndo(self):
        for entitate in self.__listObiecteVechi:
            self.__repository.modifica(entitate)

    def doRedo(self):
        for entitate in self.__listObiecteNoi:
            self.__repository.modifica(entitate)
