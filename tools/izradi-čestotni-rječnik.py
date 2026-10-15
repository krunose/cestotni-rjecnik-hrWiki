from collections import Counter
import re

ULAZNA = "čisti-izlaz"
IZLAZNA = "četotni-rječnik-hrWiki"

# Ovaj regex automatski prepoznaje sva Unicode slova na svijetu (uključujući č,ć,ž,š,đ)
# i potpuno ignorira interpunkciju i brojeve, bez obzira na sistemske greške
pattern = re.compile(r"[\w]+", re.UNICODE) 

brojac = Counter()

# OBAVEZNO eksplicitno navesti encoding="utf-8"
with open(ULAZNA, "r", encoding="utf-8") as f:
    for linija in f:
        # Filtriramo samo riječi i izbacujemo čiste brojeve iz pretrage
        rijeci = [r for r in pattern.findall(linija) if not r.isdigit()]
        brojac.update(rijeci)

with open(IZLAZNA, "w", encoding="utf-8") as f_out:
    for rijec, frekvencija in brojac.most_common():
        f_out.write(f"{frekvencija}\t{rijec}\n")

print("Rječnik je uspješno generiran u UTF-8 formatu!")
