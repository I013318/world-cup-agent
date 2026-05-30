# World Cup Agent

A Claude Code-powered prediction agent for World Cup 2026 matches. Given any two national teams, it combines a statistical Poisson goal model with qualitative context (injuries, form, news) and live betting odds to produce match outcome probabilities, expected value calculations, and Kelly Criterion stake recommendations.

---

## How It Works

The agent follows a six-step pipeline every time a match is requested:

### 1. Fetch Live Data
The agent queries the **alldontlie-api MCP server** for the latest pre-match context: squad rosters, recent form, and match statistics for both teams.

### 2. Run the Mathematical Baseline (`scripts/predict.py`)
A **Poisson Goals Model** is fitted against historical international match results and used to generate a probability matrix for the requested fixture.

- **Data source:** [martj42/international_results](https://github.com/martj42/international_results) — a comprehensive public dataset of international football results.
- **Filter:** Only competitive matches (no friendlies) from 2018 onwards are used, keeping the model sensitive to current team strength while retaining enough data to fit reliably.
- **Model:** `penaltyblog.models.PoissonGoalsModel` — a Dixon-Coles adjusted Poisson model that estimates an attack and defence strength rating for every national team, then uses those ratings to derive the expected goals (λ) for each side in a given match. From λ, the full scoreline probability matrix is computed via the Poisson distribution, and home win / draw / away win probabilities are summed from that matrix.

Output:
```
--- Mathematical Baseline for Mexico vs South Africa ---
Home Win Probability: 0.5599
Draw Probability:     0.2837
Away Win Probability: 0.1565
```

### 3. Gather Qualitative Context
The agent searches the web for **breaking news within the last 48 hours** — injury updates, suspensions, managerial changes, or travel disruptions — for both teams. These findings are used to nudge the baseline probabilities up or down before any betting calculation.

### 4. Fetch Live Odds
Current bookmaker odds for the match are retrieved. These are converted to **implied probabilities** (accounting for the overround/vig) to establish the market's view of each outcome.

### 5. Calculate Expected Value & Kelly Stake
With a final adjusted probability in hand, the agent calculates:

**Expected Value (EV)**
```
EV = (p × b) - (1 - p)
```
Where `p` is the agent's probability for an outcome and `b` is the net decimal odds (decimal odds − 1). A positive EV means the bet is mathematically profitable over the long run.

**Kelly Criterion**
```
Kelly % = (b × p - q) / b
```
Where `q = 1 - p`. This gives the theoretically optimal fraction of bankroll to stake. The agent outputs both the full Kelly and a **half-Kelly** recommendation — half-Kelly is standard practice to reduce variance while retaining most of the edge.

### 6. Output Report
A final markdown report is presented covering:
- Match overview and predicted scoreline
- Mathematical baseline probabilities
- Qualitative adjustments and reasoning
- EV calculation
- Recommended Kelly stake (half-Kelly)

---

## Project Structure

```
world-cup-agent/
├── .claude/
│   └── skills/
│       └── world-cup-predictor/
│           ├── SKILL.md              # Claude Code skill definition
│           └── scripts/
│               └── predict.py        # Poisson model script
├── pyproject.toml                    # uv project config & dependencies
├── uv.lock                           # Pinned lockfile
└── README.md
```

---

## Setup

This project uses [uv](https://docs.astral.sh/uv/) for Python environment management.

**Install dependencies:**
```bash
uv sync
```

**Run the prediction script directly:**
```bash
uv run python .claude/skills/world-cup-predictor/scripts/predict.py "Mexico" "South Africa"
```

**Run the full agent pipeline** (requires Claude Code with the `world-cup-predictor` skill):
```
/world-cup-predictor
```
Then specify the two teams when prompted.

---

## Dependencies

| Package | Purpose |
|---|---|
| [penaltyblog](https://github.com/martineastwood/penaltyblog) | Poisson/Dixon-Coles goal models, probability grids |
| pandas | Data loading and filtering |
| scipy / numpy | Numerical computation underlying the model |

Python 3.13+ required.

---

## Limitations & Disclaimer

- The Poisson model treats all competitive internationals equally — it does not distinguish between World Cup qualifiers, Nations League, and tournament group games.
- Live odds and web search are dependent on available MCP tools and may not be accessible in all environments; the agent will fall back to manual calculations when they are unavailable.
- **This tool is for educational and entertainment purposes only. Gambling involves financial risk. Never stake more than you can afford to lose.**
