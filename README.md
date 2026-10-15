# Čestotni rječnik hrvatske Wikipedije

Ovaj projekt sadrži čestotni (frekvencijski) rječnik izrađen na temelju cjelokupnog korpusa tekstova s **hrvatske Wikipedije**. Rječnik je koristan za jezična istraživanja, obradu prirodnog jezika (NLP), razvoj OCR sustava, provjeru pravopisa i druge računalno-lingvističke primjene.

## Statistika korpusa
* **Datum stvaranja baze (dump):** 1. listopad 2026 ([preuzimanje](https://dumps.wikimedia.org/other/mediawiki_content_current/))
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
* **Čišćenje:** Uklonjeni su interpunkcijski znakovi, specijalni simboli i brojevi skriptom [`izradi-čestotni-rječnik.py`](https://github.com/krunose/cestotni-rjecnik-hrWiki/tree/main/tools). Skripta uklanja interpunkciju i brojeve, broji i izvozi jedinstvene pojavnice.
* **Lematizacija** nije provedena jer je `python` i modul `classla` izvan naših trenutačnih mogućnosti, a baza podataka je prevelika za računalo na kojemu radimo  (skripta `izradi-čestotni-rječnik.py` izrađena je uz pomoć umjetne inteligencije)
* **veliko i malo slovo** Rješilo se tako što se veliko i malo slovo u prvom prolazu kroz sirov tekst (dump) nije diralo. Zatim se u drugom prolazu usporedilo unakrsnim uspređivanjem (radi homonima i zaštite vlastitih imena) ponovno provjerilo nalaze li se riječi upisane velikim slovom isključivo velikim slovom na početku rečenice, a inače malim. Ako da, pretvorilo ih se u mala slova, ako se pak pojavljuju velikim slovom i u sredini rečenice, nije ih se diralo.

## Algoritam za ispravljanje velikoga i maloga slova

Cijeli proces započeo je preuzimanjem i ekstrakcijom cjelokupnog tekstualnog odlagališta (dump) s hrvatske Wikipedije pomoću alata `wikiextractor`, nakon čega je preostali `XML` kod dodatno očišćen alatom `SED` unutar GNU/Linux terminala. Kako bi se iz sirovog, vezanog teksta uklonili brojevi i interpunkcija te prebrojale jedinstvene pojavnice, izrađena je skripta (AI) `izradi-čestotni-rječnik.py`, koja je generirala sirovi čestotni rječnik ne vodeći računa o velikom i malom slovu: opće imenice na početku rečenice ili odlomka bile su zapisane velikim slovom, što je umjetno razdvojilo njihovu frekvenciju od oblika s malim slovom. Kako bi se taj šum očistio bez skupog pokretanja teških jezičnih modela poput modula `classla`, osmišljen je lagan i brz algoritam za unakrsnu provjeru (cross-reference) izravno na postojećim datotekama.

U prvoj fazi unakrsne provjere, program je u jednom prolazu učitao sirovi tekst Wikipedije i pomoću pravilnih izraza izdvojio sve riječi s velikim slovom koje se nalaze isključivo na početku rečenice. Istovremeno, isti je algoritam pratio i bilježio svako pojavljivanje riječi s velikim slovom u sredini rečenice kako bi prepoznao stvarna vlastita imena, poput naziva država ili gradova. Ključni trenutak unakrsnog povezivanja dogodio se matematičkim oduzimanjem tih dvaju skupova, čime je stvoren popis riječi koje se u cijeloj Wikipediji s velikim slovom javljaju samo i isključivo na početku rečenice.

Na samom kraju, program je učitao sirovi rječnik i pretražio svaku riječ: ako se riječ nalazila na popisu isključivo početnih riječi, njezino je slovo promijenjeno u malo, a njezina je frekvencija pribrojena odgovarajućem malom obliku. Riječi poput „Hrvatska” ili „Zagrebu” uspješno su detektirane u sredini rečenica, pa ih je algoritam preskočio i trajno zaštitio s velikim slovom. Cijeli ovaj optimizirani proces unakrsne provjere trajao je svega šezdesetak sekundi na starijem prijenosnom računalu Lenovo ThinkPad T440. Rezultat je rječnik očišćen od šuma, ali rezultirajući lingvistički upotrebljivim rječnikom koji razlikuje 'hrvatska kultura' od 'Hrvatska država'. Nedostataka u rječniku vjerojatno ima još, ali nemamo sklopovlje za pokretanje modula `classla` u `pythonu`.

## Licenca i izvori
* **Izvor podataka:** Sadržaj je preuzet s [Hrvatske Wikipedije](https://wikipedia.org) i licenciran je pod CC BY-SA 4.0.
* **Licenca koda/rječnika:** Ovaj projekt je pod licencijom LGPLv3+ (sam rječnik, ali i popratni alati.)

Krunoslav Šebetić (listopad 2026.)
kruno.se@gmx.com

