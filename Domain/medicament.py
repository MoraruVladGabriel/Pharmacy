from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class Medicament(Entitate):
    nume: str
    producator: str
    pret: float
    necesitateReteta: str
