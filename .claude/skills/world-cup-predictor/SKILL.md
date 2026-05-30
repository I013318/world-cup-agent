---
name: world-cup-predictor
description: >-
  Predicts the outcome of a World Cup 2026 match between any two national teams. Combines a Poisson goal model (fitted on historical international results) with real-time qualitative context — injuries, suspensions, form, and breaking news — to produce adjusted win/draw/loss probabilities. Compares those probabilities against live bookmaker odds to identify positive expected value (+EV) bets and calculates the optimal Kelly Criterion stake size.
version: 1.0.0
tags: [soccer, football, sports]
allowed-tools: web_search
---

# World Cup Match Predictor

When invoked, follow this exact sequence to generate a prediction for the requested match:

1. **Run Mathematical Baseline:** Run `uv run python scripts/predict.py "<home_team>" "<away_team>"` from the directory `C:/Users/I013318/world-cup-agent/.claude/skills/world-cup-predictor`. This will use the skill's own `.venv` and return the Poisson probability matrix.
2. **Gather Qualitative Context:** Search the web for breaking news, injury updates, or managerial changes regarding the two teams within the last 48 hours.
3. **Fetch Live Odds:** Retrieve the current betting odds for the match using your available web or API tools.
4. **Calculate Expected Value & Bet Size:** 
   - Adjust the mathematical baseline probability using your qualitative context.
   - Compare the final probability against the implied probability of the bookmaker odds to find the Expected Value (EV).
   - Calculate the optimal fractional bet size using the Kelly Criterion.
5. **Output Report:** Present a final markdown summary of the match, the mathematical baseline, qualitative adjustments, EV, and the recommended Kelly stake.
