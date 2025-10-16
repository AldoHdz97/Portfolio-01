# Campus Social Media Insights Generator

Automated agentic system that analyzes social media performance data from 20+ university campuses and generates structured insights in Spanish using CrewAI and Claude Sonnet 4.5.

---

## What This Does

Takes raw social media data (metrics, publications, brand health scores) → Preprocesses everything into clean JSON → Runs through a CrewAI agent → Outputs structured insights + formatted Markdown report.

**Input:** 3 messy data files  
**Output:** 20 clean insights (one per campus) in JSON + beautiful Markdown report

---

## Tech Stack

- **Python 3.10+**
- **CrewAI** - Agentic orchestration
- **Claude Sonnet 4.5** - Insight generation (via Anthropic API)
- **Pydantic** - Schema validation
- **JSON/CSV processing** - Data preprocessing

---

## Project Structure

```
.
├── preprocess_metrics.py          # Preprocesses metrics with % changes
├── preprocess_publications.py      # Filters top 8 posts per campus
├── preprocess_sdm.py              # Processes brand health scores
├── merge_all.py                   # Unifies all data into one JSON
├── generate_insights.py           # Main agent script
├── schemas.py                     # Pydantic schemas
├── .env                           # API keys
└── README.md
```

---

## Setup

### 1. Install Dependencies

```bash
pip install crewai python-dotenv anthropic
```

### 2. Configure API Key

Create `.env` file:

```
ANTHROPIC_API_KEY=your_key_here
```

### 3. Prepare Input Files

Place these in the project root:
- `Mes_Actual_2_SDMxRegion.json`
- `Mes_del_A_o_anterior_3_SDMxRegion.json`
- `Todas_las_publicaciones_con_sus_metricas_1_SDMxRegion.json`
- `Regiones Unificadas - Valores.csv`

---

## Usage

### Step 1: Preprocess Data

Run these in order (or all at once):

```bash
python preprocess_metrics.py
python preprocess_sdm.py
python preprocess_publications.py
python merge_all.py
```

**Outputs:**
- `metrics_estructurado.json` - Metrics with percentage changes
- `sdm_estructurado.json` - Brand health scores with categories
- `publicaciones_estructurado.json` - Top 8 posts per campus
- `unified_campus_data.json` - **Final unified data**

### Step 2: Generate Insights

```bash
python generate_insights.py
```

**Takes ~6-9 minutes** (20 API calls to Claude)

**Outputs:**
- `campus_insights.json` - Raw insights data
- `campus_insights_report.md` - Formatted report

---

## How It Works

### Preprocessing Pipeline

1. **Metrics**: Merges current + previous year data, calculates percentage changes (`+86.53%`, `-12.45%`)
2. **Publications**: Filters top 4 Instagram + top 4 Facebook posts by engagement score
3. **SDM Scores**: Categorizes brand health (deficiente → excepcional)
4. **Merge**: Combines everything by `campus_id`

### Agent System

**Single Agent:** Analista de Performance Digital
- **Model:** Claude Sonnet 4.5
- **Task:** Generate 95-100 word insight per campus in Spanish
- **Input:** Unified campus data (metrics + publications + scores)
- **Output:** Structured insight following specific format

**Markdown Formatting:** Pure Python (no agent needed for mechanical formatting)

---

## Insight Format

Each insight is 95-100 words and includes:

1. **Opening:** Performance category (satisfactorio, sobresaliente, etc.)
2. **Metrics:** Exact percentage changes in publications, interactions, reach
3. **Content Analysis:** 2-3 main themes from top posts
4. **Closing:** Comment count for the period

**Example:**

> En septiembre 2025, el Campus Monterrey mostró un desempeño satisfactorio, incrementando 86% su volumen de publicaciones, 152% las interacciones y 82% el alcance respecto al año anterior. Destacaron contenidos que combinaron nostalgia institucional y vida estudiantil auténtica: recorridos históricos del campus desde 1943, celebraciones patrias que reforzaron el orgullo mexicano, y momentos cotidianos como coffee breaks y el vibrante apoyo a Borregos. Estas narrativas generaron una conexión emocional que fortaleció el sentido de pertenencia y comunidad. Se registraron 556 comentarios durante el periodo.

---

## Configuration

### Campus Mapping

20 campuses supported (MTY, GDL, PUE, CDJ, TOL, CCM, CEM, QRO, CHI, SIN, AGS, COB, LEO, LAG, SON, HGO, SLP, CVA, CSF, SAL)

Defined in `schemas.py` - modify if adding/removing campuses.

### Analysis Month

Currently set to **Septiembre 2025**

Change in `generate_insights.py`:
```python
**MES DE ANÁLISIS:** Septiembre 2025  # Change here
```

### Word Count

Insights are constrained to **95-100 words**

Modify in task description if needed (not recommended - tested extensively at this length).

---

## Token Usage & Cost

**Per campus:**
- Input: ~4,800 tokens
- Output: ~400 tokens
- Total: ~5,200 tokens

**For 20 campuses:**
- Total: ~104,000 tokens
- Cost: ~$0.50 (Claude Sonnet 4.5 pricing)

**Runtime:** ~6-9 minutes for full run

---

## Troubleshooting

### Import Errors

Delete Python cache:
```bash
rmdir /s /q __pycache__  # Windows
rm -rf __pycache__        # Mac/Linux
```

### Agent Not Following Format

Check that:
1. Task description is complete
2. Using Claude Sonnet 4.5 (not Haiku)
3. `max_iter=3` is set

### Missing Data

Verify all 4 input files exist and `unified_campus_data.json` was created successfully.

---

## Design Decisions

**Why no validation agent?**  
Data is pre-validated through Pydantic schemas. Percentages are pre-calculated. Manual spot-check is faster and more reliable for 20 campuses.

**Why Python for Markdown instead of an agent?**  
Mechanical formatting doesn't need AI. Python is faster, free, and 100% reliable.

**Why Claude Sonnet 4.5?**  
Good at following complex instructions with word count constraints.

**Why are there different models on the code?**
Claude has its limitations and before trying to process everything in batches, going for a big output was the original idea. So i tried using ChatGpt,
Model 5 and the cheaper version, it was okay, but still not enough output tokens to manage all of them so I changed the strategy and when back to Claude,
which is my personal favorite.

**Why process campuses sequentially?**  
Better error handling, progress tracking, and quality control. Batching would save minimal cost for 20 campuses.

---

## Output Examples

See `campus_insights_report.md` for full formatted output.

**JSON structure:**
```json
{
  "insights": [
    {
      "campus_id": "MTY",
      "campus_name": "Monterrey",
      "insight": "En septiembre 2025..."
    }
  ],
  "metadata": {
    "month": "Septiembre 2025",
    "total_campuses": 20,
    "generated_at": "2025-10-15"
  }
}
```

---

## Future Improvements

- Batch processing for 100+ campuses (Instead of batches of 1 could be batches of 2 or 5)
- Multi-month comparison (Maybe?)
- Dashboard integration (Sounds tedious)

---

## Notes

- All insights in Spanish
- No unnecessary metrics (only what's needed for decisions)
- Clean, scannable output
- Designed for university social media teams

---

**Questions?** Check the code comments or adjust prompts in `generate_insights.py`.