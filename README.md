# Obsługa zleceń DTP – system ekspertowy (Z2)

Dawid Seipold, gr. 3

System na podstawie zlecenia mówi, jaką paletkę wziąć do naświetlania płyty Flexcel i jaki tag jej dać, albo że zlecenie idzie do grafików. Reguły są przepisane z drzewa z Z1 do `wiedza/moja_dziedzina.json`.

## Uruchomienie

```
python se/sprawdz_format.py wiedza/moja_dziedzina.json
python se/test_silnik.py
python se/test_moja_dziedzina.py
python se/silnik.py
```

`kawa.json` zostaje w repo tylko dlatego, że korzysta z niego `test_silnik.py`.

## Baza

- P1–P4 – ustalają `tag` z grubości i rodzaju płyty (wniosek pośredni)
- R1 – proof idzie do grafików
- R2–R25 – liniatura + podłoże + tag dają paletkę
- R26 – reguła zapasowa: flexcel z liniaturą 100–200, dla której nie ma paletki, też idzie do grafików

## Konsultacja wstecz

```
Jaki jest rodzaj zlecenia? (proof/flexcel) flexcel
Podaj liniaturę (133, 150 lub 175): 150
Jakie jest podłoże? (papier/folia) folia
Podaj grubość płyty (1.14 lub 1.7): 1.7
Jaki jest rodzaj płyty? (awers/rewers) rewers
Polecam: PALETKA 150 FOLIA [TAG 1_7_REWERS]
Reguły: P4 -> R17
```

Pytania idą w tej samej kolejności co w drzewie: najpierw rodzaj zlecenia, potem liniatura i podłoże, a na końcu płyta, bo jest potrzebna dopiero do tagu. Przy proof pada tylko jedno pytanie, a przy liniaturze spoza listy (np. 160) dwa. Reszta nie ma wtedy znaczenia.

## Konflikty

Wygrywa pierwsza pasująca reguła. R26 stoi na końcu, bo jest najogólniejsza. Np. dla 150/folia/1.7/rewers pasuje i R17, i R26, ale R17 jest wyżej, więc dostajemy paletkę. Gdyby R26 była na początku, każde zlecenie flexcel szłoby do grafików.
