import pandas as pd

# Function that takes a match df and pivots it to a table where each team has a single row, and home/away is renamed to team/opponent
def pivot_result_df(match_df):
    match_df = match_df.reset_index().rename(columns={'index':'match_id'})
    pivoted_df_home_team = match_df.copy().rename(columns={
        'home_team':'team',
        'away_team':'opponent',
        'home_xg':'expected_goals_scored',
        'home_score':'goals_scored',
        'away_xg':'expected_goals_conceded',
        'away_score':'goals_conceded'
    })
    pivoted_df_home_team['home_away'] = 'home'
    pivoted_df_away_team = match_df.copy().rename(columns={
        'home_team':'opponent',
        'away_team':'team',
        'home_xg':'expected_goals_conceded',
        'home_score':'goals_conceded',
        'away_xg':'expected_goals_scored',
        'away_score':'goals_scored'
    })
    pivoted_df_away_team['home_away'] = 'away'
    pivoted_df = pd.concat([pivoted_df_home_team,pivoted_df_away_team],ignore_index=True).sort_values(by='match_date').reset_index(drop=True)
    pivoted_df['match_no'] = pivoted_df.groupby(['season','team']).cumcount()+1
    return pivoted_df

# Function that aggregates cumulative average per season and team/opponent and returns as a pd series
def get_cumulative_season_average(df,index_field,aggr_field):
    # Setting the correct index for the aggregation
    df = df.reset_index().set_index(['season',index_field,'index'])

    # Setting field value by,
    #   1. Setting cumulative average
    #   2. Shifting one step (so the average show value before game start)
    df['return_field'] = df.reset_index().groupby(['season',index_field]).expanding()[aggr_field].mean().groupby(['season',index_field]).shift().reset_index().set_index(['season',index_field,'level_2'])
    #print(df)
    return df['return_field'].values.tolist()

# Function that aggregates cumulative average over a rolling N matches and returns as a pd series
def get_rolling_match_average(df,index_field,aggr_field,N):
    # Setting correct index for aggregation
    df = df.reset_index().set_index(['season',index_field,'index'])

    # Setting field value by,
    #   1. Setting rolling N average
    #   2. Shifting one step (so the average show value before game start)
    df['return_field'] = df.reset_index().groupby(['season',index_field]).rolling(N)[aggr_field].mean().groupby(['season',index_field]).shift().reset_index().set_index(['season',index_field,'level_2'])

    return df['return_field'].values.tolist()