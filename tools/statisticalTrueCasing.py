import re
from collections import Counter

# Nazivi vaših datoteka
SIROVI_IZVOR = "čisti-izlaz"           # Vaš sirovi vezani tekst nakon sed-a
STARI_RJECNIK = "../../no-true-casing-čestotni-rječnik-hrWiki" # Vaš trenutni rječnik s GitHuba
NOVI_RJECNIK = "čestotni-rječnik-hrWiki"

# Brojači za praćenje svih pojavljivanja riječi na Wikipediji
brojac_velikih_u_sredini = Counter()
brojac_malih_u_sredini = Counter()
velika_slova_na_pocetku = set()

# Regexi za precizno hvatanje pozicija u tekstu
regex_pocetak = re.compile(r'(?:^|[.!?]\s+)[\\["\'(„\s-]*([A-ZČĆŽŠĐ][a-zčćžšđ]*)')
regex_sve_velike = re.compile(r'\b[A-ZČĆŽŠĐ][a-zčćžšđ]*\b')
regex_sve_male = re.compile(r'\b[a-zčćžšđ]+\b')

print("1. Korak: Prolazim kroz sirovi tekst Wikipedije i analiziram statistiku...")
try:
    with open(SIROVI_IZVOR, "r", encoding="utf-8") as f:
        for linija in f:
            # A) Nađi riječi koje su na početku rečenice
            pocetni_oblici = regex_pocetak.findall(linija)
            for rijec in pocetni_oblici:
                velika_slova_na_pocetku.add(rijec)
            
            # B) Broji sve riječi s velikim slovom koje NISU na početku rečenice
            sve_velike = regex_sve_velike.findall(linija)
            for rijec in sve_velike:
                if rijec not in pocetni_oblici:
                    brojac_velikih_u_sredini[rijec] += 1
            
            # C) Broji sva pojavljivanja riječi u malom slovu
            sve_male = regex_sve_male.findall(linija)
            for rijec in sve_male:
                brojac_malih_u_sredini[rijec] += 1
except FileNotFoundError:
    print(f"Pogreška: Datoteka '{SIROVI_IZVOR}' (" + SIROVI_IZVOR + ") nije pronađena!")
    exit()

print("2. Korak: Određujem koje riječi idu u malo slovo na temelju statističkog praga...")
rijeci_za_smanjivanje = set()

for rijec in velika_slova_na_pocetku:
    malo_oblik = rijec.lower()
    
    # Prisilno smanji sve jednoslovne riječi (U, I, O, A)
    if len(rijec) == 1:
        rijeci_za_smanjivanje.add(rijec)
        continue
        
    pojavljivanja_veliko_sredina = brojac_velikih_u_sredini[rijec]
    pojavljivanja_malo_sredina = brojac_malih_u_sredini[malo_oblik]
    
    ukupno_u_sredini = pojavljivanja_veliko_sredina + pojavljivanja_malo_sredina
    
    if ukupno_u_sredini > 0:
        # Računamo udio malog slova u sredini rečenice
        udio_malog_slova = pojavljivanja_malo_sredina / ukupno_u_sredini
        
        # Ako se riječ u sredini rečenice piše malim slovom u više od 95% slučajeva,
        # onda su ona velika slova u sredini bila samo naslovi ili stilske iznimke!
        if udio_malog_slova > 0.95:
            rijeci_za_smanjivanje.add(rijec)
    else:
        # Ako se riječ UOPĆE ne pojavljuje u sredini rečenice malim slovom (udio je 0),
        # ali se pojavljuje s velikim, to je sigurno vlastito ime (npr. Chalamet, Zagreb) i NE smanjujemo ga.
        continue

print(f"Analiza gotova. U malo slovo prebacujem {len(rijeci_za_smanjivanje)} jedinstvenih riječi.")

print("3. Korak: Učitavam stari rječnik i primjenjujem ispravak...")
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
            
            if rijec in rijeci_za_smanjivanje:
                verzija_s_malim = rijec.lower()
                konacni_rjecnik[verzija_s_malim] = konacni_rjecnik.get(verzija_s_malim, 0) + freq
            else:
                konacni_rjecnik[rijec] = konacni_rjecnik.get(rijec, 0) + freq
except FileNotFoundError:
    print(f"Pogreška: Datoteka '{STARI_RJECNIK}' (" + STARI_RJECNIK + ") nije pronađena!")
    exit()

print("4. Korak: Sortiram i spremam novi čestotnik...")
sortirani_rjecnik = sorted(konacni_rjecnik.items(), key=lambda x: x[1], reverse=True)

with open(NOVI_RJECNIK, "w", encoding="utf-8") as f:
    for rijec, freq in sortirani_rjecnik:
        f.write(f"{freq}\t{rijec}\n")

print(f"Uspjeh! Savršeno očišćeni rječnik je spremljen u '{NOVI_RJECNIK}'.")
