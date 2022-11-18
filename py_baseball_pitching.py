from pybaseball import pitching_stats

for i in range(1880,2023):
    print(f'Getting stats for the {i} MLB season.')
    data = pitching_stats(i,qual=0)
    data.to_csv(f'pitching\season_box\{i}_pitching_season_box.csv',index=False)