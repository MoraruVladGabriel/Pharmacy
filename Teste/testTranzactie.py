from Domain.tranzactie import Tranzactie
from Repository.repositoryJson import RepositoryJson


def testTranzactie():
    open("testTranzactie.json", "w").close()
    f = "testTranzactie.json"

    tranzactieRepository = RepositoryJson(f)

    assert tranzactieRepository.read() == []

    tranzactie = Tranzactie("1", "2", "3", 4, "12.12.2020 14:14")

    tranzactieRepository.adauga(tranzactie)

    assert tranzactieRepository.read("1") == tranzactie

    tranzactie = Tranzactie("2", "2", "3", 7, "12.12.2021 14:53")

    tranzactieRepository.adauga(tranzactie)

    assert tranzactieRepository.read("2") == tranzactie

    tranzactieRepository.sterge("2")

    assert tranzactieRepository.read("2") is None

    tranzactie = Tranzactie("1", "2", "3", 5, "11.11.2021 15:24")

    tranzactieRepository.modifica(tranzactie)

    assert tranzactieRepository.read("1") == tranzactie
