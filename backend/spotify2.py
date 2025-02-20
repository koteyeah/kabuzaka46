import pandas as pd
import numpy as np
# CSVファイルを読み込む
df = pd.read_csv('nogizaka_tracks_features.csv')
# 'valence' 列の正規化
df['valence_normalized'] =1- (df['valence'] - df['valence'].min()) / (df['valence'].max() - df['valence'].min())

# 'danceability' 列の正規化
df['danceability_normalized'] =1- (df['danceability'] - df['danceability'].min()) / (df['danceability'].max() - df['danceability'].min())

# 'energy' 列の正規化
df['energy_normalized'] = (df['energy'] - df['energy'].min()) / (df['energy'].max() - df['energy'].min())
# 'tempo' 列の正規化
df['tempo_normalized'] = (df['tempo'] - df['tempo'].min()) / (df['tempo'].max() - df['tempo'].min())
# 'energy*tempo' 列の正規化
df['energy_tempo_sqrt'] = np.sqrt(df['energy_normalized'] * df['tempo_normalized'])
df['energy_tempo_normalized'] = 1-(df['energy_tempo_sqrt'] - df['energy_tempo_sqrt'].min()) / (df['energy_tempo_sqrt'].max() - df['energy_tempo_sqrt'].min())
# 'popularity' 列の正規化
df['popularity_normalized'] = 1-(df['popularity'] - df['popularity'].min()) / (df['popularity'].max() - df['popularity'].min())
df['popularity_rank'] = df['popularity'].rank(method='min', ascending=False)

# DataFrameをCSVファイルに保存
df.to_csv('/Users/user/Desktop/nogizaka_tracks_features2.csv', index=False)

print("CSVファイルに出力が完了しました。")