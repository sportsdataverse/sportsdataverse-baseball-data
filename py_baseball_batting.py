from pybaseball import batting_stats
import pandas as pd
from sportsdataverse import mlb
from tqdm import tqdm


def get_season_batting(first_season:int,last_season=0):
    if last_season < first_season:
        last_season = first_season
    
    for i in tqdm(range(first_season,last_season+1)):
        print(f'Getting stats for the {i} MLB season.')
        data = batting_stats(i,qual=0)
        data.to_csv(f"batting/season_box/{i}_batting_season_box.csv",index=False)

def get_player_game_batting_stats(first_season:int,last_season=0):
    if last_season < first_season:
        last_season = first_season

    for i in tqdm(range(first_season,last_season+1)):
        season_df = pd.DataFrame()
        month_df = pd.DataFrame()
        month_one_df = pd.DataFrame()
        month_two_df = pd.DataFrame()
        print(i)
        
        for j in range(3,12):
            month_df = pd.DataFrame()

            if j < 10:
                month = f"0{j}"
            else:
                month = f"{j}"
            
            try:
                month_one_df = pd.read_csv(f'gamelogs/{i}_{month}_01_statcast.csv')
            except:
                month_one_df = pd.DataFrame()
            try:
                month_two_df = pd.read_csv(f'gamelogs/{i}_{month}_02_statcast.csv')
            except:
                month_two_df = pd.DataFrame()

            month_df = pd.concat([month_one_df,month_two_df],ignore_index=True)
            del month_one_df
            del month_two_df

            season_df = pd.concat([season_df,month_df],ignore_index=True)
            del month_df

        #print(season_df)

        season_df = season_df.loc[season_df['game_type'] == 'R']
        dates_arr = season_df['batter'].tolist()
        dates_arr = [*set(dates_arr)]
        #dates_arr.sort()
        #print(dates_arr)
        batting_game_stats_df = pd.DataFrame()
        for j in tqdm(dates_arr):
            pass
            data = mlb.mlbam_player_season_hitting_stats(j,i)
            # print(data)
            # batting_game_stats_df = pd.concat([batting_game_stats_df,data],ignore_index=True)
        batting_game_stats_df.to_csv('test.csv')

def main():
    print('Starting up.')
    #get_season_batting(2000,2020)
    get_player_game_batting_stats(2020)

if __name__ == "__main__":
    main()