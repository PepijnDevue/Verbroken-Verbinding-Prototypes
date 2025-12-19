# Gevoelswaarde

De gevoelswaarde van een nieuwsbegint is een score die weergeefd in hoeverre een nieuwsartikel emotioneel beladen is. Nieuwsgebruikers zien de score bij het nieuws die helpt bepalen of ze het bericht willen lezen, terwijl redacties inzicht krijgen in de emotionele impact van hun verhalen. **Zie idee-kaart X**.  

## De schaal

| Score | Betekenis | Voorbeeld |
|-------|-----------|-----------|
| 0 | Positief/opbeurend | Goed nieuws, succesverhalen, inspirerende verhalen |
| 1 | Neutraal | Zakelijk nieuws, feitelijke rapportage |
| 2 | Licht negatief | Beperkte zorgen, weinig details |
| 3 | Matig zwaar | Duidelijk leed, persoonlijke verhalen |
| 4 | Zwaar | Ernstige tragedies, schokkende details |
| 5 | Extreem | Extreme gebeurtenissen, overweldigend leed |

De AI kan ook halve punten geven (bijvoorbeeld 2.5 of 3.5) voor artikelen die tussen twee categorieen in vallen. Dit zorgt voor meer precisie wanneer een artikel niet duidelijk in een enkele categorie past. 

---

## 1. Hoe werkt het

### Input
De AI krijgt het volledige nieuwsartikel als tekst: de titel en de volledige artikeltekst. Afbeeldingen, video's en andere media worden niet meegenomen in de analyse. De score is dus puur gebaseerd op de geschreven inhoud van het artikel. 

### Verwerking
We gebruiken een taalmodel dat instructies kan volgen. Het model krijgt een prompt met daarin de schaal, de factoren, en het artikel. Het model analyseert het artikel op vier factoren: 

- **Inhoud**: Hoe ernstig is de gebeurtenis objectief gezien?
- **Type**: Kinderen, geweld tegen groepen, en misbruik wegen zwaarder. Politiek en economie wegen lichter.
- **Presentatie**: Emotionele woorden en persoonlijke details maken het zwaarder.
- **Nabijheid**: Nederlandse context weegt zwaarder dan ver weg.

### Output
Het model geeft twee outputs:

1. **Beredenering**: Een korte analyse waarin het model uitlegt hoe het tot de score is gekomen, gebaseerd op de vier factoren.
2. **Score**: Een getal tussen 0 en 5 (met halve punten voor nuance).

---

## 2. Totstandkoming

### Data
We hebben tientallen nieuwsartikelen handmatig gescoord om te bepalen wat een goede schaal is. Dit waren artikelen uit verschillende categorieen en bronnen.

### Tests
De schaal en prompt zijn iteratief verbeterd door:
- Vergelijking van AI-scores met handmatige scores
- Aanscherping van onduidelijke gevallen
- Toevoegen van regels voor specifieke situaties (bijv. kinderen)

### De huidige prompt

De prompt bestaat uit de volgende onderdelen:

**DOEL**
> Je bent een expert in het scoren van nieuwsartikelen op emotionele zwaarte op een schaal van 0 tot 5. Je taak is om nieuwsartikelen te analyseren en een score toe te kennen op basis van hun emotionele impact vanuit een Nederlands perspectief.

**INSTRUCTIES**
> Lees het volledige artikel en analyseer de emotionele impact. Geef een uitleg van je analyse en score, dek alle aspecten kort. Schrijf dit onder BEREDENEER. Geef daarna alleen de score als een getal tussen 0 en 5 onder SCORE.

**SCHAAL**
> - 0-0.5: POSITIEF - Vreugde, trots, inspiratie. Emotionele woorden, succesverhalen, menselijke veerkracht.
> - 1.0: NEUTRAAL - Zakelijk, feitelijk, geen emotie. Geen persoonlijke verhalen of betrokkenheid.
> - 2.0: LICHT NEGATIEF - Beperkte zorgen, zakelijke toon, weinig details, lage nabijheid.
> - 3.0: MATIG ZWAAR - Duidelijk menselijk leed, persoonlijke verhalen, emotionele quotes, identificeerbare slachtoffers.
> - 4.0: ZWAAR - Ernstige tragedies, schokkende details, sterke emotionele taal, impact op gemeenschappen.
> - 5.0: EXTREEM - Extreme wreedheid/massa slachtoffers, overweldigend leed, traumatische details.

**FACTOREN**
> - Inhoud: Objectieve ernst (slachtoffers, schade, maatschappelijke impact).
> - Type gebeurtenis: Zwaarder (kinderen, geweld tegen groepen, misbruik, massa ongelukken, moord, systemisch falen). Lichter (politiek, economie, verkeersongelukken, natuurrampen zonder leed).
> - Presentatie: Emotionele woorden, persoonlijke details, quotes betrokkenen, visualiseerbare beschrijvingen = zwaarder.
> - Nabijheid: Nederland/Nederlanders/herkenbaar = zwaarder. Ver weg/vreemd = lichter (tenzij extreem).

**REGELS**
> - Emotionele presentatie weegt het zwaarst, ook bij mindere ernst.
> - Acute crisis is zwaarder dan chronisch probleem.
> - Kinderen altijd +0.5 tot +1 zwaarder.
> - Gebruik halve punten voor nuance.

**ARTIKEL**
> Hier wordt de titel en tekst van het artikel ingevoegd.

**BEREDENEER**
> Hier begint het model met zijn analyse.

---

## 3. Zelf maken

1. **Praat met je publiek** - Wanneer wordt nieuws door hen ervaren als zwaar?.
2. **Definieer je schaal** - Bepaal wat de scores betekenen voor jouw context, en verbind textuele kenmerken aan de score.
2. **Verzamel voorbeelden** - Score handmatig een set artikelen als traindata.
3. **Train een model** - Train je eigen sentiment-analyse model op basis van je gelabelde data.
4. **Test en verbeter** - Vergelijk model-output met je handmatige scores en pas aan.
5. **Integreer** - Koppel het model aan je workflow.
6. **Verzamel feedback** - Laat gebruikers feedback geven op de scores om meer traindata te verzamelen en het model te blijven verbeteren.
