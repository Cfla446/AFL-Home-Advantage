import pandas as pd
from scipy.stats import binomtest

def main():
    df = pd.read_csv("data/matches_2025.csv")
    df["home_win"] = df["winner"] == df["team1"] # creating column that stores boolean

    total_games = len(df)
    home_wins = df["home_win"].sum()

    calculate_total_home_win_rate(home_wins, total_games)
    calculate_p_value_significance(home_wins, total_games)
    calculate_team_home_win_rate(df)
    calculate_venue_home_win_rate(df)

def calculate_total_home_win_rate(home_wins, total_games):
    home_win_rate = home_wins / total_games

    print(f"Total games: {total_games}")
    print(f"Home wins: {home_wins}")
    print(f"Home win rate: {home_win_rate:.2f}")

def calculate_p_value_significance(home_wins, total_games):
    p_val = binomtest(home_wins, total_games, 0.5, alternative = "greater")
    print(f"P-value: {p_val.pvalue:.7f}")

def calculate_team_home_win_rate(df):
    team_win_rates = df.groupby("team1")["home_win"].mean().sort_values(ascending = False)
    print(team_win_rates)

def calculate_venue_home_win_rate(df):
    venue_win_rates = df.groupby("venue")["home_win"].mean().sort_values(ascending = False)
    print(venue_win_rates)

if __name__ == "__main__":
    main()