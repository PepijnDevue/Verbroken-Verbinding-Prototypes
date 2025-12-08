# Veertjes - Documentatie
<!-- 
## De formule

Om de emotionele beladenheid van een nieuwsartikel te meten op een schaal van 0 tot 5 (in stappen van 0.5) wordt de volgende formule gebruikt:

### Ingrediënten
- **Sentiment van de kop** (-1 tot 1):
    - -1 = negatief : *("Ongeluk op A2")*
    - 0 = neutraal : *("Parijs top van start gegaan")*
    - 1 = positief : *("Suriname 50 jaar onafhankelijk")*
- **Sentiment van de tekst** (-1 tot 1):
    - -1 = negatief : *("De brand verwoestte het huis volledig...")*
    - 0 = neutraal : *("De koning sprak met de ministers tijdens zijn staatsbezoek")*
    - 1 = positief : *("De hulpverleners konden het kind op tijd uit het water halen")*
- **Valentie van de tekst** (0 tot 1):
    - 0 = laag : *("...dat ... het meisje langere tijd van haar vrijheid hebben beroofd")*
    - 1 = hoog : *("Ze zat vast in een kooi, aan een ketting, en de klink van haar slaapkamerdeur was weggehaald.")*

### Hoe werkt de formule?
#### De kerngedachte
- Een negatief verhaal met hoge valentie = minimale score van 4/5
- Gevolgend uit de bovenstaande kerngedachte: de kop heeft minder invloed op de score dan de tekst zelf.
- De tekstvalentie werkt als een versterker van het sentiment, het maakt negatief sentiment nog negatiever en positief sentiment nog positiever.

#### De berekening
1. **Bereken de kopscore:**
    > De kopscore wordt simpelweg berekend als de helft van het sentiment van de kop. Zo houden we de kerngedachte in stand.

    `kopScore = kopSentiment * 0.5`
2. **Bereken de tekstversterker:**
    > Deze is nodig voor de tekstscore. Als de valentie laag is (0), dan is de versterker 1 en heeft het sentiment geen effect. Als de valentie hoog is (1), dan is de versterker 2 en wordt het sentiment verdubbeld.

    `versterker = 1 - tekstValentie + tekstValentie * 2`
3. **Bereken de tekstscore:**
    > Versterk het sentiment van de tekst met de berekende versterker.

    `tekstScore = tekstSentiment * versterker`
3. **Bereken de totale score:**
    > Hier worden de twee scores bij elkaar opgeteld en omgezet naar een schaal van 0 tot 5.
    
    `totaleScore = -1 * (tekstScore + kopScore) + 2.5`


## Schaal 2.0 -->

### 1. Definitie van Emotionele Zwaarte
Emotionele zwaarte meet de mate waarin een nieuwsartikel emotionele impact heeft op de Nederlandse lezer. Het is een samengestelde meting die rekening houdt met:

**A. Inhoudelijke ernst**
Objectieve zwaarte van de gebeurtenis (schade, slachtoffers, maatschappelijke impact)

**B. Type gebeurtenis**
Verschillende soorten gebeurtenissen hebben verschillende emotionele resonantie. Dit komt ook neer op de mate waarin de lezer zich kan inleven en zelf betrokken voelt. Politiek nieuws weegt bijvoorbeeld minder zwaar dan persoonlijk leed.

**B. Presentatie en stijl**
De presentatie van het nieuws beïnvloedt de emotionele impact aanzienlijk. Zo moet er gelet worden op emotionele woordkeuze, persoonlijke beschrijvingen en quotes van betrokkenen, en het detailniveau van de beschrijving van de gebeurtenissen. Hoe meer de lezer de gebeurtenis kan visualiseren en zich kan inleven, hoe zwaarder de emotionele impact.

**C. Nabijheid en herkenbaarheid (Nederlands perspectief)**
Een andere factor voor inleving is de geografische en culturele nabijheid en herkenbaarheid van de gebeurtenis. Gebeurtenissen in Nederland of met directe Nederlandse betrokkenheid wegen zwaarder dan gebeurtenissen ver weg. Ook culturele herkenbaarheid speelt een rol: hoe meer de lezer zich kan identificeren met de situatie, hoe zwaarder de emotionele impact.

### 2. Belangrijke Nuances
**Type gebeurtenis - categorische verschillen**

- **Kinderen als slachtoffer**: alles met kinderen als slachtoffer weegt zwaarder
- **Geweld tegen groepen**: Aanslagen en aanvallen op groepen (bijv. scholen, kerken) wegen zwaarder dan individuele misdrijven
- **Menselijk misbruik**: misbruik, verwaarlozing, en mensenhandel wegen zwaarder dan onopzettelijk leed
- **Rampen en massa ongelukken**: natuurrampen en grote ongelukken met veel slachtoffers wegen zwaarder dan individuele incidenten
- **Gericht persoonlijk leed**: moord, ontvoering, en huiselijk geweld wegen zwaarder dan ongevallen
- **Systemisch falen**: institutioneel falen met menselijke tol (bijv. zorgschandalen) weegt zwaarder dan incidentele fouten
- **'Allerdaagse' ongelukken**: verkeersongelukken en huisbranden wegen minder zwaar tenzij er bijzondere omstandigheden zijn
- **Natuurrampen** : Natuurrampen zonder menselijke schuld of leed
- **Politiek geweld en conflicten**: Politieke conflicten en diplomatieke spanningen zonder directe menselijke tol
- **Indirecte economische/sociale problemen**: Economische recessies, werkloosheidscijfers, en sociale kwesties zonder directe menselijke impact

**Schaal van impact**
Het aantal betrokkenen of slachtoffers heeft een niet-lineair effect op de emotionele zwaarte. Een enkele dode kan al zwaar wegen, maar bij grotere aantallen neemt de impact niet evenredig toe.

**Presentatie-paradox**
We meten emotionele impact, niet alleen objectieve ernst. Daarom kan een zeer ernstige gebeurtenis die zakelijk wordt beschreven even zwaar scoren als een minder ernstige gebeurtenis die emotioneel wordt gepresenteerd.

**Tijdsdimensie**
Acute crises en "breaking news" wegen zwaarder dan langdurige of chronische problemen. De urgentie en actualiteit van het nieuws beïnvloeden de emotionele impact.

**Desinteresse en irrelevantie**
Gebeurtenissen die niet resoneren met Nederlandse lezers zullen meer neutraal scoren, ongeacht het sentiment. Extreem negatief nieuws valt snel niet in dit effect en weegt dan nog steeds zwaar, voornamelijk bij veel details en emotionele presentatie.

### 3. Schaal Punten-definities
#### Score 0 - Positief/Opbeurend
**Algemene omschrijving:**
Nieuws dat expliciet positieve emoties oproept: vreugde, trots, inspiratie of hoop. Gebeurtenissen die het menselijk potentieel tonen of succesverhalen vertellen zonder betekenisvolle keerzijde.

**Karakteristieken:**
Vocabulaire: "triomf", "prachtig", "historisch", "emotioneel moment"
Focus op menselijke veerkracht en positieve uitkomsten
Quotes van betrokkenen die blijdschap en dankbaarheid uitdrukken
Beschrijving van emotionele reacties (tranen van geluk, vreugdedans)
Hoge nabijheid: Nederlandse betrokkenen of herkenbare contexten

#### Score 1 - Neutraal
**Algemene omschrijving:**
Nieuws zonder significante emotionele lading. Feitelijke rapportage van gebeurtenissen die noch positieve noch negatieve emoties oproepen, of een balans tussen voor- en nadelen bevatten. De lezer kan zich niet sterk inleven of voelt geen directe betrokkenheid.

**Karakteristieken:**
Zakelijke, objectieve taal zonder emotionele woordkeuze
Focus op feiten, cijfers en procedures
Eventuele quotes zijn technisch of informatief van aard
Geen persoonlijke verhalen of menselijke gezichten
Nabijheid irrelevant of ver van Nederlandse ervaring

#### Score 2 - Licht negatief/Matig beladen
**Algemene omschrijving:**
Nieuws met beperkte negatieve lading dat enige bezorgdheid of lichte verontrusting oproept, maar geen diepgaande emotionele impact heeft. Problemen zijn ofwel klein van schaal, abstract van aard, of voldoende ver van de Nederlandse ervaring. De presentatie blijft overwegend zakelijk.

**Karakteristieken:**
Grotendeels zakelijke rapportage met occasionele emotionele woorden
Beperkt detailniveau, geen uitgebreide menselijke verhalen
Focus op feiten en gevolgen, niet op persoonlijk leed
Mogelijke zorgen geuit in quotes, maar niet dramatisch
Lage tot gemiddelde nabijheid

#### Score 3 - Matig zwaar
**Algemene omschrijving:**
Nieuws dat duidelijke emotionele impact heeft door concrete menselijke schade, leed of onrecht. De gebeurtenissen zijn verontrustend en roepen empathie op, maar zijn niet extreem traumatisch. Er is sprake van identificeerbare slachtoffers en herkenbare situaties, of van gebeurtenissen met substantiële maatschappelijke bezorgdheid.

**Karakteristieken:**
Emotionele woordkeuze begint dominant te worden
Persoonlijke verhalen en quotes van betrokkenen/nabestaanden
Beschrijving van emotionele impact op slachtoffers en omstanders
Details die inleving mogelijk maken zonder extreem grafisch te zijn
Gemiddelde tot hoge nabijheid (in Nederland of met Nederlandse betrokkenheid)

#### Score 4 - Zwaar
**Algemene omschrijving:**
Nieuws dat aanzienlijke emotionele impact heeft door ernstige menselijke tragedies, misdrijven met bijzonder schokkende elementen, of gebeurtenissen die fundamentele waarden schenden. De presentatie is vaak gedetailleerd en emotioneel, waardoor sterke inleving ontstaat. Het gaat om gebeurtenissen die lezers dagen kunnen bijblijven.

**Karakteristieken:**
Sterk emotionele woordkeuze doorheen het artikel
Uitgebreide persoonlijke verhalen, achtergronden van slachtoffers
Quotes die wanhoop, verdriet of ongeloof uitdrukken
Beschrijving van impact op gemeenschappen en families
Details die sterke visuele voorstelling mogelijk maken
Hoge nabijheid of zeer emotionele presentatie compenseert voor afstand

#### Score 5 - Extreem zwaar
**Algemene omschrijving:**
Nieuws dat de grenzen van het bevattelijke overschrijdt door extreme wreedheid, grote aantallen slachtoffers, of gebeurtenissen die fundamentele menselijke waardigheid en veiligheid op catastrofale wijze schenden. Deze gebeurtenissen zijn diep traumatisch, ook voor lezers die alleen erover lezen. De emotionele impact is overweldigend en langdurig.

**Karakteristieken:**
Extreme emotionele lading in woordkeuze
Zeer gedetailleerde beschrijvingen die sterke mentale beelden creëren
Focus op menselijk lijden en wanhoop
Quotes die onvoorstelbaar verdriet en trauma uitdrukken
Beschrijving van blijvende impact op gemeenschappen en nabestaanden
Hoge nabijheid óf zodanig extreme gebeurtenis dat afstand irrelevant wordt
Artikelen die expliciet waarschuwen voor schokkende inhoud