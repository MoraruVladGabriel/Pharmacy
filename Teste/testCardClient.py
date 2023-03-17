from Domain.cardClient import CardClient
from Repository.repositoryJson import RepositoryJson


def testCardClient():
    open("testCard.json", "w").close()
    f = "testCard.json"

    cardRepository = RepositoryJson(f)

    assert cardRepository.read() == []

    card = CardClient("1",
                      "andrei",
                      "flaviu",
                      "12.12.2002",
                      "15.11.2021",
                      7675849385743)

    cardRepository.adauga(card)

    assert cardRepository.read("1") == card

    card = CardClient("2",
                      "andrei",
                      "flaviu",
                      "12.12.2002",
                      "15.11.2021",
                      8458473859434)

    cardRepository.adauga(card)

    assert cardRepository.read("2") == card

    cardRepository.sterge("2")

    assert cardRepository.read("2") is None

    card = CardClient("1",
                      "marius",
                      "andrei",
                      "12.12.2001",
                      "15.11.2021",
                      93845903485347)

    cardRepository.modifica(card)

    assert cardRepository.read("1") == card
