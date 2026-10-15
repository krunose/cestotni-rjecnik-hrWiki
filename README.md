# Čestotni rječnik hrvatske Wikipedije

Ovaj projekt sadrži čestotni (frekvencijski) rječnik izrađen na temelju cjelokupnog korpusa tekstova s **hrvatske Wikipedije**. Rječnik je koristan za jezična istraživanja, obradu prirodnog jezika (NLP), razvoj OCR sustava, provjeru pravopisa i druge računalno-lingvističke primjene.

## Statistika korpusa
* **Datum preuzete base (dump):** 1. listopad 2026 ([preuzimanje](https://dumps.wikimedia.org/other/mediawiki_content_current/))
* **Ukupan broj članaka:** između 235 000 i 236 000
* **Ukupan broj riječi (tokena):** 53 629 419
* **Broj jedinstvenih pojavnica:** 1 487 585

## Oblik izlaznih podataka
| frekvencija | riječ |
| :--- | :--- | 
| 2197625 | je |
| 22969 | hrvatski |
| 780 | rječnik |

## Metodologija obrade
Prilikom ekstrakcije i čišćenja teksta primijenjeni su sljedeći koraci:
* **Uklanjanje koda:** Čišćenje svih Wikipedijinih oznaka, predložaka i slično koristeći `pythonov` modul `wikiextractor`. Čišćenje koda provedeno je naredbom (GNU/Linux) `pipx run wikiextractor hrwiki-2026-10-01-p1p819304.xml --no-templates -b 3000M -o wiki_privremeno`
* **Uklanjanje preostaloga koda:** nakon `wikiextractora` ostali su određene oznake poput `<doc>`, čišćenje je provedeno na operacijskom sustavu GNU/Linux naredbom `sed 's/<[^>]*>//g' wiki_00 > čisti-izlaz`
* **Čišćenje:** Uklonjeni su interpunkcijski znakovi, specijalni simboli i brojevi skriptom [`izradi-čestotni-rječnik.py`](https://github.com/krunose/cestotni-rjecnik-hrWiki/tree/main/tools). Skripta uklanja interpunkciju i brojeve, uzima pojavnice, uzima i broji pojavnice i izvozi jedinstvene pojavnice.
* **Lemantizacija** nije provedena jer ne postoji dostupan i otvoren alat za ovaj zadatak.
* **veliko i malo slovo** nije se diralo kako se ne bi uništilo veliko i malo slovo u osobnim imenima. Nedostatak pristupa je što su velika slova ostala i na početku rečenice. Međutim nije teško programski učitati popis, provjeriti postoji li za određenu riječ (oblik) upis velikim i malim slovom, zbrojiti pojavljivanja i napraviti novi čestotni popis; no to je na onome kome to treba.

Skripta `izradi-čestotni-rječnik.py` izrađena je pomoću umjetne inteligencije kako bi se ubrzao proces stvaranja čestotnoga rječnika.

## Licenca i izvori
* **Izvor podataka:** Sadržaj je preuzet s [Hrvatske Wikipedije](https://wikipedia.org) i licenciran je pod CC BY-SA 4.0.
* **Licenca koda/rječnika:** Ovaj projekt je pod licencijom LGPLv3+ (sam rječnik, ali i sve popratne skripte i alati.)

Krunoslav Šebetić (listopad 2026.)
kruno.se@gmx.com

