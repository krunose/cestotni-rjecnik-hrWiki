import re
from collections import Counter

# Nazivi vaših datoteka
SIROVI_IZVOR = "čisti-izlaz"           # Vaš sirovi vezani tekst nakon sed-a
STARI_RJECNIK = "../../no-true-casing-čestotni-rječnik-hrWiki" # Vaš trenutni rječnik s GitHuba
NOVI_RJECNIK = "čestotni-rječnik-hrWiki"

# Skupovi za praćenje pozicija velikih slova
velika_slova_na_pocetku = set()
velika_slova_u_sredini = set()

# ISPRAVLJEN REGEX: Dodana je kosa crta \[ ispred prve zagrade da se izbjegne FutureWarning
regex_pocetak = re.compile(r'(?:^|[.!?]\s+)[\\["\'(„\s-]*([A-ZČĆŽŠĐ][a-zčćžšđ]+)')
regex_sve_velike = re.compile(r'\b[A-ZČĆŽŠĐ][a-zčćžšđ]+\b')

print("1. Korak: Mapiram pozicije velikih slova na Wikipediji...")
try:
    with open(SIROVI_IZVOR, "r", encoding="utf-8") as f:
        for linija in f:
            # A) Nađi riječi koje su na početku rečenice
            pocetni_oblici = regex_pocetak.findall(linija)
            for rijec in pocetni_oblici:
                velika_slova_na_pocetku.add(rijec)
            
            # B) Nađi sve riječi s velikim slovom u toj liniji
            sve_velike = regex_sve_velike.findall(linija)
            for rijec in sve_velike:
                # Ako je riječ nađena u liniji, a NIJE bila na početku rečenice,
                # to znači da se pojavila u sredini rečenice s velikim slovom!
                if rijec not in pocetni_oblici:
                    velika_slova_u_sredini.add(rijec)
except FileNotFoundError:
    print(f"Pogreška: Datoteka '{SIROVI_IZVOR}' nije pronađena!")
    exit()

# STROGI UVJET: Riječ se smije smanjiti SAMO ako je bila na početku rečenice,
# a NIJEDNOM se u cijelom dumpu nije pojavila s velikim slovom u sredini rečenice.
rijeci_za_smanjivanje = velika_slova_na_pocetku - velika_slova_u_sredini

print(f"Analiza gotova. Od svih riječi, njih {len(rijeci_za_smanjivanje)} su ISKLJUČIVO na početku rečenice.")

print("2. Korak: Učitavam stari rječnik i primjenjujem strogi ispravak...")
konacni_rjecnik = {}

try:
    with open(STARI_RJECNIK, "r", encoding="utf-8") as f:
        for linija in f:
            linija = linija.strip()
            if not linija:
                continue
            
            dijelovi = linija.split(maxsplit=1)
            if len(dijelovi) < 2:
                continue
                
            freq_str = dijelovi[0]
            rijec = dijelovi[1]
            
            try:
                freq = int(freq_str)
            except ValueError:
                continue
            
            # Ako riječ zadovoljava naš strogi uvjet, prebaci je u malo slovo i zbroji frekvenciju
            if rijec in rijeci_za_smanjivanje:
                verzija_s_malim = rijec.lower()
                konacni_rjecnik[verzija_s_malim] = konacni_rjecnik.get(verzija_s_malim, 0) + freq
            else:
                # Vlastita imena (Hrvatska, Zagreb) koja se pojavljuju u sredini rečenica ostaju velika!
                konacni_rjecnik[rijec] = konacni_rjecnik.get(rijec, 0) + freq
except FileNotFoundError:
    print(f"Pogreška: Datoteka '{STARI_RJECNIK}' nije pronađena!")
    exit()

print("3. Korak: Sortiram i spremam novi strogi čestotnik...")
sortirani_rjecnik = sorted(konacni_rjecnik.items(), key=lambda x: x[1], reverse=True)

with open(NOVI_RJECNIK, "w", encoding="utf-8") as f:
    for rijec, freq in sortirani_rjecnik:
        f.write(f"{freq}\t{rijec}\n")

print(f"Uspjeh! Savršeno očišćeni rječnik je spremljen u '{NOVI_RJECNIK}'.")
