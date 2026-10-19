import os
import re
import gc
import sys
import classla

# =====================================================================
# KONFIGURACIJA I POSTAVKE
# =====================================================================
rjecnik_putanja = "lematizirani-čestotni-rječnik-hrWiki"
cisti_izlaz_putanja = "wiki_privremeno/AA/čisti-izlaz"

VELICINA_PAKETA = 100       # Koliko rečenica šaljemo odjednom u Classlu
PRAG_ZA_SPREMANJE = 1000    # Nakon koliko novih lema prepisujemo datoteku na disk

# KLJUČNA OPTIMIZACIJA: Riječ ide na lematizaciju samo ako se u Wiki pojavljuje ovoliko ili više puta
# (Slobodno promijeni na 10 ili 20 ako želiš još bržu obradu)
PRAG_FREKVENCIJE = 5        

# Inicijalizacija CLASSLA pipelinea s nužnim POS procesorom
print("[INFO] Pokrećem CLASSLA pipeline za hrvatski jezik (tokenize, pos, lemma)...")
nlp = classla.Pipeline('hr', processors='tokenize,pos,lemma')

# Funkcija za kontrolirano streaming zapisivanje novih lema na disk (RAM ostaje prazan)
def zapisi_leme_na_disk(putanja_rjecnika, mapa_novih_lema):
    if not mapa_novih_lema:
        return
    print(f"\n[SVEUČILIŠTE/DISK] Pokrećem kontrolirano zapisivanje {len(mapa_novih_lema)} lema na disk...")
    
    privremena_putanja = putanja_rjecnika + ".tmp"
    
    with open(putanja_rjecnika, "r", encoding="utf-8") as f_in, \
         open(privremena_putanja, "w", encoding="utf-8") as f_out:
         
        # Prepiši zaglavlje
        f_out.write(next(f_in))
        
        for line in f_in:
            line_clean = line.replace("\n", "").replace("\r", "")
            dijelovi = line_clean.split("\t")
            
            if len(dijelovi) < 6:
                f_out.write(line)
                continue
                
            pojavnica = dijelovi[5]
            pojavnica_lower = pojavnica.lower().strip()
            
            # Ako redak već ima lemu od prije, samo ga prepiši
            if len(dijelovi) == 7 and dijelovi[6].strip():
                f_out.write(line)
            else:
                # Provjeri imamo li spremnu lemu u našem privremenom rječniku
                nova_lema = mapa_novih_lema.get(pojavnica_lower, "")
                
                if pojavnica.isupper() and nova_lema:
                    nova_lema = nova_lema.capitalize()
                    
                if len(dijelovi) == 7:
                    dijelovi[6] = nova_lema
                    f_out.write("\t".join(dijelovi) + "\n")
                else:
                    f_out.write(f"{line_clean}\t{nova_lema}\n")
                    
    # Zamijeni staru datoteku novom (atomarna operacija na razini OS-a)
    os.replace(privremena_putanja, putanja_rjecnika)
    print("[DISK] Zapisivanje uspješno završeno. Datoteka je ažurirana.")

# =====================================================================
# 1. KORAK: Pronalaženje riječi koje nemaju lemu (Uz primjenu PRAGA FREKVENCIJE)
# =====================================================================
print(f"[INFO] Tražim riječi koje su ostale bez leme, a imaju frekvenciju >= {PRAG_FREKVENCIJE}...")
prazne_rijeci = set()

with open(rjecnik_putanja, "r", encoding="utf-8") as f:
    next(f) # Preskoči zaglavlje
    for line in f:
        dijelovi = line.replace("\n", "").split("\t")
        if len(dijelovi) >= 6:
            pojavnica = dijelovi[5]
            
            # Sigurno izvlačenje apsolutne frekvencije iz drugog stupca (indeks 1)
            try:
                frekvencija_rijeci = int(dijelovi[1].strip())
            except (ValueError, IndexError):
                frekvencija_rijeci = 1
            
            # Uvjet: riječ ide na obradu samo ako nema lemu I ako prelazi prag frekvencije
            if len(dijelovi) < 7 or not dijelovi[6].strip():
                if pojavnica.strip() and frekvencija_rijeci >= PRAG_FREKVENCIJE:
                    prazne_rijeci.add(pojavnica.strip().lower())

print(f"[USPJEH] Pronađeno je {len(prazne_rijeci)} jedinstvenih čestih riječi bez leme.")

if not prazne_rijeci:
    print("[KRAJ] Sve česte riječi već imaju lemu! Skripta se gasi.")
    exit()

# =====================================================================
# 2. KORAK: Traženje kontekstnih rečenica u datoteci 'čisti-izlaz'
# =====================================================================
print("[INFO] Prolazim kroz 'čisti-izlaz' i tražim rečenice za nepoznate riječi...")
kontekst_recenice = {}
recenica_regex = re.compile(r'[^.!?\n]+[.!?]?')

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
                    
            # Čim skupimo rečenice za sve tražene riječi, prekidamo i drastično štedimo RAM i vrijeme
            if len(kontekst_recenice) == len(prazne_rijeci):
                break
        if len(kontekst_recenice) == len(prazne_rijeci):
            break

sve_recenice = list(kontekst_recenice.values())
print(f"[INFO] Pronađeno je {len(sve_recenice)} rečenica za obradu.")

# Oslobađamo privremene strukture iz memorije prije ulaska u tešku CLASSLA petlju
del kontekst_recenice
gc.collect()

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
                        izracunata_lema = word_obj.lemma
                        if izracunata_lema:
                            izracunata_lema = izracunata_lema.lower()
                        
                        if izvorna_riza in prazne_rijeci:
                            pronadjene_leme[izvorna_riza] = izracunata_lema
        except Exception as e:
            print(f"\n[UPOZORENJE] Greška prilikom obrade paketa: {e}")
        
        # AUTOSAVE MEHANIZAM
        if len(pronadjene_leme) >= PRAG_ZA_SPREMANJE:
            zapisi_leme_na_disk(rjecnik_putanja, pronadjene_leme)
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

