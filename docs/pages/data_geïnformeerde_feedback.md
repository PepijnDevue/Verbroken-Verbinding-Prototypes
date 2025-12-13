# Data Geïnformeerde Feedback - Documentatie

## AI Pipeline: Technische Reproduceerbaarheid

<!-- TODO Nalopen en verder schrijven -->

### Overzicht

De data-geïnformeerde feedback pipeline is een two-stage AI-systeem dat gebruikersreacties onder nieuwsartikelen analyseert en transformeert naar gestructureerde, bruikbare feedback voor de redactie. Het systeem gebruikt een groot taalmodel (LLM) om enerzijds individuele commentthreads te filteren op redactie-relevantie, en anderzijds om gefilterde feedback te aggregeren tot een coherent rapport.

### Architectuur

De pipeline bestaat uit vier hoofdcomponenten:

#### 1. Model Management (`huggingface_utils.py`)

Het systeem gebruikt de Hugging Face Transformers bibliotheek voor model loading en inferentie:

**Modelkeuze:**
- **Default model:** `CohereLabs/aya-expanse-8b`
- **Rationale:** Meertalig model (incl. Nederlands) met voldoende capaciteit voor complexe instructievolging
- **Device mapping:** Automatische GPU-detectie via `device_map="auto"` voor optimale performance

**Implementatiedetails:**
```python
pipeline(
    "text-generation",
    model=model_name,
    device_map=device_map,
    token=_get_token(),
)
```

**Key design decisions:**
- Gebruik van `@st.cache_resource` voor model caching: voorkomt herhaalde model loads binnen dezelfde sessie
- Token-based authenticatie voor toegang tot private/gated models
- Expliciete GPU memory management via `torch.cuda.empty_cache()` bij model unloading
- Model validatie via `huggingface_hub.model_info()` voordat loading plaatsvindt

#### 2. Stage 1: Thread-level Feedback Extractie

**Doel:** Bepaal per commentthread of er expliciete feedback aan de redactie in staat.

**Prompt strategie (`NOTE_PROMPT`):**
De prompt is ontworpen met strikte filtering criteria:
- **Expliciete verwijzing vereist:** Alleen reacties die duidelijk het artikel of redactionele keuzes adresseren
- **Geen interpretatie:** Het systeem mag geen intenties raden of afleidingen maken
- **Contextuele grounding:** Volledige artikeltekst wordt meegestuurd voor begrip

**Prompt:**
```plaintext
DOEL
Je analyseert één thread onder een nieuwsartikel (één hoofdcomment + alle replies). Je taak is uitsluitend te bepalen of er expliciete feedback aan de redactie over het artikel in staat.

HARDERE REGELS
- Alleen feedback opnemen die duidelijk gericht is op het artikel of de redactie.
- Reacties die een probleem beschrijven zonder het artikel te benoemen zijn geen feedback.
- Alleen als een gebruiker expliciet verwijst naar het artikel of iets dat de redactie heeft gedaan/nagelaten (titel, feit, bron, uitleg, fout, gemis) mag het meetellen.
- Geen interpretaties, geen afleidingen, geen pogingen intenties te raden.
- Als er geen expliciete verwijzing is naar het artikel of redactionele keuzes -> resultaat = "".

WERKWIJZE
1. Lees het artikel.
2. Lees de volledige thread.
3. Beantwoord alleen deze vraag:
Is er een reactie die expliciet de redactie aanspreekt?
4. Zo ja: vat dat kort en feitelijk samen.
5. Zo nee: geef een lege string.

OUTPUT (strikte JSON)
{
    "beredeneer": "Korte uitleg waarom er wel/geen expliciete verwijzing naar het artikel of redactie is.",
    "resultaat": "Samenvatting van de expliciete feedback, of ""."
}

ARTICLE
<article>{{PLAATS_HIER_HET_ARTIKEL}}</article>

INPUT
Hieronder staat één thread:
<thread>{{PLAATS_HIER_DE_THREAD}}</thread>

OUTPUT 
```

**Processing flow:**
```python
for comment in comments:
    result = process_comment_thread(comment, article_text)
    all_results.append(result)
```

- **Sequential processing:** Threads worden één voor één verwerkt (geen parallel processing vanwege model constraints)
- **Progress tracking:** Real-time voortgangsindicatie via Streamlit progress bar
- **Error handling:** Retry mechanism (max 5 pogingen) bij JSON parsing fouten

#### 3. Stage 2: Feedback Aggregatie

**Doel:** Combineer alle valide feedbackpunten tot één professioneel redactierapport.

**Prompt strategie (`AGGREGATION_PROMPT`):**
- **Clustering:** Groepeer gelijkaardige feedback (titel, feiten, bronnen, toon)
- **Deduplicatie:** Vermijd herhaling van dezelfde punten
- **Neutralisatie:** Transformeer potentieel agressieve toon naar constructieve feedback
- **Professionalisering:** Verwijder namen, quotes en irrelevante details

**Prompt:**
```plaintext
DOEL
Je ontvangt een lijst met JSON-objecten die per thread samengevatte feedback bevatten.
Je taak is om alle aanwezige feedbackpunten te combineren tot één samenhangend, constructief en professioneel redactierapport.

INHOUDSRICHTLIJNEN
- Lees de artikeltekst als context voor interpretatie.
- Gebruik alle feedback die niet leeg is.
- Cluster gelijkaardige punten (bijv. titelproblemen, feitencontrole, ontbrekende context, bronnen, toon).
- Vermijd herhaling en bundel dubbele signalen.
- Formuleer neutraal, professioneel en agressieloos.
- Geen namen, geen quotes, geen verzonnen punten.

WERKWIJZE
1. Lees eerst de artikeltekst.
2. Lees alle JSON-items.
3. Extraheer alle niet-lege 'resultaat'-velden.
4. Groepeer en synthetiseer alle feedback in logische categorieën.
5. Formuleer een geordende, constructieve eindrapportage.
6. Denk eerst stap voor stap in een 'beredeneer'-sectie.
7. Geef daarna alleen de JSON-output.

OUTPUT
Geef uitsluitend dit JSON-schema:
{
    "beredeneer": "Korte, stap-voor-stap beschrijving hoe je de lijst hebt geanalyseerd en geherstructureerd. En welke onderwerpen je bent tegengekomen.",
    "samenvatting": "Geclusterde en geordende feedback in neutrale, professionele toon."
}

ARTICLE
<article>{{PLAATS_HIER_HET_ARTIKEL}}</article>

INPUT
Hieronder staat de lijst met JSON-resultaten:
<results>{{PLAATS_HIER_DE_RESULTATEN}}</results>

OUTPUT
```

**Processing:**
```python
aggregated = aggregate_feedback(extracted_feedbacks, article_text)
```

**Design rationale:**
- Filter alleen niet-lege resultaten voor aggregatie (efficiency)
- Hogere retry limit (10 vs 5) voor aggregatie vanwege complexere output
- Artikelcontext opnieuw meegestuurd voor accurate interpretatie

#### 4. Error Handling & Robustness

**JSON Extraction:**
De `extract_json_from_response()` functie implementeert een two-pass parsing strategie:
1. **Markdown code blocks:** Detectie via regex `r'```(?:json)?\s*(\{.*?\})\s*```'`
2. **Raw JSON:** Fallback naar `r'\{.*\}'` pattern matching

**Retry Mechanism:**
```python
def generate_with_retries(prompt: str, max_retries: int = 5) -> dict:
    iterations = 0
    while output.get("error") is not None and iterations < max_retries:
        response = hf_utils.generate(prompt)
        output = extract_json_from_response(response)
        iterations += 1
```

**Rationale:**
- LLMs kunnen inconsistent formatteren (markdown wrappers, extra whitespace)
- Retry zonder exponential backoff: fouten zijn deterministisch (formatting), niet rate-limit gerelateerd
- Max retries als fallback: voorkomt infinite loops bij persistente model problemen

### Data Persistence

**Output format (`dgf_outputs_chatgpt.json`):**
```json
{
    "individual_results": [...],  // Alle thread-level analyses
    "aggregated_feedback": {...}  // Finaal rapport
}
```

**Design decisions:**
- Single-file output: eenvoudige version control en reproducibility
- Volledige intermediate results bewaard: transparantie en debugging
- File existence check voorkomt onnodige herberekening (cost optimization)

### Reproduceerbaarheid Garanties

**Determinisme:**
- **Temperatuur niet gespecificeerd:** Default model sampling (mogelijk non-deterministic)
- **Prompt versioning:** Prompts zijn hardcoded in source code (traceable via git)
- **Model versioning:** Default model pinned (`aya-expanse-8b` zonder version tag - kan updates krijgen)

**Verbetersuggesties voor volledige reproduceerbaarheid:**
1. Specificeer temperature=0 voor deterministische output
2. Pin model versie met commit hash
3. Bewaar gebruikte model config in output JSON
4. Log model versie + timestamp per run

### Performance Overwegingen

**Bottlenecks:**
- **Sequential processing:** O(n) per thread, geen parallelisatie
- **Model inference:** ~1-5s per thread (afhankelijk van thread lengte en hardware)
- **Memory:** Volledig model in GPU/CPU memory (8B parameters ≈ 16GB bij FP16)

**Optimalisatie mogelijkheden:**
- Batch processing van threads (indien model max context length toelaat)
- Quantization (int8/int4) voor lagere memory footprint
- Async processing met queue systeem voor langere artikelen

### Kwaliteitsborging

**Prompt Engineering Principes:**
- **Chain-of-thought:** "beredeneer" veld forceert expliciet redeneren
- **Few-shot learning:** Impliciet via strikte output voorbeelden
- **Grounding:** Volledige context (artikel + thread) meegestuurd
- **Constraints:** Harde regels ("ALLEEN als expliciete verwijzing") reduceren false positives

**Validatie:**
- JSON schema enforcement via extraction logic
- Type checking van output structure
- Empty result handling (lege strings bij geen feedback)

### Technische Dependencies

**Core:**
- `transformers`: Model loading en inferentie
- `huggingface_hub`: Model validatie en toegangsbeheer
- `torch`: GPU acceleratie (optioneel)

**Integration:**
- `streamlit`: UI en state management
- `dotenv`: Configuratie management (HF token)

**Python versie:** Niet gespecificeerd (aanbevolen: ≥3.10 voor moderne type hints)