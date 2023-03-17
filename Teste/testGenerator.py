from Domain.medicamentValidator import MedicamentValidator
from Repository.repositoryJson import RepositoryJson
from Service.medicamentService import MedicamentService
from Service.undoRedoService import UndoRedoService


def testGenerator():
    open("testGenerator.json", "w").close()
    f = "testGenerator.json"
    undoRedoService = UndoRedoService()
    tranzactieRepository = RepositoryJson(f)
    medicamentRepository = RepositoryJson(f)
    medicamentValidator = MedicamentValidator()
    medicamentService = MedicamentService(medicamentRepository,
                                          medicamentValidator,
                                          tranzactieRepository,
                                          undoRedoService)
    medicamentRepository = RepositoryJson(f)

    assert medicamentRepository.read() == []

    medicamentService.generatorMedicamente(7)

    assert len(medicamentRepository.read()) == 7
