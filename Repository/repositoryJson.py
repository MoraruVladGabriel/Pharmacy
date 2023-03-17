import jsonpickle

from Domain.entitate import Entitate
from Repository.repositoryInMemory import RepositoryInMemory


class RepositoryJson(RepositoryInMemory):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def __readfile(self):
        try:
            with open(self.filename, "r") as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __writeFile(self):
        with open(self.filename, "w") as f:
            f.write(jsonpickle.dumps(self.entitati, indent=4))

    def read(self, idEntitate=None):
        self.entitati = self.__readfile()
        return super().read(idEntitate)

    def adauga(self, entitate: Entitate):
        self.entitati = self.__readfile()
        super().adauga(entitate)
        self.__writeFile()

    def sterge(self, idEntitate: str):
        self.entitati = self.__readfile()
        super().sterge(idEntitate)
        self.__writeFile()

    def modifica(self, entitate: Entitate):
        self.entitati = self.__readfile()
        super().modifica(entitate)
        self.__writeFile()
