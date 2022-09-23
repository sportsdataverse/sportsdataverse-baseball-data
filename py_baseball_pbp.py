from pybaseball import statcast
import pandas as pd
import pybaseball
from datetime import datetime

if __name__ == '__main__':
    pybaseball.cache.enable()
    #for i in range(1920,datetime.now().year + 1):
    for i in range(2020,datetime.now().year + 1):
        print(i)
        season_df = statcast(start_dt=f'{i}-02-01', end_dt=f'{i}-12-01')
        # season = [game_year]
        #season_df['year'] = pd.DatetimeIndex(season_df['game_date']).year
        season_df['month'] = pd.DatetimeIndex(season_df['game_date']).month
        season_df['day'] = pd.DatetimeIndex(season_df['game_date']).month

        min_month = season_df['month'].min()
        max_month = season_df['month'].max()
        
        for j in range(min_month,max_month+1):
            month = 0
            if j < 10:
                month = f"0{j}"
            else:
                month = j
            
            month_df = season_df.loc[season_df['month'] == j]
            
            len_month_df = len(month_df)
            len_month_df = len_month_df // 2

            partOne = month_df.iloc[:len_month_df]
            partTwo = month_df.iloc[len_month_df:]
            
            partOne.to_csv(f'gamelogs/{i}_{month}_01_statcast.csv',index=False)
            partTwo.to_csv(f'gamelogs/{i}_{month}_02_statcast.csv',index=False)
        
        #print(season_df)