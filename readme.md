# iCalendar voor MijnAfvalwijzer.nl
De dienst MijnAfvalwijzer.nl wordt door veel gemeenten gebruikt voor het informeren over de ophaaltijden van het afval.
De ophaaltijden staan per maand overzichtelijk op de website en er is een app.
Helaas biedt MijnAfvalwijzer.nl niet een iCal kalender feed waarmee het ophaalschema overzichtelijk in je favoriete kalender app wordt getoond.

Het script mijnafvalwijzer-to-ical.py haalt het ophaalschema op aan de hand van de opgegeven postcode en huisnummer en genereert een ics bestand.
Voor het gemak kan er ook een Docker image worden gemaakt.

## Gebruik
Het script heeft 3 argumenten, waarvan de eerste 2 verplicht zijn:
  1. Postcode
  - Huisnummer
  - Comma-gescheiden lijst van afvalsoorten die in de iCal feed terecht moeten komen. De beschikbare waarden zijn:
    - `gft`: Voor groente, fruit en tuinafval
    - `glas`: Voor glas
    - `grofvuil`: Voor grofvuil
    - `kca`: Voor klein chemisch afval
    - `papier`: Voor papier en karton
    - `pd`: Voor plastic en drankverpakkingen
    - `pmd`: Plastic, Metalen en Drankkartons
    - `restafval`: Voor restafval
    - `textiel`: Voor textiel

Voorbeeld:

    python mijnafvalwijzer-to-ical.py 3825AL 41 restafval,gft


Belangrijk: de uitvoer moet als UTF-8 worden opgeslagen voor gebruikt in veel iCal readers.

## Vereisten
Python 3 met de packages `beautifulsoup4`, `requests`, `icalendar`.
