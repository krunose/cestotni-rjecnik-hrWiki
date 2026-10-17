# Čestotni rječnik hrvatske Wikipedije

Ovaj projekt sadrži čestotni (frekvencijski) rječnik izrađen na temelju cjelokupnog korpusa tekstova s **hrvatske Wikipedije**. Rječnik je koristan za jezična istraživanja, obradu prirodnog jezika (NLP), razvoj OCR sustava, provjeru pravopisa i druge računalno-lingvističke primjene.

## Statistika korpusa
* **Datum stvaranja baze (dump):** 1. listopad 2026 ([preuzimanje](https://dumps.wikimedia.org/other/mediawiki_content_current/))
* **Ukupan broj članaka:** između 235 000 i 236 000 (procjena umjetne inteligencije 15. listopada 2026.)
* **Ukupan broj redaka** ili (zapravo) odlomaka je 1 412 879 (`wc -l <datoteka>`)
* **Ukupan broj riječi (tokena):** 53 106 215 (`wc -w <datoteka>`)
* **Broj jedinstvenih pojavnica:** 1 412 870

## Oblik izlaznih podataka

| Rang    | Apsolutna<br>frekvencija | Relativna frekvencija % | IPM    | Kumulativno % | Riječ    | Lema     |
| :------ | :----------------------- | :---------------------- | :----- | :------------ | :------- | :------- |
| 125     | 22 969                   | 0.0433%                 | 432.51 | 31.95%        | hrvatski | hrvatski |
| 7008    | 780                      | 0.0015%                 | 14.69  | 65.15%        | rječnik  | rječnik  |
| 712 136 | 2                        | 0.0000%                 | 0.04   | 95.21%        | čestotni | čestotni |

**Potpuno statistički procesuiran rječnik** nalazi se u arhivi `čestotni-rječnik-hrWiki.zip`, naime u obliku obične tekstne datoteke prevelik je izravno postavljanje na GitHub; ograničenje je 25 MB, a sam rječnik sa statističkim podatcima je dvostruko veći.

Podatci su razdvojeni tabulatorom tako da su i više nego pogodni za uvoz u program za izradu i obradu proračunskih tablica kao što je LibreOffice Calc. Treba samo biti oprezan jer je popis riječi veći negoli Calc može imati redaka (maksimum: 1 048 576). Nije probano u Microsoftovu Excelu, ali rijetko kada će tko trebati analizirati 1 412 879 jedinstvenih pojavnica, posebice zato što su riječi na dnu datoteke statistički irelevantne, osim ako se ne analizira baš njih; u tom se slučaju može odrezati vrh datoteke: `tail -n 500000 čestotni-rječnik-hrWiki > dno-rječnika`.

U programu za obradbu proračunskih tablica moguće je proširiti postotak relativne frekvencije kako bi se dobili relevantni podatci; za LibreOffice Calc to je formula `=(<apsolutna frekvencija> / 53106215) * 100` i poveća se broj decimalnih mjesta koliko već treba.

## Metodologija obrade
Prilikom ekstrakcije i čišćenja teksta primijenjeni su sljedeći koraci:
* **Uklanjanje koda:** Čišćenje svih Wikipedijinih oznaka, predložaka i slično koristeći `pythonov` modul `wikiextractor`. Čišćenje koda provedeno je naredbom (GNU/Linux) `pipx run wikiextractor hrwiki-2026-10-01-p1p819304.xml --no-templates -b 3000M -o wiki_privremeno`
* **Uklanjanje preostaloga koda:** nakon `wikiextractora` ostali su određene oznake poput `<doc>`, čišćenje je provedeno na operacijskom sustavu GNU/Linux naredbom `sed 's/<[^>]*>//g' wiki_00 > čisti-izlaz`
* **Čišćenje:** Uklonjeni su interpunkcijski znakovi, specijalni simboli i brojevi skriptom [`izradi-čestotni-rječnik.py`](https://github.com/krunose/cestotni-rjecnik-hrWiki/tree/main/tools). Skripta uklanja interpunkciju i brojeve, broji i izvozi jedinstvene pojavnice.
* **frekvencijska analiza** provedena je skriptom `čestotna-analiza.py` 
* **Lematizacija** lematizacija je provedena pomoću korpusa [hr500k](https://github.com/reldi-data) u pravoj ruci, u drugoj pomoću modula `classla` (programski jezik `python`). Naime skriptom `lematizacija-iz-hr500k.py` izvukle su se leme i pojavnice iz korpusa `hr500k`, usporedile su se sa bazom `čestotni-rječnik-hrWiki` i leme iz `hr500k` zalijepile su se na čestotni rječnik ako su se jedinstvene pojavnice podudarale. Naravno, one jedinstvene pojavnice koje nisu postojale u `hr500k` ostale su nelematizirane: to se riješilo modulom `classla`; učitao se djelomično lematiziran riječnik, jedinstvene pojavnice suprotstavljene su korpusu, provjerava se pojavnica u kontekstu (rečenici) i strojno se obrađuje modulom `classla` kako bi se dobile leme (skripta `lematizacija-s-classla-nakon-hr500k.py`). Lematizacija se radi u serijama jer hardver ne može prožvakati sve u jednom zalogaju.
* **veliko i malo slovo** Rješilo se tako što se veliko i malo slovo u prvom prolazu kroz sirov tekst (dump) nije diralo. Zatim se u drugom prolazu usporedilo unakrsnim uspređivanjem (radi homonima i zaštite vlastitih imena) ponovno provjerilo nalaze li se riječi upisane velikim slovom isključivo velikim slovom na početku rečenice, a inače malim. Ako da, pretvorilo ih se u mala slova, ako se pak pojavljuju velikim slovom i u sredini rečenice, nije ih se diralo.

## Algoritam za ispravljanje velikoga i maloga slova

Cijeli proces započeo je preuzimanjem i ekstrakcijom cjelokupnog tekstualnog odlagališta (dump) s hrvatske Wikipedije pomoću alata `wikiextractor`, nakon čega je preostali `XML` kod dodatno očišćen alatom `SED` unutar GNU/Linux terminala. Kako bi se iz sirovog, vezanog teksta uklonili brojevi i interpunkcija te prebrojale jedinstvene pojavnice, izrađena je skripta (AI) `izradi-čestotni-rječnik.py`, koja je generirala sirovi čestotni rječnik ne vodeći računa o velikom i malom slovu: opće imenice na početku rečenice ili odlomka bile su zapisane velikim slovom, što je umjetno razdvojilo njihovu frekvenciju od oblika s malim slovom. Kako bi se taj šum očistio bez skupog pokretanja teških jezičnih modela poput modula `classla`, osmišljen je lagan i brz algoritam za unakrsnu provjeru (cross-reference) izravno na postojećim datotekama.

U prvoj fazi unakrsne provjere, program je u jednom prolazu učitao sirovi tekst Wikipedije i pomoću pravilnih izraza izdvojio sve riječi s velikim slovom koje se nalaze isključivo na početku rečenice. Istovremeno, isti je algoritam pratio i bilježio svako pojavljivanje riječi s velikim slovom u sredini rečenice kako bi prepoznao stvarna vlastita imena, poput naziva država ili gradova. Ključni trenutak unakrsnog povezivanja dogodio se matematičkim oduzimanjem tih dvaju skupova, čime je stvoren popis riječi koje se u cijeloj Wikipediji s velikim slovom javljaju samo i isključivo na početku rečenice.

Na samom kraju, program je učitao sirovi rječnik i pretražio svaku riječ: ako se riječ nalazila na popisu isključivo početnih riječi, njezino je slovo promijenjeno u malo, a njezina je frekvencija pribrojena odgovarajućem malom obliku. Riječi poput „Hrvatska” ili „Zagrebu” uspješno su detektirane u sredini rečenica, pa ih je algoritam preskočio i trajno zaštitio s velikim slovom. Cijeli ovaj optimizirani proces unakrsne provjere trajao je svega šezdesetak sekundi na starijem prijenosnom računalu Lenovo ThinkPad T440. Rezultat je rječnik relativno dobro očišćen od šuma rezultirajući lingvistički upotrebljivim rječnikom koji razlikuje 'hrvatska kultura' od 'Hrvatska država'.

Druga faza algoritma predstavlja ključni dio lingvističke provjere u kojoj se donosi odluka o sudbini svake riječi uočene na početku rečenice. Na samom početku, sve jednoslovne riječi, poput prijedloga i veznika *U, I, O, A*, automatski se šalju na popis za smanjivanje jer u hrvatskom jeziku jedno slovo ne može biti samostalno vlastito ime. Za sve ostale, višeslovne riječi program računa omjer velikih i malih slova isključivo u sredini rečenice. Program precizno zbraja koliko se puta određena riječ unutar teksta piše velikim, a koliko malim slovom, te na temelju tih brojki izračunava točan postotak pojavljivanja malog slova. 

U ovom koraku primijenjen je statistički prag tolerancije koji iznosi 95%. Ako udio malog slova u sredini rečenice prelazi zadanih 95%, riječ se proglašava općom, običnom riječi, kao što je to slučaj s riječima *Nakon* ili *Za*. Takva se riječ potom sigurno dodaje na popis za smanjivanje, dok se u suprotnom slučaju, kada je udio malog slova manji od 95%, riječ prepoznaje kao stvarno vlastito ime, poput imenica *Hrvatska* ili *Zagrebu*. Vlastita imena se u tom trenutku preskaču i ostaju zaštićena velikim slovom, čime je izbjegnuta zamka homonimije u hrvatskom jeziku.

Nedostataka u rječniku vjerojatno ima još, ali nemamo sklopovlje za pokretanje modula `classla` u `pythonu`.

## Pomoć umjetne inteligencije

Alate pisane programskim jezikom `pyhton` izradila je umjetna inteligencija jer baratam samo programskim jezikom `PHP`. Dio teksta `Algoritam za ispravljanje velikoga i maloga slova` napisala je također umjetna inteligencija prema mojim uputama i ispravljanjima. Čovjek je osmislio algoritam, ali je umjetna inteligencija to pretočila u `pyhton` i objasnila vlastiti kôd.

## Licenca i izvori

Ovaj projekt kombinira podatkovne skupove otvorenog koda i računalno-lingvističke alate. Svi ugrađeni izvori i izvedeni podatci usklađeni su s uvjetima Creative Commons ShareAlike licenciranja.

### Izvori podataka i modela

| Izvor / Alat | Licenca | Opis korištenja |
| :--- | :--- | :--- |
| **Hrvatska Wikipedija** | [CC BY-SA 4.0](https://creativecommons.org) | Izvor cjelokupnog tekstualnog korpusa (dump od 1. listopada 2026.) koji služi kao temelj za izradu rječnika. |
| **Korpus hr500k (v2.0)** | [CC BY-SA 4.0](https://creativecommons.org) | Korišten za prvu fazu lematizacije unakrsnim mapiranjem jedinstvenih pojavnica. |
| **CLASSLA-Stanza model** | [CC BY-SA 4.0](https://creativecommons.org) | Python modul primijenjen za strojnu obradu i kontekstualnu lematizaciju preostalih nelematiziranih riječi. |

### Atribucija (Navođenje autora)

U skladu s uvjetima licenci CC BY-SA 4.0, u nastavku su navedeni službeni izvori i citati za korištene jezične resurse:

1. **Hrvatska Wikipedija:** Sadržaj je preuzet s [hr.wikipedia.org](https://wikipedia.org) ([dump](https://dumps.wikimedia.org/other/mediawiki_content_current/)).
2. **Korpus hr500k:** Ljubešić, Nikola; et al. (2023). *Croatian linguistic training corpus hr500k 2.0*. Slovenian language technologies research infrastructure CLARIN.SI. Dostupno na: [http://handle.net](http://handle.net).
3. **CLASSLA alat:** Terčon, Luka; et al. (2023). *The CLASSLA-Stanza model for lemmatisation of standard Croatian 2.1*. Dostupno na CLARIN.SI repozitoriju.

### Licenca koda i rječnika

Ovaj projekt (što uključuje sam čestotni rječnik, prateće baze i sve priložene skripte u repozitoriju) licenciran je pod:

* **[GNU Lesser General Public License v3.0 ili novija (LGPLv3+)](https://gnu.org)**

**Zašto ova licenca?** 
Prema pravilima Creative Commons CC BY-SA 4.0 licence, izvedena djela moraju se dijeliti pod istim ili kompatibilnim uvjetima (ShareAlike). Licenca LGPLv3 službeno je priznata od strane organizacije Creative Commons kao kompatibilna nizvodna licenca za prenošenje CC BY-SA 4.0 sadržaja. Ona osigurava copyleft zaštitu (kod i rječnik ostaju trajno slobodni za zajednicu), a istovremeno omogućuje jednostavnu integraciju u druge lingvističke i softverske sustave.

Krunoslav Šebetić (listopad 2026.)
kruno.se@gmx.com

