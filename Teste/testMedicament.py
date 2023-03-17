from Domain.medicament import Medicament
from Repository.repositoryJson import RepositoryJson


def testMedicament():
    open("testMedicament.json", "w").close()
    f = "testMedicament.json"

    medicamentRepository = RepositoryJson(f)

    assert medicamentRepository.read() == []

    medicament = Medicament("1", "parasinus", "rof", 25, "nu")

    medicamentRepository.adauga(medicament)

    assert medicamentRepository.read("1") == medicament

    medicament = Medicament("2", "parasinus", "rof", 25, "nu")

    medicamentRepository.adauga(medicament)

    assert medicamentRepository.read("2") == medicament

    medicamentRepository.sterge("2")

    assert medicamentRepository.read("2") is None

    medicament = Medicament("1", "paracetamol", "rof", 65, "da")

    medicamentRepository.modifica(medicament)

    assert medicamentRepository.read("1") == medicament
