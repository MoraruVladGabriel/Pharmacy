from Domain.tranzactie import Tranzactie
from Repository.repository import Repository


class TranzactieValidator:
    def __init__(self, cardClientRepository: Repository,
                 medicamentRepository: Repository):
        self.__cardClientRepository = cardClientRepository
        self.__medicamentRepository = medicamentRepository

    def valideaza(self, tranzactie: Tranzactie):
        erori = []
        if tranzactie.nrBucati < 0:
            erori.append("Numarul de bucati trebuie sa fie pozitiv!")
        if self.__medicamentRepository.read(tranzactie.idMedicament) is None:
            erori.append("Nu exista niciun medicament cu id-ul dat!")
        if int(tranzactie.idCard) != 0:
            if self.__cardClientRepository.read(tranzactie.idCard) is None:
                erori.append("Nu exista niciun card client cu id-ul dat!")
        if len(erori) > 0:
            raise ValueError(erori)
