from Domain.cardClientValidator import CardClientValidator
from Domain.medicamentValidator import MedicamentValidator
from Domain.tranzactieValidator import TranzactieValidator
from Repository.repositoryJson import RepositoryJson
from Service.cardClientService import CardClientService
from Service.medicamentService import MedicamentService
from Service.tranzactieService import TranzactieService
from Service.undoRedoService import UndoRedoService
from Teste.testAll import testAll
from UI.consola import Consola


def main():
    testAll()
    undoRedoService = UndoRedoService()
    medicamentRepositoryJson = RepositoryJson("medicamente.json")
    medicamentValidator = MedicamentValidator()
    tranzactieRepositoryJson = RepositoryJson("tranzactii.json")
    medicamentService = MedicamentService(medicamentRepositoryJson,
                                          medicamentValidator,
                                          tranzactieRepositoryJson,
                                          undoRedoService)

    cardClientRepositoryJson = RepositoryJson("carduriClienti.json")
    cardClientValidator = CardClientValidator(cardClientRepositoryJson)
    tranzactieValidator = TranzactieValidator(cardClientRepositoryJson,
                                              medicamentRepositoryJson)
    tranzactieService = TranzactieService(tranzactieRepositoryJson,
                                          tranzactieValidator,
                                          medicamentRepositoryJson,
                                          cardClientRepositoryJson,
                                          undoRedoService)
    cardClientService = CardClientService(cardClientRepositoryJson,
                                          cardClientValidator,
                                          tranzactieService,
                                          tranzactieRepositoryJson,
                                          undoRedoService)

    consola = Consola(medicamentService, cardClientService, tranzactieService,
                      medicamentRepositoryJson, undoRedoService)

    consola.runMenu()


main()
