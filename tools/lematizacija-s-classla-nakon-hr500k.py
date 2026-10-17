import os
import re
import gc
import sys
import classla

# Inicijalizacija CLASSLA pipelinea s nužnim POS procesorom (jer lematizator ovisi o njemu)
print("[INFO] Pokrećem CLASSLA pipeline za hrvatski jezik (tokenize, pos, lemma)...")
nlp = classla.Pipeline('hr', processors='tokenize,pos,lemma')

rjecnik_putanja = "lematizirani-čestotni-rječnik-hrWiki.txt"
cisti_izlaz_putanja = "wiki_privremeno/AA/čisti-izlaz"

VELICINA_PAKETA = 100       # Koliko rečenica šaljemo odjednom u Classlu
PRAG_ZA_SPREMANJE = 1000    # Nakon koliko novih lema prepisujemo datoteku na disk

# Pomoćna funkcija za fizičko upisivanje skupljenih lema na disk
def zapisi_leme_na_disk(putanja_rjecnika, mapa_novih_lema):
    if not mapa_novih_lema:
        return
    print(f"\n[SVEUČILIŠTE/DISK] Pokrećem kontrolirano zapisivanje {len(mapa_novih_lema)} lema na disk...")
    privremeni_redci = []
    
    with open(putanja_rjecnika, "r", encoding="utf-8") as f_in:
        privremeni_redci.append(next(f_in)) # Prepiši zaglavlje
        for line in f_in:
            line_clean = line.replace("\n", "").replace("\r", "")
            dijelovi = line_clean.split("\t")
            
            if len(dijelovi) < 6:
                privremeni_redci.append(line)
                continue
                
            pojavnica = dijelovi[5]
            pojavnica_lower = pojavnica.lower().strip()
            
            # Ako redak već ima lemu od prije, samo ga prepiši
            if len(dijelovi) == 7 and dijelovi[6].strip():
                privremeni_redci.append(line)
            else:
                # Provjeri imamo li spremnu lemu u našem privremenom rječniku
                nova_lema = mapa_novih_lema.get(pojavnica_lower, "")
                
                if pojavnica.isupper() and nova_lema:
                    nova_lema = nova_lema.capitalize()
                    
                if len(dijelovi) == 7:
                    dijelovi[6] = nova_lema
                    privremeni_redci.append("\t".join(dijelovi) + "\n")
                else:
                    privremeni_redci.append(f"{line_clean}\t{nova_lema}\n")
                    
    # Prepiši datoteku na disku
    with open(putanja_rjecnika, "w", encoding="utf-8") as f_out:
        f_out.writelines(privremeni_redci)
    print("[DISK] Zapisivanje uspješno završeno. Datoteka je ažurirana.")

# =====================================================================
# 1. KORAK: Pronalaženje riječi koje nemaju lemu
# =====================================================================
print("[INFO] Tražim riječi koje su ostale bez leme u rječniku...")
prazne_rijeci = set()

with open(rjecnik_putanja, "r", encoding="utf-8") as f:
    next(f) # Preskoči zaglavlje
    for line in f:
        dijelovi = line.replace("\n", "").split("\t")
        if len(dijelovi) >= 6:
            pojavnica = dijelovi[5]
            if len(dijelovi) < 7 or not dijelovi[6].strip():
                if pojavnica.strip():
                    prazne_rijeci.add(pojavnica.strip().lower())

print(f"[USPJEH] Pronađeno je {len(prazne_rijeci)} jedinstvenih riječi bez leme.")

if not prazne_rijeci:
    print("[KRAJ] Sve riječi već imaju lemu! Skripta se gasi.")
    exit()

# =====================================================================
# 2. KORAK: Traženje kontekstnih rečenica u datoteci 'čisti-izlaz'
# =====================================================================
print("[INFO] Prolazim kroz 'čisti-izlaz' i tražim rečenice za nepoznate riječi...")
kontekst_recenice = {}
recenica_regex = re.compile(r'[^.!?]+[.!?]?')

with open(cisti_izlaz_putanja, "r", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue
        
        recenice = recenica_regex.findall(line)
        for rec in recenice:
            rec_clean = rec.strip()
            rijeci_u_rec = [w.lower().strip(",.!?\"()'-") for w in rec_clean.split()]
            
            for rijec in rijeci_u_rec:
                if rijec in prazne_rijeci and rijec not in kontekst_recenice:
                    kontekst_recenice[rijec] = rec_clean
                    
        if len(kontekst_recenice) == len(prazne_rijeci):
            break

sve_recenice = list(kontekst_recenice.values())
print(f"[INFO] Pronađeno je {len(sve_recenice)} rečenica za obradu.")

# =====================================================================
# 3. KORAK: Procesiranje s CLASSLA-om u paketima (s autosave funkcijom)
# =====================================================================
print("[INFO] Pokrećem CLASSLA obradu... Za prekid pritisni CTRL + C (trenutni napredak će se spremiti).")
pronadjene_leme = {}

try:
    for i in range(0, len(sve_recenice), VELICINA_PAKETA):
        paket = sve_recenice[i:i + VELICINA_PAKETA]
        sys.stdout.write(f"\rProcesiram paket rečenica: {i} do {i + len(paket)}... Skupio novih lema: {len(pronadjene_leme)}")
        sys.stdout.flush()
        
        blok_teksta = "\n".join(paket)
        try:
            doc = nlp(blok_teksta)
            for sentence in doc.sentences:
                for token in sentence.tokens:
                    for word_obj in token.words:
                        izvorna_riza = word_obj.text.lower()
                        izracunata_lema = word_obj.lemma.lower()
                        if izvorna_riza in prazne_rijeci:
                            pronadjene_leme[izvorna_riza] = izracunata_lema
        except Exception as e:
            print(f"\n[UPOZORENJE] Greška prilikom obrade paketa: {e}")
        
        # AUTOSAVE MEHANIZAM: Ako smo prebacili prag od 1000 riječi, spremaj na disk i čisti RAM
        if len(pronadjene_leme) >= PRAG_ZA_SPREMANJE:
            zapisi_leme_na_disk(rjecnik_putanja, pronadjene_leme)
            
            # Čišćenje rječnika i prisilno pražnjenje memorije
            pronadjene_leme.clear()
            gc.collect()
            print("[RAM] Memorija očišćena. Nastavljam s obradom idućeg paketa...\n")
            
    # Konačno zapisivanje preostalih riječi nakon završetka petlje
    if pronadjene_leme:
        zapisi_leme_na_disk(rjecnik_putanja, pronadjene_leme)

except KeyboardInterrupt:
    print("\n\n[PREKID] Detektiran pritisak CTRL + C! Spašavam trenutno obrađene podatke prije izlaza...")
    if pronadjene_leme:
        zapisi_leme_na_disk(rjecnik_putanja, pronadjene_leme)
    print("[KRAJ] Podaci su sigurno pohranjeni. Skripta je uspješno zaustavljena.")
    exit()

print("\n[ZAVRŠENO] Cijeli proces lematizacije je uspješno dovršen bez gubitka podataka!")

