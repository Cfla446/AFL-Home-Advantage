import pandas as pd

url = "https://afltables.com/afl/seas/2025.html"


def main():
    tables = pd.read_html(url) # returns a list of tables, each element in list is one HTML, not one match or row
    print(f"Number of tables found: {len(tables)}")
    match_tables = []
    for df in tables:
        matches = is_match(df)

        for match in matches:
            match_info = parse_match_info(match)
            match_tables.append(match_info)
    
    print(f"Total matches: {len(match_tables)}")
    if match_tables:
        print(match_tables[0])

    total_matches = pd.DataFrame(match_tables)
    total_matches.to_csv("data/matches_2025.csv", index = False) # index false means row labels/no.s will not be included as an exxtra initial column
    print("Successfully cleaned and stored 2025 season match data")

def is_match(df):
    match_list = []

    if df.shape[1] != 4:
        return match_list
    for start in range(0, len(df), 2):
        chunk = df.iloc[start: start + 2]
        if len(chunk) != 2:
            continue
        
        result_text = str(chunk.iloc[1, 3])
        if "won by" in result_text:
            match_list.append(chunk)

    return match_list

def parse_match_info(df):
    # While we could parse the string in the formatting of the data with 'X won by Y points'
    # It is more structured to to view the two empirical values to determine the winner and loser
    # data integrity, validating rather than trusting

    team1 = df.iloc[0]
    team2 = df.iloc[1]

    team1_name = team1[0]
    team2_name = team2[0]

    team1_score = int(team1[2])
    team2_score = int(team2[2])

    string = df.iloc[0, 3]
    venue = string.split("Venue:")[-1].strip()

    if team1_score > team2_score:
        winner = team1_name
        margin = team1_score - team2_score
    elif team2_score > team1_score:
        winner = team2_name
        margin = team2_score - team1_score
    else:
        winner = None
        margin = 0
    
    return {
        'team1': team1_name,
        'team2': team2_name,
        'score1': team1_score,
        'score2': team2_score,
        'winner': winner,
        'win_margin': margin,
        'venue': venue
    }

if __name__ == "__main__":
    main()