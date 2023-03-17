from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class CardClient(Entitate):
    nume: str
    prenume: str
    dataNasterii: str
    dataInregistarii: str
    CNP: int
