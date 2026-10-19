<?php

/**

debugging i provjera preformansi i memory leaks uz pomoć umjetne inteligencije

**/

$sourceFile = dirname(__DIR__) . '/prvih-milijun-pojavnica';
$destFile = "sortedLemasByLemaFrequency";

$collectFrequences = array();

$collectedFrequences = array();

$sourceFileHandle = fopen($sourceFile, "r");
$destFileHandle = fopen($destFile, "w");

/*

Zbrajanje frekvencija da se dobije popis najčešić riječi

*/

// preskoči prvi redak (zaglavlje)
$line = fgets($sourceFileHandle);

// čitanje datoteke redak po redak
while (($line = fgets($sourceFileHandle)) !== false) {

    // brisanje znakova za novi redak na kraju
    $line = trim($line);

    $explodeLine = explode("\t", $line);

    // Prvo provjeri postoje li ključevi na disku
    if(isset($explodeLine[7]) && isset($explodeLine[1])) {

        $frekvencija = intval(trim($explodeLine[1]));

        // Tvoj uvjet: Nastavi obradu samo ako je frekvencija veća ili jednaka 5
        if ($frekvencija >= 5) {

            $lema = trim($explodeLine[7]);
            $pojavnica = trim($explodeLine[5]);

        } else {

            continue; // Preskoči hapokse

        }

    } else {

        continue; // Preskoči retke bez leme

    }

    // ako je frekvencija broj i ako lema nije broj jer imam podatke i gdje je lema 0
    if(is_numeric($frekvencija) && !is_numeric($lema)) {

        // Popravljena logika: ako lema ne postoji, inicijaliziraj je
        if(!isset($collectFrequences[$lema])) {

            $collectFrequences[$lema][0] = $frekvencija;
            $collectFrequences[$lema][1][$pojavnica] = $pojavnica;

        // Ako lema već postoji, pribroji frekvenciju i dodaj unikatnu pojavnicu kroz ključ
        } else {

            $collectFrequences[$lema][0] += $frekvencija;
            $collectFrequences[$lema][1][$pojavnica] = $pojavnica;

        }

    }

}

// Sortiranje višedimenzionalnog polja prema frekvenciji na indeksu [0] (silazno)
uasort($collectFrequences, function($a, $b) {

    if ($a[0] == $b[0]) {

        return 0;

    }

    // Ako je frekvencija elementa 'b' veća, gurni ga prema gore (silazni poredak)
    return ($a[0] < $b[0]) ? 1 : -1;

});


// Zapisivanje zaglavlja u izlaznu datoteku radi preglednosti na GitHubu
fwrite($destFileHandle, "Frekvencija\tLema\tPojavnice\n");

$freqLine = "";

foreach($collectFrequences as $lemaKey => $lema) {

    $freqLine .= $lema[0] . "\t";
    $freqLine .= $lemaKey . "\t";

    // Spajamo unikatne pojavnice zarezom u istu liniju radi čiste tablične strukture
    $freqLine .= implode(", ", $lema[1]) . "\n";

    // Zapisivanje izlaza direktno na disk (da ThinkPad ne drži cijeli ispis u RAM-u)
    fwrite($destFileHandle, $freqLine);
    
    // Ispis radi praćenja napretka
    echo $freqLine;
    
    $freqLine = "";

}

fclose($sourceFileHandle);
fclose($destFileHandle);

?>

