from load_data import main as load_data_main
from analysis import main as analysis_main


def main():
    df_all = load_data_main(1897, 2025)
    print(f"Total matches across all selected seasons: {len(df_all)}")
    analysis_main(df_all)


if __name__ == "__main__":
    main()