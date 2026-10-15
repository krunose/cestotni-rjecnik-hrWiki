# Pretvaranje brojčanog zapisa u slovni

Modul dodatka `Numbertext` za hrvatski jezik koji omogućuje pretvaranje brojeva zapisanih znamenkama (brojčani zapis) u riječi (slovni zapis).

## Značajke modula

Trenutačno su podržane sljedeće pretvorbe:

| Kategorija | Opis | Primjeri |
| :--- | :--- | :--- |
| **Glavni brojevi** | Pretvorba cijelih brojeva (od nule do decilijardi) | `102` → sto dva<br>`5000` → pet tisuća |
| **Negativni brojevi** | Podrška predznak minus | `-15` → minus petnaest |
| **Decimalni brojevi** | Sklanjanje uz riječ "cijelo/cijela/cijelih" | `1.5` → jedno cijelo i pet<br>`2.3` → dva cijela i tri |
| **Redni brojevi** | Podržana sva tri roda (muški, ženski, srednji) | `ord:1` → prvi<br>`ord-fem:1` → prva<br>`ord-neu:1` → prvo |
| **Valute i novčani iznosi** | Automatsko dodavanje valuta i sklanjanje | `101 EUR` → sto jedan euro<br>`5.50 €` → pet eura i pedeset centi |

## Primjeri korištenja u LibreOfficeovu Calcu

Potrebno je sa [stranice LibreOfficeovih dodataka](https://extensions.libreoffice.org/en/extensions/show/numbertext-1) preuzeti i instalirati proširenje `Numbertext`.

Primjer formule: `=NUMBERTEXT(1235;"hr")` → `tisuću dvjesto trideset pet`.

### Glavni i decimalni brojevi
* `0` → nula
* `21.5` → dvadeset jedno cijelo i pet
* `1000000` → jedan milijun

### Redni brojevi
Ovisno o kontekstu irodu, možete pozvati specifičnu funkciju:
* `ord:12` → dvanaesti (muški rod)
* `ord-fem:12` → dvanaesta (ženski rod)
* `ord-neu:12` → dvanaesto (srednji rod)

### Valute
Modul prepoznaje oznake valuta prije ili poslije broja (kn, €, $, USD, EUR, HRK...):
* `1 kn` → jedna kuna
* `2 kn` → dvije kune
* `5 kn` → pet kuna
* `12.34 EUR` → dvanaest eura i trideset četiri centa

## Tehnologija i sintaksa

Ovaj jezični paket napisan je u jeziku **Soros**, koji se koristi unutar alata **Numbertext**. Pravila se temelje na regularnim izrazima i rekurzivnom raščlanjivanju brojeva.

Za više informacija o samom programskom jeziku i integraciji s LibreOffice/OpenOffice ili drugim sustavima posjetite službenu stranicu [numbertext.org](http://numbertext.org).

## Autori i povijest razvoja

* **Krunoslav Šebetić (2026)** - Ispravak i proširenje glavnih brojeva, izrada rednih brojeva te, uz pomoć umjetne inteligencije, implementacija generiranja decimalnih brojeva kruno.se@gmx.com
* **Mihovil Stanić (2014)** - Prilagodba dijela koda za valute.
* **Goran Rakić (2009)** - Izvorna srpska verzija na kojoj se temelji dio koda za valute.

## Licencija

Ovaj projekt je dostupan pod dvostrukom licencom (Dual-licensed):
1. **Creative Commons 3.0 Attribution-ShareAlike** (CC BY-SA 3.0)
2. **GNU Lesser General Public License** (LGPL v3) ili novija

Slobodno možete koristiti, modificirati i dijeliti ovaj kod uz zadržavanje informacija o autorima i iste licence.

