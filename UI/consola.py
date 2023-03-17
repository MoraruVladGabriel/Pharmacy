from datetime import datetime
from Domain.meidicamentError import MedicamentError
from Repository.repository import Repository
from Service.cardClientService import CardClientService
from Service.medicamentService import MedicamentService
from Service.tranzactieService import TranzactieService
from Service.undoRedoService import UndoRedoService


class Consola:
    def __init__(self, medicamentService: MedicamentService,
                 cardClientService: CardClientService,
                 tranzactieService: TranzactieService,
                 medicamentRepository: Repository,
                 undoRedoService: UndoRedoService):
        self.__cardClientService = cardClientService
        self.__medicamentService = medicamentService
        self.__tranzactieService = tranzactieService
        self.__medicamentRepository = medicamentRepository
        self.__undoRedoService = undoRedoService

    def runMenu(self):
        while True:
            print("1. CRUD medicamente.")
            print("2. CRUD card client.")
            print("3. CRUD tranzactie.")
            print("4. Căutare medicamente și clienți.")
            print("5. Afișarea tuturor tranzacțiilor dintr-un"
                  " interval de zile dat.")
            print("6. Afișarea medicamentelor ordonate "
                  "descrescător după numărul de vânzări.")
            print("7. Afișarea cardurilor client ordonate "
                  "descrescător după valoarea reducerilor obținute.")
            print("8. Ștergerea tuturor tranzacțiilor dintr-un "
                  "anumit interval de zile.")
            print("9. Scumpirea cu un procentaj dat a tuturor "
                  "medicamentelor cu prețul mai mic decât o valoare dată.")
            print("rnd. Random")
            print("u. Undo.")
            print("r. Redo.")
            print("c. Sterge in cascsada.")
            print("x. Iesire.")
            optiune = input("Dati optiunea: ")

            if optiune == "1":
                self.runCRUDMedicamenteMenu()
            elif optiune == "2":
                self.runCRUDCardClientMenu()
            elif optiune == "3":
                self.runCRUDTranzactieMenu()
            elif optiune == "4":
                self.uiCautare()
            elif optiune == "5":
                self.uiAfisTranzIntervalDat()
            elif optiune == "6":
                self.uiOrdMedDupaNrVanzari()
            elif optiune == "7":
                self.uiOrdCCDupaValReduceri()
            elif optiune == "8":
                self.uiStergeTranzDinInterval()
            elif optiune == "9":
                self.uiScumpesteMed()
            elif optiune == "u":
                self.__undoRedoService.undo()
            elif optiune == "r":
                self.__undoRedoService.redo()
            elif optiune == "rnd":
                self.generator()
            elif optiune == "c":
                self.runStergereCascada()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati! ")

    def generator(self):
        try:
            n = int(input("Dati numarul de medicamente aleatorii: "))
            self.__medicamentService.generatorMedicamente(n)
        except Exception as e:
            print(e)

    def runCRUDMedicamenteMenu(self):
        while True:
            print("1. Adauga medicament.")
            print("2. Sterge medicament.")
            print("3. Modifica medicament.")
            print("a. Afiseaza toate medicamentele.")
            print("x. Iesire.")
            optiune = input("Dati optiunea: ")

            if optiune == "1":
                self.uiAdaugaMedicament()
            elif optiune == "2":
                self.uiStergeMedicament()
            elif optiune == "3":
                self.uiModificaMedicament()
            elif optiune == "a":
                self.showAllMedicamente()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati!")

    def runCRUDCardClientMenu(self):
        while True:
            print("1. Adauga card client.")
            print("2. Sterge card client.")
            print("3. Modifica card client.")
            print("a. Afiseaza toate cardurile.")
            print("x. Iesire.")
            optiune = input("Dati optiunea: ")

            if optiune == "1":
                self.uiAdaugaCardClient()
            elif optiune == "2":
                self.uiStergeCardClient()
            elif optiune == "3":
                self.uiModificaCardCLient()
            elif optiune == "a":
                self.showAllCarduriClienti(self.__cardClientService.getAll())
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati!")

    def runCRUDTranzactieMenu(self):
        while True:
            print("1. Adauga tranzactie.")
            print("2. Sterge tranzactie.")
            print("3. Modifica tranzactie.")
            print("a. Afiseaza toate tranzactiile.")
            print("x. Iesire.")
            optiune = input("Dati optiunea: ")

            if optiune == "1":
                self.uiAdaugaTranzactie()
            elif optiune == "2":
                self.uiStergeTranzactie()
            elif optiune == "3":
                self.uiModificaTranzactie()
            elif optiune == "a":
                self.showAllTranzactii()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati!")

    def runStergereCascada(self):
        while True:
            print("1. Sterge medicament.")
            print("2. Sterge card client.")
            print("x. Iesire.")
            optiune = input("Dati optiunea: ")

            if optiune == "1":
                self.uiStergeCascadaMed()
            elif optiune == "2":
                self.uiStergeCascadaCard()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati!")

    def uiAdaugaMedicament(self):
        try:
            idMedicament = input("Dati id-ul medicamentului: ")
            nume = input("Dati numele medicamentului: ")
            producator = input("Dati producatorul medicamentului: ")
            pret = float(input("Dati pretul medicamentului: "))
            necesitateReteta = input("Dati necesitatea "
                                     "retetei medicamentului(da/nu): ")

            self.__medicamentService.adauga(idMedicament,
                                            nume,
                                            producator,
                                            pret,
                                            necesitateReteta)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except MedicamentError as me:
            print(me)
        except Exception as e:
            print(e)

    def uiStergeMedicament(self):
        try:
            idMedicament = input("Dati id-ul medicamentului de sters: ")

            self.__medicamentService.sterge(idMedicament)
        except KeyError as ke:
            print(ke)
        except MedicamentError as me:
            print(me)
        except Exception as e:
            print(e)

    def uiModificaMedicament(self):
        try:
            idMedicament = input("Dati id-ul medicamentului de modificat: ")
            nume = input("Dati noul nume al medicamentului: ")
            producator = input("Dati moul producator al medicamentului: ")
            pret = float(input("Dati moul pret al medicamentului: "))
            necesitateReteta = input("Dati noua necesitate "
                                     "a retetei medicamentului: ")

            self.__medicamentService.modifica(idMedicament,
                                              nume,
                                              producator,
                                              pret,
                                              necesitateReteta)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except MedicamentError as me:
            print(me)
        except Exception as e:
            print(e)

    def showAllMedicamente(self):
        for medicament in self.__medicamentService.getAll():
            print(medicament)

    def uiAdaugaCardClient(self):
        try:
            idCard = input("Dati id-ul cardului: ")
            nume = input("Dati numele: ")
            prenume = input("Dati prenumele: ")
            dataNasterii = input("Dati data nasterii: ")
            dataInregistrarii = input("Dati data inregistrarii: ")
            CNP = int(input("Dati CNP-ul: "))

            self.__cardClientService.adauga(idCard,
                                            nume,
                                            prenume,
                                            dataNasterii,
                                            dataInregistrarii,
                                            CNP)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiStergeCardClient(self):
        try:
            idCard = input("Dati id-ul cardului de sters: ")

            self.__cardClientService.sterge(idCard)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiModificaCardCLient(self):
        try:
            idCard = input("Dati id-ul cardului de modificat: ")
            nume = input("Dati noul nume: ")
            prenume = input("Dati noul prenume: ")
            dataNasterii = datetime.strptime(input("Dati noua data "
                                                   "a nasterii:"),
                                             "%d.%m.%Y")
            dataInregistrarii = datetime.strptime(input("Dati noua data "
                                                        "a inregistrarii:"),
                                                  "%d.%m.%Y")
            CNP = int(input("Dati noul CNP: "))

            self.__cardClientService.modifica(idCard,
                                              nume,
                                              prenume,
                                              dataNasterii,
                                              dataInregistrarii,
                                              CNP)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def showAllCarduriClienti(self, carduri):
        if len(carduri) == 0:
            return
        print(carduri[0])
        return carduri[1:]

    def uiAdaugaTranzactie(self):
        try:
            idTranzactie = input("Dati id-ul tranzactiei: ")
            idMedicament = input("Dati id-ul medicamentului: ")
            idCard = input("Dati id-ul cardului(0 daca nu "
                           "exista card client): ")
            nrBucati = int(input("Dati numarul de bucati: "))
            dataOra = datetime.strptime(input("Dati data si ora: "),
                                        "%d.%m.%Y %H:%M")

            self.__tranzactieService.adauga(idTranzactie,
                                            idMedicament,
                                            idCard,
                                            nrBucati,
                                            dataOra)

            lista = self.__tranzactieService.calculReducere(idTranzactie)
            print("Total de plata: {}. "
                  "Reduceri: {}".format(lista[0], lista[1]))
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiStergeTranzactie(self):
        try:
            idTranzactie = input("Dati id-ul tranzactiei de sters: ")

            self.__tranzactieService.sterge(idTranzactie)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiModificaTranzactie(self):
        try:
            idTranzactie = input("Dati id-ul tranzactiei de modificat: ")
            idMedicament = input("Dati noul id al medicamentului: ")
            idCard = input("Dati noul id al cardului: ")
            nrBucati = int(input("Dati noul numar de bucati: "))
            dataOra = datetime.strptime(input("Dati noua data si ora: "),
                                        "%d.%m.%Y %H:%M")

            self.__tranzactieService.modifica(idTranzactie,
                                              idMedicament,
                                              idCard,
                                              nrBucati,
                                              dataOra)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def showAllTranzactii(self):
        for tranzactie in self.__tranzactieService.getAll():
            print(tranzactie)

    def uiOrdMedDupaNrVanzari(self):
        try:
            for med in self.__medicamentService.ordMedDupaNrVanzari():
                print(med)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiCautare(self):
        try:
            text = input("Dati textul de cautat: ")
            cautareMed = self.__medicamentService.cautareMed(text)
            cautareClienti = self.__cardClientService.cautareClineti(text)
            if len(cautareMed) > 0:
                for med in cautareMed:
                    print(med)
            else:
                print("Nu s-a gasit niciun medicament cu textul dat!")

            if len(cautareClienti) > 0:
                for client in cautareClienti:
                    print(client)
            else:
                print("Nu s-a gasit niciun client cu textul dat!")
        except Exception as e:
            print(e)

    def uiAfisTranzIntervalDat(self):
        try:
            data1 = datetime.strptime(input("Dati prima data: "), '%d.%m.%Y')
            data2 = datetime.strptime(input("Dati a doua data: "), '%d.%m.%Y')
            if data2 < data1:
                data1, data2 = data2, data1

            rezultat = self.__tranzactieService.tranzDinInterval(data1, data2)

            if len(rezultat) > 0:
                for tranz in rezultat:
                    print(tranz)
            else:
                print("Nu exista nicio tranzactie in intervalul dat!")
        except Exception as e:
            print(e)

    def uiOrdCCDupaValReduceri(self):
        try:
            for card in self.__cardClientService.ordDupaValReducerilor():
                print(card)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiStergeTranzDinInterval(self):
        try:
            data1 = datetime.strptime(input("Dati prima data: "), '%d.%m.%Y')
            data2 = datetime.strptime(input("Dati a doua data: "), '%d.%m.%Y')
            if data2 < data1:
                data1, data2 = data2, data1
            self.__tranzactieService.stergeTranzDinInterval(data1, data2)
        except Exception as e:
            print(e)

    def uiScumpesteMed(self):
        try:
            procent = float(input("Dati procentul: "))
            valoare = float(input("Dati valoare: "))
            self.__medicamentService.scumpire(procent, valoare)
        except Exception as e:
            print(e)

    def uiStergeCascadaMed(self):
        try:
            idMed = input("Dati id-ul medicamentului de sters: ")
            self.__medicamentService.stergeCascada(idMed)
        except Exception as e:
            print(e)

    def uiStergeCascadaCard(self):
        try:
            idCard = input("Dati id-ul cardului de sters: ")
            self.__cardClientService.stergeCascada(idCard)
        except Exception as e:
            print(e)
