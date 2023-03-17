from Domain.cardClientValidator import CardClientValidator
from Domain.medicamentValidator import MedicamentValidator
from Domain.tranzactieValidator import TranzactieValidator
from Repository.repositoryJson import RepositoryJson
from Service.cardClientService import CardClientService
from Service.medicamentService import MedicamentService
from Service.tranzactieService import TranzactieService
from Service.undoRedoService import UndoRedoService


def testUndoRedo():
    open("testMedicament.json", "w").close()
    f = "testMedicament.json"

    open("testCard.json", "w").close()
    g = "testMedicament.json"

    open("testTranzactie.json", "w").close()
    h = "testTranzactie.json"

    medicamentRepositoryJson = RepositoryJson(f)
    cardRepositoryJson = RepositoryJson(g)
    tranzactieRepositoryJson = RepositoryJson(h)

    undoRedoService = UndoRedoService()

    medicamentValidator = MedicamentValidator()
    cardClientValidator = CardClientValidator(cardRepositoryJson)
    tranzactieValidator = TranzactieValidator(cardRepositoryJson,
                                              medicamentRepositoryJson)

    medicamentService = MedicamentService(medicamentRepositoryJson,
                                          medicamentValidator,
                                          tranzactieRepositoryJson,
                                          undoRedoService)
    tranzactieService = TranzactieService(tranzactieRepositoryJson,
                                          tranzactieValidator,
                                          medicamentRepositoryJson,
                                          cardRepositoryJson,
                                          undoRedoService)
    cardService = CardClientService(cardRepositoryJson,
                                    cardClientValidator,
                                    tranzactieService,
                                    tranzactieRepositoryJson,
                                    undoRedoService)

    # test undo + redo CRUD medicament

    medicamentService.adauga('1', 'xanax', 'max', 59, 'da')

    undoRedoService.undo()

    assert len(medicamentRepositoryJson.read()) == 0

    undoRedoService.redo()

    assert len(medicamentRepositoryJson.read()) == 1

    medicamentService.sterge('1')

    undoRedoService.undo()

    assert len(medicamentRepositoryJson.read()) == 1

    undoRedoService.redo()

    assert len(medicamentRepositoryJson.read()) == 0

    medicamentService.adauga('1', 'xanax', 'max', 59, 'da')

    medicamentService.modifica('1', 'paracetamol', 'fimp', 100, 'nu')

    undoRedoService.undo()

    medicament = medicamentRepositoryJson.read('1')

    assert medicament.nume == 'xanax'
    assert medicament.producator == 'max'
    assert medicament.pret == 59
    assert medicament.necesitateReteta == 'da'

    undoRedoService.redo()

    medicament = medicamentRepositoryJson.read('1')

    assert medicament.nume == 'paracetamol'
    assert medicament.producator == 'fimp'
    assert medicament.pret == 100
    assert medicament.necesitateReteta == 'nu'

    medicamentService.scumpire(25, 110)

    undoRedoService.undo()

    medicament = medicamentRepositoryJson.read('1')

    assert medicament.pret == 100

    undoRedoService.redo()

    medicament = medicamentRepositoryJson.read('1')

    assert medicament.pret == 125

    # test undo + redo CRUD tranzactie

    tranzactieService.adauga('1', '1', '0', 7, '13.12.2021 14:54')

    undoRedoService.undo()

    assert len(tranzactieRepositoryJson.read()) == 0

    undoRedoService.redo()

    assert len(tranzactieRepositoryJson.read()) == 1

    tranzactieService.modifica('1', '1', '0', 10, '13.12.2021 14:54')

    undoRedoService.undo()

    tranzactie = tranzactieRepositoryJson.read('1')

    assert tranzactie.nrBucati == 7

    undoRedoService.redo()

    tranzactie = tranzactieRepositoryJson.read('1')

    assert tranzactie.nrBucati == 10

    tranzactieService.sterge('1')

    undoRedoService.undo()

    assert len(tranzactieRepositoryJson.read()) == 1

    undoRedoService.redo()

    assert len((tranzactieRepositoryJson.read())) == 0

    undoRedoService.undo()

    tranzactieService.stergeTranzDinInterval('10.12.2021', '19.12.2021')

    undoRedoService.undo()

    assert len(tranzactieRepositoryJson.read()) == 1

    undoRedoService.redo()

    assert len(tranzactieRepositoryJson.read()) == 0

    # test stergere cascada + undo + redo

    medicamentService.adauga('2', 'paracetamol', 'maxos', 23, 'nu')

    tranzactieService.adauga('1', '1', '0', 7, '13.12.2021 15:32')

    assert len(medicamentRepositoryJson.read()) == 2
    assert len(tranzactieRepositoryJson.read()) == 1

    medicamentService.stergeCascada('1')

    assert len(medicamentRepositoryJson.read()) == 1
    assert len(tranzactieRepositoryJson.read()) == 0

    undoRedoService.undo()

    assert len(medicamentRepositoryJson.read()) == 2
    assert len(tranzactieRepositoryJson.read()) == 1

    undoRedoService.redo()

    assert len(medicamentRepositoryJson.read()) == 1
    assert len(tranzactieRepositoryJson.read()) == 0
