import pandas as pd

url = "https://afltables.com/afl/seas/2025.html"


def main():
    tables = pd.read_html(url) # returns a list of tables, each element in list is one HTML, not one match or row
    print(f"Number of tables found: {len(tables)}")
    match_tables = []
    for df in tables:
        matches_in_df = is_match(df)
        if matches_in_df:
            match_tables.extend(matches_in_df)
    
    print(f"Total matches: {len(match_tables)}")
    if match_tables:
        print(match_tables[0])

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

if __name__ == "__main__":
    main()