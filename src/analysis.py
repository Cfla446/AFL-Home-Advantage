import pandas as pd

def main():
    calculate_total_home_win_rate()

def calculate_total_home_win_rate():
    df = pd.read_csv("../data/matches_2025.csv")
    df["home_win"] = df["winner"] == df["team1"] # creating column that stores boolean

    total_games = len(df)
    home_wins = df["home_win"].sum()

    home_win_rate = home_wins / total_games

    print(f"Total games: {total_games}")
    print(f"Home wins: {home_wins}")
    print(f"Home win rate: {home_win_rate:.2f}")

if __name__ == "__main__":
    main()