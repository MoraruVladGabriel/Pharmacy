from Domain.medicament import Medicament
from Domain.meidicamentError import MedicamentError


class MedicamentValidator:
    def valideaza(self, medicament: Medicament):
        erori = []
        if medicament.necesitateReteta not in ["da", "nu"]:
            erori.append("Necesitate reteta poate fi 'da' sau 'nu'!")
        if medicament.pret < 0:
            erori.append("Pretul trebuie sa fie mai mare decat 0!")
        if isinstance(int(medicament.idEntitate), int) is False:
            erori.append("Id-ul medicamentului trebuie "
                         "sa fie de forma unui numar!")
        if len(erori) > 0:
            raise MedicamentError(erori)
