# Veertjes - Documentatie

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