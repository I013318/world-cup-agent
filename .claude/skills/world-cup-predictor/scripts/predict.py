import sys
import pandas as pd
import penaltyblog as pb

# International results dataset (Mart Jürisoo, github.com/martj42/international_results)
DATA_URL = (
    "https://raw.githubusercontent.com/martj42/international_results/"
    "master/results.csv"
)

def predict_match(home_team, away_team):
    df = pd.read_csv(DATA_URL)

    # Keep only the last 8 years of competitive matches for relevance
    df["date"] = pd.to_datetime(df["date"])
    df = df[df["date"] >= "2018-01-01"]
    df = df[df["tournament"] != "Friendly"]
    df = df.dropna(subset=["home_score", "away_score"])
    df["home_score"] = df["home_score"].astype(int)
    df["away_score"] = df["away_score"].astype(int)

    model = pb.models.PoissonGoalsModel(
        goals_home=df["home_score"],
        goals_away=df["away_score"],
        teams_home=df["home_team"],
        teams_away=df["away_team"],
    )
    model.fit()

    probs = model.predict(home_team, away_team)

    print(f"--- Mathematical Baseline for {home_team} vs {away_team} ---")
    print(f"Home Win Probability: {probs.home_win:.4f}")
    print(f"Draw Probability:     {probs.draw:.4f}")
    print(f"Away Win Probability: {probs.away_win:.4f}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python predict.py 'Home Team' 'Away Team'")
    else:
        predict_match(sys.argv[1], sys.argv[2])
