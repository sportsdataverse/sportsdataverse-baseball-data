import pandas as pd
from tqdm import tqdm
import sqlite3

gamelog_table = """
CREATE TABLE "statcast_pbp" (
	"pitch_type"	TEXT,
	"game_date"	TEXT,
	"release_speed"	REAL,
	"release_pos_x"	REAL,
	"release_pos_z"	REAL,
	"player_name"	TEXT,
	"batter"	INTEGER,
	"pitcher"	INTEGER,
	"events"	TEXT,
	"description"	TEXT,
	"spin_dir"	TEXT,
	"spin_rate_deprecated"	REAL,
	"break_angle_deprecated"	REAL,
	"break_length_deprecated"	REAL,
	"zone"	INTEGER,
	"des"	TEXT,
	"game_type"	TEXT,
	"stand"	TEXT,
	"p_throws"	TEXT,
	"home_team"	TEXT,
	"away_team"	TEXT,
	"type"	TEXT,
	"hit_location"	INTEGER,
	"bb_type"	TEXT,
	"balls"	INTEGER,
	"strikes"	INTEGER,
	"game_year"	INTEGER,
	"pfx_x"	REAL,
	"pfx_z"	REAL,
	"plate_x"	REAL,
	"plate_z"	REAL,
	"on_3b"	INTEGER,
	"on_2b"	INTEGER,
	"on_1b"	INTEGER,
	"outs_when_up"	INTEGER,
	"inning"	INTEGER,
	"inning_topbot"	TEXT,
	"hc_x"	REAL,
	"hc_y"	REAL,
	"tfs_deprecated"	REAL,
	"tfs_zulu_deprecated"	REAL,
	"fielder_2"	INTEGER,
	"umpire"	TEXT,
	"sv_id"	INTEGER,
	"vx0"	REAL,
	"vy0"	REAL,
	"vz0"	REAL,
	"ax"	REAL,
	"ay"	REAL,
	"az"	REAL,
	"sz_top"	REAL,
	"sz_bot"	REAL,
	"hit_distance_sc"	REAL,
	"launch_speed"	REAL,
	"launch_angle"	REAL,
	"effective_speed"	REAL,
	"release_spin_rate"	INTEGER,
	"release_extension"	REAL,
	"game_pk"	INTEGER,
	"pitcher.1"	INTEGER,
	"fielder_2.1"	INTEGER,
	"fielder_3"	INTEGER,
	"fielder_4"	INTEGER,
	"fielder_5"	INTEGER,
	"fielder_6"	INTEGER,
	"fielder_7"	INTEGER,
	"fielder_8"	INTEGER,
	"fielder_9"	INTEGER,
	"release_pos_y"	REAL,
	"estimated_ba_using_speedangle"	REAL,
	"estimated_woba_using_speedangle"	REAL,
	"woba_value"	REAL,
	"woba_denom"	INTEGER,
	"babip_value"	INTEGER,
	"iso_value"	INTEGER,
	"launch_speed_angle"	REAL,
	"at_bat_number"	INTEGER,
	"pitch_number"	INTEGER,
	"pitch_name"	TEXT,
	"home_score"	INTEGER,
	"away_score"	INTEGER,
	"bat_score"	INTEGER,
	"fld_score"	INTEGER,
	"post_away_score"	INTEGER,
	"post_home_score"	INTEGER,
	"post_bat_score"	INTEGER,
	"post_fld_score"	INTEGER,
	"if_fielding_alignment"	TEXT,
	"of_fielding_alignment"	TEXT,
	"spin_axis"	INTEGER,
	"delta_home_win_exp"	REAL,
	"delta_run_exp"	REAL,
	"month"	INTEGER,
	"day"	INTEGER
);
"""

batting_table = """
SELECT 
	game_year as season,
	batter as batter_id,
	player_name as batter_name,
	SUM(IIF(statcast_pbp.events = "double",1,0)) as `2B`
	
	
FROM 
	statcast_pbp
	
WHERE game_type = "R"
GROUP BY 
	batter, 
	player_name,
	game_year;
"""

season_min = 1974
season_max = 2022

for i in tqdm(range(season_min,season_max+1)):
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

	print(season_df)

	con = sqlite3.connect(":memory:")
	cur = con.cursor()
	print('Generating database table.')
	cur.execute(gamelog_table)
	season_df.to_sql('statcast_pbp',con,if_exists="append",index=False)
	print('Done')

	batting_df = pd.read_sql_query(batting_table,con)
	batting_df.to_csv(f'batting\season_box\{i}_batting_season_box.csv')
	print("")

	del season_df
	