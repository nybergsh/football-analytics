# Module dependencies
import pandas as pd
from pathlib import Path
import time
from tqdm import tqdm

# Path
p = str(Path(__file__).parent.parent.parent.absolute())
fbref_match_result_csv_path = p + r'/data/raw/fbref_match_results.csv'
fbref_fixtures_csv_path = p + r'/data/raw/fbref_fixtures.csv'


#https://fbref.com/en/comps/9/2022-2023/schedule/2022-2023-Premier-League-Scores-and-Fixtures

# Leagues
league_list = ['Premier-League','Championship','La-Liga','Serie-A','Bundesliga','Eredivisie','Primeira-Liga','Ligue-2','2-Bundesliga','Serie-B']
league_code_dict = {
    'Premier-League':9,
    'Championship':10,
    'Serie-A':11,
    'La-Liga':12,
    'Bundesliga':20,
    'Eredivisie':23,
    'Primeira-Liga':30,
    '2-Bundesliga':33,
    'Ligue-2':60,
    'Serie-B':18
}

# Seasons
season_list = ['2017-2018','2018-2019','2019-2020','2020-2021','2021-2022','2022-2023','2023-2024']
#season_list = ['2023-2024']

# Output df
fbref_fixtures_and_match_results_df = pd.DataFrame()

# Loop through leagues and seasons
for league in tqdm(league_list):
    for season in tqdm(season_list,leave=False):
        league_code = league_code_dict[league]
        #tmp_df = pd.read_html(r'https://fbref.com/en/comps/9/2023-2024/schedule/2023-2024-Premier-League-Scores-and-Fixtures')
        tmp_df = pd.read_html(r'https://fbref.com/en/comps/{}/{}/schedule/{}-{}-Scores-and-Fixtures'.format(league_code,season,season,league))[0]
        tmp_df[['season','league','league_id']] = season,league.replace('-',' '),league_code
        tmp_df = tmp_df.dropna(subset = ['Wk'])
        #tmp_df = tmp_df.loc[tmp_df['xG'].notnull()]
        fbref_fixtures_and_match_results_df = pd.concat([fbref_fixtures_and_match_results_df,tmp_df],ignore_index=True)
        time.sleep(2)


# Formatting
fbref_fixtures_and_match_results_df[['home_score','away_score']] = fbref_fixtures_and_match_results_df['Score'].astype('string').str.split('–',expand=True).astype('Int64')
fbref_fixtures_and_match_results_df['Wk'] = fbref_fixtures_and_match_results_df['Wk'].astype('Int64')
fbref_fixtures_and_match_results_df['Date'] = pd.to_datetime(fbref_fixtures_and_match_results_df['Date'])
fbref_fixtures_and_match_results_df['Time'] = pd.to_datetime(fbref_fixtures_and_match_results_df['Time'],format= '%H:%M' ).dt.time
fbref_fixtures_and_match_results_df['Attendance'] = fbref_fixtures_and_match_results_df['Attendance'].astype('Int64')
fbref_fixtures_and_match_results_df = fbref_fixtures_and_match_results_df.rename(columns={
    'Wk':'gameweek',
    'xG.1':'away_xg',
    'Day':'weekday',
    'Date':'match_date',
    'Time':'kickoff_time',
    'Home':'home_team',
    'xG':'home_xg',
    'Away':'away_team',
    'Attendance':'attendance',
    'Venue':'venue',
    'Referee':'referee',
    'Match Report':'match_report',
    'Notes':'notes'
})

fbref_fixtures_df = fbref_fixtures_and_match_results_df.loc[fbref_fixtures_and_match_results_df['Score'].isnull()].copy().drop(columns=['away_xg', 'home_xg','attendance','referee','match_report','notes','Score','home_score','away_score'])
fbref_results_df = fbref_fixtures_and_match_results_df.loc[fbref_fixtures_and_match_results_df['home_xg'].notnull()].copy().drop(columns=['Score'])
fbref_results_df = fbref_results_df[['season','league','league_id','gameweek','match_date','home_team','home_xg','home_score','away_team','away_xg','away_score']]

fbref_fixtures_df.to_csv(fbref_fixtures_csv_path,index=False)
fbref_results_df.to_csv(fbref_match_result_csv_path,index=False)
