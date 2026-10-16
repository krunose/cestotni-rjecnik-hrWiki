# Nazivi datoteka
ULAZNI_RJECNIK = "statistical-true-cased-hrWiki"
IZLAZNA_ANALIZA = "čestotni-rječnik-hrWiki"

# Točan broj tokena iz vaše statistike korpusa
UKUPNO_TOKENA = 53106215

print("Učitavam rječnik i pokrećem statističku analizu...")
stavke = []

with open(ULAZNI_RJECNIK, "r", encoding="utf-8") as f:
    for linija in f:
        linija = linija.strip()
        if not linija:
            continue
        dijelovi = linija.split(maxsplit=1)
        if len(dijelovi) < 2:
            continue
            
        freq = int(dijelovi[0])
        rijec = dijelovi[1]
        stavke.append((freq, rijec))

print("Računam relativne i kumulativne vrijednosti...")
kumulativni_zbroj = 0

with open(IZLAZNA_ANALIZA, "w", encoding="utf-8") as f:
    # Zapisujemo zaglavlje tablice radi preglednosti
    f.write("Rang\tAps_Freq\tRel_Freq_%\tIPM\tKumulativno_%\tRiječ\n")
    
    for rang, (freq, rijec) in enumerate(stavke, start=1):
        # 1. Izračun relativne frekvencije u postocima
        rel_freq = (freq / UKUPNO_TOKENA) * 100
        
        # 2. Izračun pojavljivanja na milijun riječi (IPM)
        ipm = (freq / UKUPNO_TOKENA) * 1000000
        
        # 3. Izračun kumulativnog postotka pokrivenosti korpusa
        kumulativni_zbroj += freq
        kumulativni_postotak = (kumulativni_zbroj / UKUPNO_TOKENA) * 100
        
        # Zapisivanje u datoteku odvojeno tabulatorima
        f.write(f"{rang}\t{freq}\t{rel_freq:.4f}%\t{ipm:.2f}\t{kumulativni_postotak:.2f}%\t{rijec}\n")

print(f"Uspjeh! Detaljna frekvencijska analiza spremljena je u '{IZLAZNA_ANALIZA}'.")
