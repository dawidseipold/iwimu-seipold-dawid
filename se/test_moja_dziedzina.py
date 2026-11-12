"""Testy własnej bazy wiedzy (Z2). Uruchom: python se/test_moja_dziedzina.py

Każdy przypadek sprawdza oba tryby: w przód (wszystkie dane od razu) i wstecz (dialog),
oraz to, że w trybie wstecz system nie pyta dwa razy o to samo.
"""
from pathlib import Path

from silnik import wczytaj_baze, regula_spelniona, wnioskuj_w_przod, wnioskuj_wstecz

baza = wczytaj_baze(Path(__file__).parent.parent / "wiedza" / "moja_dziedzina.json")
CEL = baza["cel"]
REGULY = {r["id"]: r for r in baza["reguly"]}


def flexcel(liniatura, podloze, grubosc, rodzaj):
    return {"rodzaj_zlecenia": "flexcel", "liniatura": liniatura, "podloze": podloze,
            "grubosc_plyty": grubosc, "rodzaj_plyty": rodzaj}


# (nr, rodzaj, dane wejściowe, oczekiwana decyzja, oczekiwany ślad w przód lub None)
PRZYPADKI = [
    ("T1", "typowy", flexcel(133, "papier", 1.14, "awers"),
     "PALETKA 133 PAPIER [BEZ TAGU]", ["P1", "R2"]),
    ("T2", "typowy", {"rodzaj_zlecenia": "proof"},
     "PRZEKAZUJĘ GRAFIKOM", ["R1"]),
    ("T3", "granica", flexcel(200, "folia", 1.7, "awers"),       # górna granica R26: liniatura <= 200
     "PRZEKAZUJĘ GRAFIKOM", ["P3", "R26"]),
    ("T4", "granica", flexcel(100, "papier", 1.14, "rewers"),    # dolna granica R26: liniatura >= 100
     "PRZEKAZUJĘ GRAFIKOM", ["P2", "R26"]),
    ("T5", "brak wyniku", flexcel(201, "papier", 1.14, "awers"), # tuż za granicą: żadna reguła nie pasuje
     None, ["P1"]),
    ("T6", "brak wyniku", flexcel(90, "folia", 1.7, "rewers"),   # liniatura poniżej przedziału R26
     None, ["P4"]),
    ("T7", "konflikt", flexcel(150, "folia", 1.7, "rewers"),     # pasują R17 i R26, wygrywa R17 (stoi wyżej)
     "PALETKA 150 FOLIA [TAG 1_7_REWERS]", ["P4", "R17"]),
    ("T8", "luka w tagu", flexcel(175, "papier", 1.5, "awers"),  # niestandardowa grubość: brak tagu, ratuje R26
     "PRZEKAZUJĘ GRAFIKOM", ["R26"]),
]

ok = 0
for nr, rodzaj, wejscie, oczekiwane, oczekiwany_slad in PRZYPADKI:
    fakty, slad = wnioskuj_w_przod(baza, wejscie)
    w_przod_ok = fakty.get(CEL) == oczekiwane and (oczekiwany_slad is None or slad == oczekiwany_slad)

    zadane = []
    def zapytaj(atrybut, powod):
        zadane.append(atrybut)
        return wejscie.get(atrybut)
    wstecz = wnioskuj_wstecz(baza, CEL, {}, zapytaj, [])
    wstecz_ok = wstecz == oczekiwane and len(zadane) == len(set(zadane))

    dodatkowe_ok = True
    if rodzaj == "konflikt":
        # Konflikt naprawdę zachodzi: obie reguły są spełnione dla tych samych faktów.
        dodatkowe_ok = regula_spelniona(REGULY["R17"], fakty) and regula_spelniona(REGULY["R26"], fakty)
        # Strategia = kolejność: po przeniesieniu R26 na początek wynik się zmienia.
        odwrocona = dict(baza, reguly=[REGULY["R26"]] + [r for r in baza["reguly"] if r["id"] != "R26"])
        fakty_odwr, _ = wnioskuj_w_przod(odwrocona, wejscie)
        dodatkowe_ok = dodatkowe_ok and fakty_odwr.get(CEL) == "PRZEKAZUJĘ GRAFIKOM"

    zaliczony = w_przod_ok and wstecz_ok and dodatkowe_ok
    ok += zaliczony
    print(f"[{'OK ' if zaliczony else 'BŁĄD'}] {nr} {rodzaj:<12} -> w przód: {fakty.get(CEL)} "
          f"({' -> '.join(slad)}), wstecz: {wstecz}, pytań: {len(zadane)}")

print(f"\nZaliczone przypadki: {ok}/{len(PRZYPADKI)}")
