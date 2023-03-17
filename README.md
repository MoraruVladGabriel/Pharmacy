# Pharmacy

Farmacie Online
1.1. CRUD medicament: id, nume, producător, preț, necesită rețetă. Prețul să fie strict pozitiv.
1.2. CRUD card client: id, nume, prenume, CNP, data nașterii (dd.mm.yyyy), data înregistrării (dd.mm.yyyy). CNP-ul trebuie să fie unic.
1.3. CRUD tranzacție: id, id_medicament, id_card_client (poate fi nul), nr_bucăți, data și ora. Dacă există un card client, atunci aplicați o reducere de 10% dacă medicamentul nu necesită rețetă și de 15% dacă necesită. Se tipărește prețul plătit și reducerile acordate.
1.4. Căutare medicamente și clienți. Căutare full text.
1.5. Afișarea tuturor tranzacțiilor dintr-un interval de zile dat.
1.6. Afișarea medicamentelor ordonate descrescător după numărul de vânzări.
1.7. Afișarea cardurilor client ordonate descrescător după valoarea reducerilor obținute.
1.8. Ștergerea tuturor tranzacțiilor dintr-un anumit interval de zile.
1.9. Scumpirea cu un procentaj dat a tuturor medicamentelor cu prețul mai mic decât o valoare dată.
