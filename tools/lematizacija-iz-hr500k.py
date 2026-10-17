import os
import zipfile

# =====================================================================
# 1. KORAK: Izvlačenje pojavnice i leme iz hr500k (2. i 3. stupac)
# =====================================================================
print("Faza 1: Čitam hr500k kao običan tekst...")
lema_dict = {}

with open("hr500k.conllu", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
            
        dijelovi = line.split("\t")
        if len(dijelovi) >= 3:
            pojavnica = dijelovi[1].lower().strip()  # 2. stupac (indeks 1)
            lema = dijelovi[2].lower().strip()       # 3. stupac (indeks 2)
            
            if pojavnica and lema and pojavnica not in lema_dict:
                lema_dict[pojavnica] = lema

print(f"[USPJEH] Izvučeno {len(lema_dict)} parova iz hr500k.\n")

# =====================================================================
# 2. KORAK: Čitanje wikirječnika i dodavanje leme (prazno ako ne postoji)
# =====================================================================
rjecnik_datoteka = "čestotni-rječnik-hrWiki"
arhiva_datoteka = "statistički-procesuiran-čestotni-rječnik-hrWiki.zip"

if not os.path.exists(rjecnik_datoteka) and os.path.exists(arhiva_datoteka):
    print(f"[INFO] Raspakiravam {rjecnik_datoteka}...")
    with zipfile.ZipFile(arhiva_datoteka, 'r') as zip_ref:
        zip_ref.extract(rjecnik_datoteka)

if not os.path.exists(rjecnik_datoteka):
    raise FileNotFoundError(f"Nije pronađena datoteka rječnika '{rjecnik_datoteka}'!")

print("Faza 2: Dodavanje leme u čestotni rječnik...")
izlazni_redci = []

with open(rjecnik_datoteka, "r", encoding="utf-8") as f:
    for line in f:
        line_clean = line.replace("\n", "").replace("\r", "")
        
        # Obrada zaglavlja tablice
        if line_clean.startswith("Rang"):
            izlazni_redci.append(f"{line_clean}\tLema\n")
            continue
            
        if not line_clean:
            continue
            
        dijelovi = line_clean.split("\t")
        if len(dijelovi) < 6:
            izlazni_redci.append(f"{line_clean}\t\n")
            continue
            
        pojavnica_wiki = dijelovi[5].strip()  # 6. stupac (indeks 5) je tvoja riječ
        pojavnica_lower = pojavnica_wiki.lower()
        
        # Provjera: ako je riječ u hr500k, uzmi lemu i uredi velika slova. Ako nije, ostaje prazno.
        if pojavnica_lower in lema_dict:
            lema = lema_dict[pojavnica_lower]
            if pojavnica_wiki[0].isupper() if pojavnica_wiki else False:
                lema = lema.capitalize()
        else:
            lema = ""  # Ovdje se ne ispisuje ništa ako riječi nema u hr500k
            
        # Spajanje tvog originalnog retka i leme (ili praznine) u sedmi stupac
        izlazni_redci.append(f"{line_clean}\t{lema}\n")

# =====================================================================
# 3. KORAK: Zapisivanje u novu datoteku
# =====================================================================
izlazna_datoteka = "lematizirani-čestotni-rječnik-hrWiki.txt"
print(f"Faza 3: Zapisujem podatke u {izlazna_datoteka}...")

with open(izlazna_datoteka, "w", encoding="utf-8") as f:
    f.writelines(izlazni_redci)

print(f"[ZAVRŠENO] Nova datoteka je uspješno generirana na lokaciji: {izlazna_datoteka}")

