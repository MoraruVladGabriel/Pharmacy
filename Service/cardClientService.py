from Domain.addOpertion import AddOperation
from Domain.cardClient import CardClient
from Domain.cardClientValidator import CardClientValidator
from Domain.deleteOperation import DeleteOperation
from Domain.modifyOperation import ModifyOperation
from Repository.repository import Repository
from Service.tranzactieService import TranzactieService
from Service.undoRedoService import UndoRedoService


class CardClientService:
    def __init__(self, cardClientRepository: Repository,
                 cardClientValidator: CardClientValidator,
                 tranzactieService: TranzactieService,
                 tranzactieRepository: Repository,
                 undoRedoService: UndoRedoService):
        self.__cardClientRepository = cardClientRepository
        self.__cardClientValidator = cardClientValidator
        self.__tranzactieService = tranzactieService
        self.__tranzactieRepository = tranzactieRepository
        self.__undoRedoService = undoRedoService

    def getAll(self):
        return self.__cardClientRepository.read()

    def adauga(self, idCard,
               nume,
               prenume,
               dataNasterii,
               dataInregistrarii,
               CNP):
        """
        Adauga un card client.
        :param idCard: str
        :param nume: str
        :param prenume: str
        :param dataNasterii: date
        :param dataInregistrarii: date
        :param CNP: int
        :return:
        """
        cardClient = CardClient(idCard,
                                nume,
                                prenume,
                                dataNasterii,
                                dataInregistrarii,
                                CNP)
        self.__cardClientValidator.valideaza(cardClient)
        self.__cardClientRepository.adauga(cardClient)
        self.__undoRedoService.addUndoOperation(AddOperation(
            self.__cardClientRepository, cardClient))

    def sterge(self, idCard):
        """
        Sterge un card client.
        :param idCard: str
        :return:
        """
        cardClient = self.__cardClientRepository.read(idCard)
        self.__cardClientRepository.sterge(idCard)
        self.__undoRedoService.addUndoOperation(
            DeleteOperation(self.__cardClientRepository, cardClient))

    def modifica(self, idCard,
                 nume,
                 prenume,
                 dataNasterii,
                 dataInregistrarii,
                 CNP):
        """
        Modifica datele unui card client.
        :param idCard: str
        :param nume: str
        :param prenume: str
        :param dataNasterii: date
        :param dataInregistrarii: date
        :param CNP: int
        :return:
        """
        cardClientVechi = self.__cardClientRepository.read(idCard)
        cardClient = CardClient(idCard,
                                nume,
                                prenume,
                                dataNasterii,
                                dataInregistrarii,
                                CNP)
        self.__cardClientValidator.valideaza(cardClient)
        self.__cardClientRepository.modifica(cardClient)
        self.__undoRedoService.addUndoOperation(
            ModifyOperation(self.__cardClientRepository, cardClientVechi,
                            cardClient))

    def cautareClineti(self, text):
        """
        Cautare carduri ce contin text.
        :param text: str
        :return:
        """
        rezultat = []
        for card in self.__cardClientRepository.read():
            if text in card.idEntitate or text in card.nume \
                    or text in card.prenume or text in str(card.CNP) \
                    or text in str(card.dataNasterii) or \
                    text in str(card.dataInregistrarii):
                rezultat.append(card)

        return rezultat

    def ordDupaValReducerilor(self):
        """
        Ordoneaza cardurile dupa reducerea aplicata.
        :return:
        """
        reduceriPerCard = {}
        rezultat = []

        for card in self.__cardClientRepository.read():
            reduceriPerCard[card.idEntitate] = []

        for tranzactie in self.__tranzactieRepository.read():
            lista = self.__tranzactieService.calculReducere(tranzactie.idCard)
            reducere = lista[1]
            reduceriPerCard[tranzactie.idCard].append(reducere)

        for idCard in reduceriPerCard:
            reduceri = reduceriPerCard[idCard]
            rezultat.append({
                "card": self.__cardClientRepository.read(idCard),
                "reducere": sum(reduceri)
            })

        return sorted(rezultat,
                      key=lambda reduceri: reduceri["reducere"],
                      reverse=True)

    def stergeCascada(self, idCard):
        """
        Sterge in cascada un card.
        :param idCard: str
        :return:
        """
        if self.__cardClientRepository.read(idCard) is None:
            raise KeyError("Nu exista niciun card cu id-ul dat!")
        for tranz in self.__tranzactieRepository.read():
            if idCard == tranz.idCard:
                self.__tranzactieRepository.sterge(tranz.idCard)
        self.__cardClientRepository.sterge(idCard)
