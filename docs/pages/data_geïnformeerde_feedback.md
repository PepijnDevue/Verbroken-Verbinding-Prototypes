# Data-Geïnformeerde Feedback

Data-Geïnformeerde Feedback haalt bruikbare redactionele feedback uit lezersreacties onder een nieuwsartikel. Het filtert ruis en klachten, en bundelt alleen de punten die de redactie kan gebruiken om het artikel te verbeteren.

---

## 1. Hoe werkt het

### Input
De AI krijgt twee dingen:
1. **Het nieuwsartikel** - De volledige tekst van het artikel. Alleen de tekstuele inhoud wordt meegenomen; afbeeldingen, video's en andere media worden niet geanalyseerd.
2. **De reacties** - Alle commentaren onder het artikel, inclusief replies.

### Verwerking
Het systeem werkt in twee stappen:

**Stap 1: Per reactie filteren**
Voor elke reactie-thread bepaalt de AI: staat hier expliciete feedback voor de redactie in? Alleen reacties die direct verwijzen naar het artikel of redactionele keuzes (titel, feiten, bronnen, ontbrekende context) worden meegenomen. Algemene klachten of meningen zonder verwijzing naar het artikel worden genegeerd.

**Stap 2: Samenvoegen tot rapport**
Alle gevonden feedbackpunten worden gebundeld tot één rapport. Dubbele punten worden samengevoegd, de toon wordt geneutraliseerd, en het resultaat is een professioneel overzicht voor de redactie.

### Output
Het model geeft twee outputs:

1. **Beredenering**: Een uitleg van hoe de AI tot het rapport is gekomen.
2. **Feedbackrapport**: Een gestructureerd overzicht van alle feedbackpunten, gegroepeerd per onderwerp.

---

## 2. Totstandkoming

### Data
We hebben gekozen voor een artikel van Omroep Venlo, omdat zij een publieke reactiesectie hebben via Facebook. Dit gaf ons toegang tot echte lezersreacties om te bepalen wat wel en geen bruikbare feedback is.

### Tests
De prompts zijn iteratief verbeterd door:
- Vergelijking van AI-output met handmatige analyse
- Aanscherpen van regels om ruis te verminderen
- Testen met verschillende soorten reactiesecties

### De huidige prompts

Het systeem gebruikt twee prompts: één voor het filteren per thread, en één voor het samenvoegen.

#### Prompt 1: Filteren per thread

**DOEL**
> Je analyseert één thread onder een nieuwsartikel (één hoofdcomment + alle replies). Je taak is uitsluitend te bepalen of er expliciete feedback aan de redactie over het artikel in staat.

**HARDERE REGELS**
> - Alleen feedback opnemen die duidelijk gericht is op het artikel of de redactie.
> - Reacties die een probleem beschrijven zonder het artikel te benoemen zijn geen feedback.
> - Alleen als een gebruiker expliciet verwijst naar het artikel of iets dat de redactie heeft gedaan/nagelaten (titel, feit, bron, uitleg, fout, gemis) mag het meetellen.
> - Geen interpretaties, geen afleidingen, geen pogingen intenties te raden.
> - Als er geen expliciete verwijzing is naar het artikel of redactionele keuzes: resultaat is leeg.

**WERKWIJZE**
> 1. Lees het artikel.
> 2. Lees de volledige thread.
> 3. Beantwoord alleen deze vraag: Is er een reactie die expliciet de redactie aanspreekt?
> 4. Zo ja: vat dat kort en feitelijk samen.
> 5. Zo nee: geef een lege string.

**INPUT**
> Het artikel en de thread worden hier ingevoegd.

**OUTPUT**
> Een beredenering en een resultaat (samenvatting of leeg).

#### Prompt 2: Samenvoegen tot rapport

**DOEL**
> Je ontvangt een lijst met samengevatte feedback per thread. Je taak is om alle aanwezige feedbackpunten te combineren tot één samenhangend, constructief en professioneel redactierapport.

**INHOUDSRICHTLIJNEN**
> - Lees de artikeltekst als context voor interpretatie.
> - Gebruik alle feedback die niet leeg is.
> - Cluster gelijkaardige punten (bijv. titelproblemen, feitencontrole, ontbrekende context, bronnen, toon).
> - Vermijd herhaling en bundel dubbele signalen.
> - Formuleer neutraal, professioneel en zonder agressie.
> - Geen namen, geen quotes, geen verzonnen punten.

**WERKWIJZE**
> 1. Lees eerst de artikeltekst.
> 2. Lees alle feedbackpunten.
> 3. Groepeer en synthetiseer alle feedback in logische categorieën.
> 4. Schrijf een beredenering van je analyse.
> 5. Schrijf een geclusterde, geordende feedbackrapportage.

**INPUT**
> Het artikel en alle feedbackpunten worden hier ingevoegd.

**OUTPUT**
> Een beredenering en een samenvatting.

---

## 3. Zelf maken

1. **Definieer wat feedback is** - Bepaal welke soorten reacties bruikbaar zijn voor jouw redactie.
2. **Verzamel voorbeelden** - Analyseer handmatig reacties om traindata te verzamelen.
3. **Train een classificatiemodel** - Train een model dat per reactie bepaalt of het bruikbare feedback bevat.
4. **Aggregeer met een taalmodel** - Gebruik een taalmodel met scherpgestelde instructies om alle gevonden feedbackpunten te bundelen tot een rapport.
5. **Integreer** - Koppel het systeem aan je CMS of redactietools.
6. **Verzamel feedback** - Laat redacteuren aangeven of de AI-feedback bruikbaar was, om het model te blijven verbeteren.
