# Leg Het Me Uit Knop

De Leg Het Me Uit Knop geeft lezers een korte, begrijpelijke uitleg bij een nieuwsartikel. Het vat de context samen op basis van een dossier met eerdere artikelen over hetzelfde onderwerp, zodat de lezer snel op de hoogte is.

---

## 1. Hoe werkt het

### Input
De AI krijgt twee dingen:
1. **Het nieuwsartikel** - De volledige tekst van het nieuwe artikel. Alleen de tekstuele inhoud wordt meegenomen; afbeeldingen, video's en andere media worden niet geanalyseerd.
2. **Het dossier** - Een verzameling eerdere artikelen over hetzelfde onderwerp, die samen de context vormen.

### Verwerking
Het systeem werkt stapsgewijs door het dossier:

1. De AI begint met een lege uitleg.
2. Voor elk artikel in het dossier (van oud naar nieuw) wordt de uitleg bijgewerkt met de nieuwe informatie uit dat artikel.
3. Als laatste wordt het nieuwe artikel verwerkt, zodat de uitleg volledig up-to-date is.

Op deze manier bouwt de AI een lopende samenvatting op die steeds wordt aangevuld met nieuwe informatie.

### Output
Het model geeft twee outputs:

1. **Beredenering**: Een uitleg van welke nieuwe informatie uit het artikel belangrijk is.
2. **Uitleg**: Een korte, begrijpelijke samenvatting van maximaal 150 woorden.

---

## 2. Totstandkoming

### Data
We maken gebruik van een dossier van Omroep Brabant. Dit gaf ons een reeks samenhangende artikelen over de verdwijning van Moerdijk om het concept mee te weergeven.

### Tests
De prompt is iteratief verbeterd door:
- Testen met dossiers van verschillende lengtes
- Aanscherpen van de instructies voor beknoptheid
- Controleren of nieuwe informatie correct wordt toegevoegd

### De huidige prompt

**DOEL**
> Je bent een expert in het uitleggen van nieuwsartikelen en de grotere context daaromheen. Je taak is om een begrijpelijke uitleg te geven van het gegeven artikel, zodat een gemiddelde lezer de inhoud en context beter kan begrijpen. Meestal is er een nieuw artikel toegevoegd aan een bestaand dossier. Dan vernieuw je de huidige uitleg met de nieuwe informatie. Je verwerkt alleen de korte nodige informatie uit de artikelen, geen quotes of details. Je verwerkt alle nieuwe informatie uit het nieuwe artikel, zo is de lezer helemaal op de hoogte.

**INSTRUCTIES**
> 1. Lees eerst de huidige uitleg goed door.
> 2. Lees daarna het nieuwe artikel aandachtig.
> 3. Bedenk welke nieuwe informatie uit het nieuwe artikel belangrijk is voor de lezer om te weten, beredeneer dit goed en schrijf het onder BEREDENEER.
> 4. Werk de huidige uitleg bij met deze nieuwe informatie, zodat de lezer een compleet beeld krijgt, schrijf dit onder UITLEG.

**REGELS**
> - Gebruik een heldere, toegankelijke taal.
> - Houd de uitleg super beknopt en to the point, maximaal 150 woorden.
> - Vermijd jargon en ingewikkelde termen.
> - Focus op de kerninformatie en context.

**INPUT**
> De huidige uitleg en het nieuwe artikel worden hier ingevoegd.

**OUTPUT**
> Een beredenering en een bijgewerkte uitleg.

---

## 3. Zelf maken

1. **Bouw een dossiersysteem** - Groepeer artikelen per onderwerp, zodat je weet welke artikelen bij elkaar horen.

2. **Kies een aanpak voor het samenvattingsmodel:**
   - *Optie A*: Schrijf een prompt en geef een taalmodel instructies om samenvattingen te genereren.
   - *Optie B*: Verzamel handmatig geschreven samenvattingen als traindata en train een eigen samenvattingsmodel.

3. **Verwerk incrementeel** - Bouw de samenvatting stapsgewijs op per artikel, zodat nieuwe informatie wordt toegevoegd.
4. **Integreer** - Voeg een "Leg het me uit" knop toe aan je artikelpagina's die de samenvatting toont.
5. **Verzamel feedback** - Laat lezers aangeven of de uitleg duidelijk was, om het systeem te blijven verbeteren.
