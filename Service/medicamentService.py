import random
from Domain.addOpertion import AddOperation
from Domain.cascadeDelete import CascadeDelete
from Domain.deleteOperation import DeleteOperation
from Domain.medicament import Medicament
from Domain.medicamentValidator import MedicamentValidator
from Domain.modifyOperation import ModifyOperation
from Domain.multiModifyOperation import MultiModifyOperation
from Repository.repository import Repository
from Service.undoRedoService import UndoRedoService
from utils import mySort


class MedicamentService:
    def __init__(self, medicamentRepository: Repository,
                 medicamentValidator: MedicamentValidator,
                 tranzactieRepository: Repository,
                 undoRedoService: UndoRedoService):
        self.__medicamentRepository = medicamentRepository
        self.__medidamentValidator = medicamentValidator
        self.__tranzactieRepository = tranzactieRepository
        self.__undoRedoService = undoRedoService

    def getAll(self):
        return self.__medicamentRepository.read()

    def adauga(self, idMedicament, nume, producator, pret, necesitateReteta):
        """
        Adauga un medicament.
        :param idMedicament: str
        :param nume: str
        :param producator: str
        :param pret: float
        :param necesitateReteta: str
        :return:
        """
        medicament = Medicament(idMedicament,
                                nume,
                                producator,
                                pret,
                                necesitateReteta)
        self.__medidamentValidator.valideaza(medicament)
        self.__medicamentRepository.adauga(medicament)
        self.__undoRedoService.addUndoOperation(AddOperation(
            self.__medicamentRepository, medicament))

    def sterge(self, idMedicament):
        """
        Sterge un medicament.
        :param idMedicament: str
        :return:
        """
        medicament = self.__medicamentRepository.read(idMedicament)
        self.__medicamentRepository.sterge(idMedicament)
        self.__undoRedoService.addUndoOperation(
            DeleteOperation(self.__medicamentRepository, medicament))

    def modifica(self, idMedicament, nume, producator, pret, necesitateReteta):
        """
        Modifica datele unui medicament
        :param idMedicament: str
        :param nume: str
        :param producator: str
        :param pret: float
        :param necesitateReteta: str
        :return:
        """
        medicamentVechi = self.__medicamentRepository.read(idMedicament)
        medicament = Medicament(idMedicament,
                                nume,
                                producator,
                                pret,
                                necesitateReteta)
        self.__medidamentValidator.valideaza(medicament)
        self.__medicamentRepository.modifica(medicament)
        self.__undoRedoService.addUndoOperation(
            ModifyOperation(self.__medicamentRepository, medicamentVechi,
                            medicament))

    def ordMedDupaNrVanzari(self):
        """
        Ordoneaza medicamentele dupa nr de vanzari
        :return:
        """
        nrVanzPerMed = {}
        rezultat = []

        for medicament in self.__medicamentRepository.read():
            nrVanzPerMed[medicament.idEntitate] = []
        for tranzactie in self.__tranzactieRepository.read():
            nrVanzPerMed[tranzactie.idMedicament].append(tranzactie.nrBucati)

        for idMedicament in nrVanzPerMed:
            nrVanzari = nrVanzPerMed[idMedicament]
            rezultat.append({
                "medicament": self.__medicamentRepository.read(idMedicament),
                "nrBucati": sum(nrVanzari)
            })

        return mySort(rezultat,
                      key=lambda vanzariMed: vanzariMed["nrBucati"],
                      reverse=True)

    def cautareMed(self, text):
        """
        Cauta un text prin campurile medicamentelor.
        :param text: str
        :return: medicamentele care contin acel text.
        """
        rezultat = []

        for med in self.__medicamentRepository.read():
            if text in med.idEntitate or text in med.nume \
                    or text in med.producator or text in str(med.pret) \
                    or text in med.necesitateReteta:
                rezultat.append(med)

        return rezultat

    def scumpire(self, procent, valoare):
        """
        Scumpeste medicamentele cu prop data.
        :param procent: float
        :param valoare: float
        :return:
        """
        listObiecteVechi = list(filter(
            lambda x: x.pret < valoare, self.__medicamentRepository.read()))
        listObiecteNoi = []

        for med in self.__medicamentRepository.read():
            if med.pret < valoare:
                med.pret += med.pret * procent / 100
                self.__medicamentRepository.modifica(med)
                listObiecteNoi.append(
                    self.__medicamentRepository.read(med.idEntitate))
        self.__undoRedoService.addUndoOperation(
            MultiModifyOperation(self.__medicamentRepository,
                                 listObiecteVechi,
                                 listObiecteNoi))

    def stergeCascada(self, idMed):
        """
        Sterge in cascada un medicament.
        :param idMed: str
        :return:
        """
        tranzactiiSterse = []

        if self.__medicamentRepository.read(idMed) is None:
            raise KeyError("Nu exista niciun medicament cu id-ul dat!")

        for tranz in self.__tranzactieRepository.read():
            if idMed == tranz.idMedicament:
                tranzactiiSterse.append(tranz)
                self.__tranzactieRepository.sterge(tranz.idMedicament)

        self.__undoRedoService.addUndoOperation(
            CascadeDelete(self.__medicamentRepository,
                          self.__tranzactieRepository,
                          self.__medicamentRepository.read(idMed),
                          tranzactiiSterse))

        self.__medicamentRepository.sterge(idMed)

    def generatorMedicamente(self, number):
        numePos = ["parasinus", "theraflu", "aspirina",
                   "nurofen", "vitaminaC", "Coxtral",
                   "panadlo", "XANAX"]
        prdPos = ["asdas", "asdsa", "sadasd", "gfjghj", "fdlgkdfgl",
                  "sdhgfhlgj", "sdfgb87hsdf", "sdfgddgsdfsdfsdfm",
                  "sdfdsjnkdnvn", "sdfdpgkok", "kjnjknjncv"]
        pretPos = [34, 35, 46, 678, 67, 45, 56, 87, 23, 654, 39, 78]
        retataPos = ["da", "nu"]
        id = 100
        for i in range(number):
            while self.__medicamentRepository.read(str(id)) is not None:
                id += 1
            self.adauga(str(id),
                        random.choice(numePos),
                        random.choice(prdPos),
                        random.choice(pretPos),
                        random.choice(retataPos))
            id += 1
