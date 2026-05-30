---
name: world-cup-predictor
description: Predicts World Cup match outcomes using Poisson models, real-time news, and calculates Kelly Criterion bet sizing.
disable-model-invocation: true
---

# World Cup Match Predictor

When invoked, follow this exact sequence to generate a prediction for the requested match:

1. **Fetch Live Data:** Use the alldontlie-api MCP server to fetch the latest match stats, rosters, and pre-match form for the requested teams.
2. **Run Mathematical Baseline:** Execute the Python script at scripts/predict.py passing the home and away team names as arguments. This will return the Poisson probability matrix.
3. **Gather Qualitative Context:** Search the web for breaking news, injury updates, or managerial changes regarding the two teams within the last 48 hours.
4. **Fetch Live Odds:** Retrieve the current betting odds for the match using your available web or API tools.
5. **Calculate Expected Value & Bet Size:** 
   - Adjust the mathematical baseline probability using your qualitative context.
   - Compare the final probability against the implied probability of the bookmaker odds to find the Expected Value (EV).
   - Calculate the optimal fractional bet size using the Kelly Criterion.
6. **Output Report:** Present a final markdown summary of the match, the mathematical baseline, qualitative adjustments, EV, and the recommended Kelly stake.
