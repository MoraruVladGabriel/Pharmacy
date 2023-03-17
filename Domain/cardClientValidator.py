from Domain.cardClient import CardClient
from Repository.repository import Repository


class CardClientValidator:
    def __init__(self, cardClientRepository: Repository):
        self.__cardClientRepository = cardClientRepository

    def valideaza(self, cardClient: CardClient):
        erori = []

        if len(str(cardClient.CNP)) != 13:
            erori.append("CNP-ul trebuie sa fie de exact 13 cifre")

        if isinstance(int(cardClient.idEntitate), int) is False:
            erori.append("Id-ul trebuie sa fie de forma unui numar!")

        for card in self.__cardClientRepository.read():
            if card.nume == cardClient.nume and \
                    card.prenume == cardClient.prenume:
                erori.append("Exista deja un card pe acest nume!")

        for card in self.__cardClientRepository.read():
            if card.CNP == cardClient.CNP and \
                (cardClient.nume != card.nume or
                 cardClient.prenume != card.prenume):
                erori.append("CNP-ul exista deja!")

        if len(erori) > 0:
            raise ValueError(erori)
