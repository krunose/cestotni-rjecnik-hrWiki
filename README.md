# Čestotni rječnik hrvatske Wikipedije

Ovaj projekt sadrži čestotni (frekvencijski) rječnik izrađen na temelju cjelokupnog korpusa tekstova s **hrvatske Wikipedije**. Rječnik je koristan za jezična istraživanja, obradu prirodnog jezika (NLP), razvoj OCR sustava, provjeru pravopisa i druge računalno-lingvističke primjene.

## Statistika korpusa
* **Datum stvaranja baze (dump):** 1. listopad 2026 ([preuzimanje](https://dumps.wikimedia.org/other/mediawiki_content_current/))
* **Ukupan broj članaka:** između 235 000 i 236 000 (procjena umjetne inteligencije na dan 15. listopada 2026.)
* **Ukupan broj redaka** ili (zapravo) odlomaka je 1 412 879 (`wc -l` <datoteka>)
* **Ukupan broj riječi (tokena):** 53 106 215 (`wc -w <datoteka>`)
* **Broj jedinstvenih pojavnica:** 1 412 870

## Oblik izlaznih podataka

| Rang    | Apsolutna<br>frekvencija | Relativna frekvencija % | IPM    | Kumulativno % | Riječ    |
| :------ | :----------------------- | :---------------------- | :----- | :------------ | :------- |
| 125     | 22 969                   | 0.0433%                 | 432.51 | 31.95%        | hrvatski |
| 7008    | 780                      | 0.0015%                 | 14.69  | 65.15%        | rječnik  |
| 712 136 | 2                        | 0.0000%                 | 0.04   | 95.21%        | čestotni |

**Potpuno statistički procesuiran rječnik** nalazi se u arhivi `statistički-procesuiran-čestotni-rječnik-hrWiki.zip`, naime u obliku obične tekstne datoteke prevelik je izravno postavljanje na GitHub; ograničenje je 25 MB, a sam rječnik sa statističkim podatcima je dvostruko veći.

Podatci su razdvojeni tabulatorom tako da su i više nego pogodni za uvoz u program za izradu i obradu proračunskih tablica kao što je LibreOffice Calc. Treba samo biti oprezan jer je popis riječi veći negoli Calc može imati redaka (maksimum: 1 048 576). Nije probano u Microsoftovu Excelu, ali rijetko kada će tko trebati analizirati 1 412 879 jedinstvenih pojavnica, posebice zato što su riječi na dnu datoteke statistički irelevantne, osim ako se ne analizira baš njih; u tom se slučaju može odrezati vrh datoteke: `tail -n 500000 čestotni-rječnik-hrWiki > dno-rječnika`.

U programu za obradbu proračunskih tablica moguće je proširiti postotak relativne frekvencije kako bi se dobili relevantni podatci; za LibreOffice Calc to je formula `=(<apsolutna frekvencija> / 53106215) * 100` i poveća se broj decimalnih mjesta koliko već treba.

## Metodologija obrade
Prilikom ekstrakcije i čišćenja teksta primijenjeni su sljedeći koraci:
* **Uklanjanje koda:** Čišćenje svih Wikipedijinih oznaka, predložaka i slično koristeći `pythonov` modul `wikiextractor`. Čišćenje koda provedeno je naredbom (GNU/Linux) `pipx run wikiextractor hrwiki-2026-10-01-p1p819304.xml --no-templates -b 3000M -o wiki_privremeno`
* **Uklanjanje preostaloga koda:** nakon `wikiextractora` ostali su određene oznake poput `<doc>`, čišćenje je provedeno na operacijskom sustavu GNU/Linux naredbom `sed 's/<[^>]*>//g' wiki_00 > čisti-izlaz`
* **Čišćenje:** Uklonjeni su interpunkcijski znakovi, specijalni simboli i brojevi skriptom [`izradi-čestotni-rječnik.py`](https://github.com/krunose/cestotni-rjecnik-hrWiki/tree/main/tools). Skripta uklanja interpunkciju i brojeve, broji i izvozi jedinstvene pojavnice.
* **frekvencijska analiza** provedena je skriptom `čestotna-analiza.py` 
* **Lematizacija** nije provedena. Uz pomoć umjetne inteligencije instalirala se i postavila `classla` i počelo se lematizirati 53 milijuna riječi, ali korpus je prevelik za računalo na kojem radimo. Ako je vjerovati procjeni, proces bi trajao nekoliko dana. Uz to, uzimati samo dio hrvatske Wikipedije ne daje reprezentativni korpus jer su članci poredani ili abecedno ili kronološki. Cijeli korpus ne možemo postaviti u repozitorij jer je maksimalna veličina datoteke 25 MB. Kome treba lematizirana hrvatska Wikipedija, morat će ponoviti kompletan proces i imati jako računalo.
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
* **Izvor podataka:** Sadržaj je preuzet s [Hrvatske Wikipedije](https://wikipedia.org) i licenciran je pod CC BY-SA 4.0.
* **Licenca koda/rječnika:** Ovaj projekt je pod licencijom LGPLv3+ (sam rječnik, ali i popratni alati.)

Krunoslav Šebetić (listopad 2026.)
kruno.se@gmx.com

