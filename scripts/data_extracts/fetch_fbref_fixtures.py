import pandas as pd

def get_league_fixtures_and_results(fbref_url):
    df = pd.read_html(fbref_url)[0]
    df = df.dropna(subset=['Wk'])
    df['Wk'] = df['Wk'].astype(int)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Time'] = pd.to_datetime(df['Time'],format= '%H:%M' ).dt.time
    df['Attendance'] = df['Attendance'].astype('Int64')
    df[['home_score','away_score']] = df['Score'].astype('string').str.split('–',expand=True).astype('Int64')
    df = df.rename(columns={
        'Wk': 'gameweek', 
        'Day': 'weekday',
        'Date':'match_date',
        'Time':'start_time',
        'Home':'home_team',
        'xG':'home_xg',
        'xG.1':'away_xg',
        'Away':'away_team',
        'Attendance':'attendance',
        'Venue':'venue',
        'Referee':'referee'
        })

    df_fixtures = df.loc[df['Score'].isnull()][['gameweek','weekday','match_date','start_time','home_team','away_team']]
    df_results = df.loc[~df['Score'].isnull()][['gameweek','weekday','match_date','start_time','home_team','home_xg','home_score','away_team','away_xg','away_score','attendance','venue','referee']]
    return df_fixtures,df_results

def get_league_id_and_name(league_name):
    league_id = {'Premier League':'9','Championship':'10'}
    league_url_name = {'Premier League':'Premier-League','Championship':'Championship'}
    league_folder_name = {'Premier League':'premier_league','Championship':'championship'}
    return league_id[league_name],league_url_name[league_name],league_folder_name[league_name]

def store_to_csv(df,folder_name,file_name):
    df.to_csv(r'data/raw/league/'+folder_name+r'/'+file_name+r'.csv',index=False)
    return


def fetch_fbref_fixtures():
    base_url = r'https://fbref.com/en/comps/'
    league_list = ['Premier League','Championship']
    for league in league_list:
        id,name,folder = get_league_id_and_name(league)
        league_url = base_url+id+r'/schedule/'+name+r'-Scores-and-Fixtures'
        fixtures,results = get_league_fixtures_and_results(league_url)
        store_to_csv(fixtures,folder,'fixtures')
        store_to_csv(results,folder,'results')
    return



if __name__ == '__main__':
    fetch_fbref_fixtures()