from Domain.addOpertion import AddOperation
from Domain.deleteOperation import DeleteOperation
from Domain.modifyOperation import ModifyOperation
from Domain.multiDeleteOperation import MultiDeleteOperation
from Domain.tranzactie import Tranzactie
from Domain.tranzactieValidator import TranzactieValidator
from Repository.repository import Repository
from Service.undoRedoService import UndoRedoService


class TranzactieService:
    def __init__(self, tranzactieRepository: Repository,
                 tranzactieValidator: TranzactieValidator,
                 medicamentRepository: Repository,
                 cardClientRepository: Repository,
                 undoRedoService: UndoRedoService):
        self.__tranzactieRepository = tranzactieRepository
        self.__tranzactieValidator = tranzactieValidator
        self.__medicamentRepository = medicamentRepository
        self.__cardClientRepository = cardClientRepository
        self.__undoRedoService = undoRedoService

    def getAll(self):
        return self.__tranzactieRepository.read()

    def adauga(self, idTranzactie, idMedicament, idCard, nrBucati, dataOra):
        """
        Adauga o tranzactie.
        :param idTranzactie: str
        :param idMedicament: str
        :param idCard: str
        :param nrBucati: int
        :param dataOra: date
        :return:
        """

        tranzactie = Tranzactie(idTranzactie,
                                idMedicament,
                                idCard,
                                nrBucati,
                                dataOra)
        self.__tranzactieValidator.valideaza(tranzactie)
        self.__tranzactieRepository.adauga(tranzactie)
        self.__undoRedoService.addUndoOperation(
            AddOperation(self.__tranzactieRepository, tranzactie))

    def sterge(self, idTranzactie):
        """
        Sterge o tranzactie.
        :param idTranzactie: str
        :return:
        """
        tranzactie = self.__tranzactieRepository.read(idTranzactie)
        self.__tranzactieRepository.sterge(idTranzactie)
        self.__undoRedoService.addUndoOperation(
            DeleteOperation(self.__tranzactieRepository, tranzactie))

    def modifica(self, idTranzactie, idMedicament, idCard, nrBucati, dataOra):
        """
        Modifica datele unei tranzactii.
        :param idTranzactie: str
        :param idMedicament: str
        :param idCard: str
        :param nrBucati: int
        :param dataOra: date
        :return:
        """
        tranzactieVeche = self.__tranzactieRepository.read(idTranzactie)
        tranzactie = Tranzactie(idTranzactie,
                                idMedicament,
                                idCard,
                                nrBucati,
                                dataOra)
        self.__tranzactieValidator.valideaza(tranzactie)
        self.__tranzactieRepository.modifica(tranzactie)
        self.__undoRedoService.addUndoOperation(
            ModifyOperation(self.__tranzactieRepository, tranzactieVeche,
                            tranzactie))

    def calculReducere(self, idTranzactie):
        """
        Calculeaza reducerea unei tranzactii.
        :param idTranzactie: str
        :return:
        """
        lista = []
        reducere = 0
        tranzactie = self.__tranzactieRepository.read(idTranzactie)
        medicament = self.__medicamentRepository.read(tranzactie.idMedicament)
        total = medicament.pret * tranzactie.nrBucati
        if self.__cardClientRepository.read(tranzactie.idCard) is not None \
                and tranzactie.idCard != 0:
            if medicament.necesitateReteta == "nu":
                reducere = 10 / 100 * total
                total -= reducere
            elif medicament.necesitateReteta == "da":
                reducere = 15 / 100 * total
                total -= reducere
        lista.append(total)
        lista.append(reducere)
        return lista

    def tranzDinInterval(self, data1, data2):
        """
        Determina tranzactiile dintr-un interval de zile.
        :param data1: date
        :param data2: date
        :return:
        """
        rezultat = list(filter(
            lambda x: data1 <= x.dataOra <= data2,
            self.__tranzactieRepository.read()))

        return rezultat

    def stergeTranzDinInterval(self, data1, data2):
        """
        Sterge tranzactiile dintr-un interval de zile.
        :param data1: date
        :param data2: date
        :return:
        """
        tranzactii = self.__tranzactieRepository.read()
        listObiecteSterse = list(filter(
            lambda x: data1 <= x.dataOra <= data2, tranzactii))

        for tranzactie in tranzactii:
            if data1 <= tranzactie.dataOra <= data2:
                self.__tranzactieRepository.sterge(tranzactie.idEntitate)

        self.__undoRedoService.addUndoOperation(
            MultiDeleteOperation(self.__tranzactieRepository,
                                 listObiecteSterse))
