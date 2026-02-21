import pandas as pd
import os

# Ensuring path is set relative/absolute
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def operate_on_season(year):
    url = f"https://afltables.com/afl/seas/{year}.html"
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
        df_matches = pd.DataFrame(match_tables) # 
        os.makedirs("DATA_DIR", exist_ok=True) # 
        df_matches.to_csv(os.path.join(DATA_DIR, f"matches_{year}.csv"), index = False) # 
        print(f"{year}: {len(df_matches)} matches cleaned  and stored.") # 
        return df_matches # 
        # print(match_tables[0])

    # total_matches = pd.DataFrame(match_tables)
    # total_matches.to_csv("data/matches_2025.csv", index = False) # index false means row labels/no.s will not be included as an exxtra initial column
    # print("Successfully cleaned and stored 2025 season match data")
    return pd.DataFrame() # 

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
        'venue': venue,
    }

def main(start_year, end_year):
    all_seasons = [] # each entry will be a seasons dataframe
    for year in range(start_year, end_year + 1):
        df_season = operate_on_season(year) # scraper and save to csv, returns dataframe for that year
        if not df_season.empty:
            all_seasons.append(df_season) # append season to list
    if all_seasons: # if contains at least one dataframe
        return pd.concat(all_seasons, ignore_index=True) # stacks DF vertically, ignoring index means row indicies from each DF are preserved (doesnt just append to the list)
    return pd.DataFrame() # only executes in the case that no data

if __name__ == "__main__":
    main(1897, 2025)