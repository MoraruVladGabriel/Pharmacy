from Teste.testCardClient import testCardClient
from Teste.testFunctionalitati import testFunctionalitatiMed
from Teste.testGenerator import testGenerator
from Teste.testMedicament import testMedicament
from Teste.testTranzactie import testTranzactie
from Teste.testUndoRedo import testUndoRedo


def testAll():
    testCardClient()
    testMedicament()
    testTranzactie()
    testFunctionalitatiMed()
    testGenerator()
    testUndoRedo()
