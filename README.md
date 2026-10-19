# Čestotni rječnik hrvatske Wikipedije

Ovaj projekt sadrži čestotni (frekvencijski) rječnik izrađen na temelju cjelokupnog korpusa tekstova s hrvatske Wikipedije poredan frekvencijski (od najčešće do najrjeđe riječi) prema jedinstvenoj pojavnici, ne samoj lemi. Rječnik je koristan za jezična istraživanja, obradu prirodnog jezika (NLP), razvoj OCR sustava, provjeru pravopisa i druge računalno-lingvističke primjene.

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

**Statistički procesuiran rječnik** nalazi se u arhivi `čestotni-rječnik-hrWiki.zip`, kako bi se smanjila veličina rječnika pri prijenosu podataka na računalo korisnika. Podatci su strukturirani kao `tsv`, što znači da su razdvojeni tabulatorom, a time pogodni za unos u LibreOffice Calc.

U datoteci `čestotni-rječnik-hrWiki` **frekvencije** se odnose na **pojavnicu**, ne na lemu. Obrađene su sve riječi u hrvatskoj Wikipediji.

U datoteci `sortirano-prema-učestalosti-leme` **frekvencije** su dane u odnosu na **lemu**, ali tako da se **nije uvrstilo** one leme čije pojavnice imaju **manje od 5 pojavljivanja** jer je takvih riječi previše i hardver koji imamo to ne bi izdržao. A i brzim pregledom takvih riječi jasno je da bi lematizacija bila potpuno premašena (mahom strana i neprilagođena vlastita imena, rijetki i neprilagođeni toponimi, egzotizmi, riječi na stranim jezicima i pismima itd.)

Treba samo biti oprezan jer Calc ne može primiti više od 1 048 576 redaka. Izvući prvih milijun pojavnica moguće je na GNU/Linuxu iz naredbenoga retka naredbom `head -n 1000000 čestotni-rječnik-hrWiki > milijun-pojavnica`. Ako koga zanimaju hapoksi ili rijetke riječi općenito, kraj može izvući na GNU/Linuxu naredbom `tail -n 100000 čestotni-rječnik-hrWiki > sto-tisuća-zadnjih-pojavnica`.

U programu za obradbu proračunskih tablica moguće je proširiti postotak relativne frekvencije kako bi se dobili relevantni podatci za riječi koje se ne ponavljaju često; za LibreOffice Calc to je formula `=(<apsolutna frekvencija riječi> / 53106215) * 100` i poveća se broj decimalnih mjesta za prikaz.

## Metodologija obrade

Prilikom ekstrakcije i čišćenja teksta primijenjeni su sljedeći koraci:

* **Uklanjanje koda:** Za čišćenje Wikipedijinih oznaka, predložaka i slično, koristio se modul `wikiextractor` (programski jezik `python`). Čišćenje koda provedeno je naredbom (GNU/Linux) `pipx run wikiextractor hrwiki-2026-10-01-p1p819304.xml --no-templates -b 3000M -o wiki_privremeno`
* **Uklanjanje preostaloga koda:** nakon `wikiextractora` ostale su oznake poput `<doc>`, čišćenje je provedeno na operacijskom sustavu GNU/Linux naredbom `sed 's/<[^>]*>//g' wiki_00 > čisti-izlaz`
* **Čišćenje:** Uklonjeni su interpunkcijski znakovi, specijalni simboli i brojevi skriptom [`izradi-čestotni-rječnik.py`](https://github.com/krunose/cestotni-rjecnik-hrWiki/tree/main/tools). Skripta uklanja interpunkciju i brojeve, broji i izvozi jedinstvene pojavnice.
* **frekvencijska analiza** provedena je skriptom `čestotna-analiza.py`.
* **Veliko i malo slovo** U prvom se prolazu veliko i malo slovo nije diralo. Nedostatak je što su velika slova, pored osobnih imena, ostala i na riječima koje su stajale na početku rečenice. Da bi se to popravilo, u drugom prolazu se provjeravalo postoji li riječ upisana u rječnik velikim slovom gdje u korpusu u sredini rečenice a upisana isključivo malim slovom: ako jest, to je znak da se radi o početku rečenice, ne vlastitom imenu; tako se zaštitilo razlikovanje 'Hrvatska' (država) i 'hrvatska' (kultura). Naravno, nesavršenosti ima. Koristio se i prag: ako je pojavnica u 95 % slučajeva bila upisana malim slovom, pretvarala se u malo slovo. Ovo je rješava problem homonimije, ali je upotrebljivo.
* **Lematizacija** Lematizacija je provedena u dva koraka jer nemamo dovoljno snažno sklopovlje da 1,4 milijuna jedinstvenih pojavnica propustimo kroz modul `classla`. U prvom potezu koristio se označen rječnik [`hr500k`](https://github.com/reldi-data): uzela se pojavnica iz čestotnoga rječnika, pronašla se ista pojavnica u hr500k i ako je došlo do podudaranja, lema je prepisana u čestotni rječnik. Problem je što se uzimala najčešća lema, homonimi se ovdje nisu rješavali jer bez konteksta rečenice - a nemamo sklopovlje za to - jednostavno nema načina. U drugoj ruci se lematizacija provela pomoću modula `classla` (programski jezik `python`). Naime skriptom `lematizacija-iz-hr500k.py` izvukle su se leme i pojavnice iz korpusa `hr500k`, usporedile su se sa bazom `čestotni-rječnik-hrWiki` i leme iz `hr500k` zalijepile su se na čestotni rječnik ako su se jedinstvene pojavnice podudarale. Naravno, one jedinstvene pojavnice koje nisu postojale u `hr500k` ostale su nelematizirane - zato `classla`: učitao se djelomično lematiziran rječnik, jedinstvene pojavnice bez leme suprotstavljene su korpusu, provjerava se pojavnica u kontekstu jedne rečenice, iz koje je `classla` izvukla leme (skripta `lematizacija-s-classla-nakon-hr500k.py`). Lematizacija se radi u serijama jer hardver ne može prožvakati sve u jednom zalogaju. Nakon nekog vremena postavljen je prag da se ne lematiziraju riječi koje imaju manje od 5 pojavljivanja jer hardver više od toga neće podnijeti. **Pogreške pri lematiziranju** mogu biti rezultat našega (možda) nepravilnoga (prilično rudimentarnoga) rastavljanja na rečenice, pa `classla` možda nije uvijek imala pun kontekst. Ipak: nasumični odabir 2000 jedinstvenih pojavnica (lematiziranih, dakle više od 5 pojavljivanja) proslijeđen je umjetnoj inteligenciji na procjenu, koja je iznosila preko 90 % i koliko to sada vrijedi ne znam.

## Algoritam za ispravljanje velikoga i maloga slova

Cijeli proces započeo je preuzimanjem i ekstrakcijom tekstnog odlagališta (engl. 'dump') s hrvatske Wikipedije pomoću alata `wikiextractor`, nakon čega je preostali `XML` kod dodatno očišćen alatom `sed` unutar GNU/Linux terminala. Kako bi se iz sirovog, vezanog teksta uklonili brojevi i interpunkcija te prebrojale jedinstvene pojavnice, izrađena je skripta (generirao AI radi uštede vremena) `izradi-čestotni-rječnik.py`, koja je stvorila sirovi čestotni rječnik ne vodeći računa o velikom i malom slovu: opće imenice na početku rečenice ili odlomka bile su zapisane velikim slovom, što je umjetno razdvojilo njihovu frekvenciju od oblika s malim slovom. Kako bi se taj šum očistio, osmišljen je lagan i brz algoritam za unakrsnu provjeru (cross-reference) izravno na postojećim datotekama.

U prvoj fazi unakrsne provjere, program je u jednom prolazu učitao sirovi tekst Wikipedije i pomoću pravilnih izraza izdvojio sve riječi s velikim slovom koje se nalaze isključivo na početku rečenice. Istovremeno, isti je algoritam pratio i bilježio svako pojavljivanje riječi s velikim slovom u sredini rečenice kako bi prepoznao stvarna vlastita imena, poput naziva država ili gradova. Ključni trenutak unakrsnog povezivanja dogodio se matematičkim oduzimanjem tih dvaju skupova, čime je stvoren popis riječi koje se u cijeloj Wikipediji s velikim slovom javljaju samo i isključivo na početku rečenice.

Na samom kraju, program je učitao sirovi rječnik i pretražio svaku riječ: ako se riječ nalazila na popisu riječi koje su pisane velikim slovom isključivo na početku rečenice, njezino je slovo promijenjeno u malo, a njezina je frekvencija pribrojena odgovarajućem obliku (već upisanom malim slovom). Riječi poput „Hrvatska” ili „Zagrebu” uspješno su detektirane u sredini rečenica, pa ih je algoritam preskočio i trajno zaštitio s velikim slovom. Cijeli ovaj optimizirani proces unakrsne provjere trajao je svega šezdesetak sekundi na starijem prijenosnom računalu Lenovo ThinkPad T440. Rezultat je rječnik relativno dobro očišćen od šuma rezultirajući upotrebljivim rječnikom koji razlikuje 'hrvatska kultura' od 'Hrvatska država'.

Druga faza algoritma predstavlja ključni dio lingvističke provjere u kojoj se donosi odluka o sudbini svake riječi uočene na početku rečenice. Na samom početku, sve jednoslovne riječi, poput prijedloga i veznika *U, I, O, A*, automatski se šalju na popis za smanjivanje jer u hrvatskom jeziku jedno slovo ne može biti samostalno vlastito ime. Za sve ostale, višeslovne riječi program računa omjer velikih i malih slova isključivo u sredini rečenice. Program precizno zbraja koliko se puta određena riječ unutar teksta piše velikim, a koliko malim slovom, te na temelju tih brojki izračunava točan postotak pojavljivanja malog slova. 

U ovom koraku primijenjen je statistički prag tolerancije koji iznosi 95%. Ako udio malog slova u sredini rečenice prelazi zadani prag, riječ se proglašava općom, običnom riječi, kao što je to slučaj s riječima *Nakon* ili *Za*. Takva se riječ potom sigurno dodaje na popis za smanjivanje, dok se u suprotnom slučaju, kada je udio malog slova manji od 95%, riječ prepoznaje kao stvarno vlastito ime, poput imenica *Hrvatska* ili *Zagrebu*. Vlastita imena se u tom trenutku preskaču i ostaju zaštićena velikim slovom.

Nedostataka u rječniku vjerojatno ima još, ali nemamo sklopovlje ni vrijeme da to odradimo pedantnije ili pregledavamo ručno.

## Pomoć umjetne inteligencije

Alate pisane programskim jezikom `pyhton` izradila je umjetna inteligencija jer baratamo samo programskim jezikom `PHP`. Modul `classla` radi samo s programskim jezikom `python`. Alate pisane `PHP`-om umjetna inteligencija je optimizirala. Dio teksta `Algoritam za ispravljanje velikoga i maloga slova` napisala je također umjetna inteligencija prema mojim uputama i ispravljanjima (tekst je moderiran). Čovjek je osmislio algoritam, ali je umjetna inteligencija to pretočila u `pyhton` i objasnila vlastiti kôd.

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

