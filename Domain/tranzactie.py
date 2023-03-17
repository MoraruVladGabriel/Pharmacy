from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class Tranzactie(Entitate):
    idMedicament: str
    idCard: str
    nrBucati: int
    dataOra: str
