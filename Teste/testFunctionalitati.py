from Domain.medicamentValidator import MedicamentValidator
from Repository.repositoryInMemory import RepositoryInMemory
from Service.medicamentService import MedicamentService
from Service.undoRedoService import UndoRedoService


def testFunctionalitatiMed():
    undoRedoService = UndoRedoService()
    repMed = RepositoryInMemory()
    valMed = MedicamentValidator()
    repTranz = RepositoryInMemory()
    medicamentService = MedicamentService(repMed, valMed, repTranz,
                                          undoRedoService)

    medicamentService.adauga("1", "parasinus", "rof", 20, "nu")

    assert len(medicamentService.getAll()) == 1

    # cautareText
    lista = medicamentService.cautareMed("xa")

    assert len(lista) == 0

    lista = medicamentService.cautareMed("a")

    assert len(lista) == 1

    # scumpire
    medicamentService.scumpire(50, 30)

    medicament = repMed.read("1")

    assert medicament.pret == 30
