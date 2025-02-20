import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

# Spotify APIのクライアントIDとクライアントシークレットを設定
client_id = 'f436a1fbbed14f4cbe42cc835327b642'
client_secret = 'b73940bd41044135875b073c8ff45a4f'


# クレデンシャルを使用してSpotify APIに接続
credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=credentials)

# 乃木坂46のアーティストIDを取得
result = sp.search(q='乃木坂46', type='artist')
artist_id = result['artists']['items'][0]['id']

# 乃木坂46の全アルバムとトラックを取得
albums = []
results = sp.artist_albums(artist_id, album_type='album,single', limit=50)
albums.extend(results['items'])
while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])

all_tracks = []

for album in albums:
    tracks = sp.album_tracks(album['id'])
    for track in tracks['items']:
        # 曲名に「off vocal」が含まれていないことを確認
        if 'off vocal' not in track['name'].lower():
            track_info = {
                'track_id': track['id'],
                'track_name': track['name'],
                'preview_url': track['preview_url']
            }
            all_tracks.append(track_info)

def get_audio_features_with_retry(track_id):
    retries = 5
    while retries > 0:
        try:
            features = sp.audio_features(track_id)[0]
            return features
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 429:
                retry_after = int(e.headers.get('Retry-After'),60)
                print(f"Rate limit exceeded, retrying after {retry_after} seconds")
                time.sleep(retry_after)
                retries -= 1
            else:
                raise e
    return None

# 各曲の詳細情報を取得し、人気度を含める
track_features = []

for track in all_tracks:
    track_detail = sp.track(track['track_id'])
    print(track['track_name'])
    features = get_audio_features_with_retry(track['track_id'])
    # features = sp.audio_features(track['track_id'])[0]

    if features:
        # track_nameとtrack_idを先頭に挿入
        features['track_name'] = track['track_name']
        features['track_id'] = track['track_id']
        features['preview_url'] = track['preview_url']
        features['popularity'] = track_detail['popularity']  # 人気度を追加

        track_features.append(features)

# DataFrameに変換し、列の順番を指定
df = pd.DataFrame(track_features, columns=['track_name', 'track_id', 'preview_url', 'popularity'] + [col for col in track_features[0].keys() if col not in ['track_name', 'track_id', 'preview_url', 'popularity']])

# 同じ曲名のものを除外する
df = df.drop_duplicates(subset=['track_name'])
# 必要な列だけを保持するために、不要な列をドロップ
df = df[['track_name', 'track_id', 'popularity','mode','valence','danceability', 'energy', 'tempo',  'preview_url']]

# DataFrameをCSVファイルに保存
df.to_csv('/Users/user/Desktop/nogizaka_tracks_features.csv', index=False)

print("CSVファイルに出力が完了しました。")
