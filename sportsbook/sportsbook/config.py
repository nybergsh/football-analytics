from pathlib import Path

main_directory = Path(__file__).parent.parent.parent
fbref_results_csv_path = Path(str(main_directory) + r'\data\raw\fbref_match_results.csv')
