import re, requests, bisect
import numpy as np
import pandas as pd
from ids import *
from keys import *

def trn_api_stats(Origin_id):
    '''Tracker Network Apiによって、origin idからStatsデータを取得'''
    try:
        header = {'TRN-Api-Key': trn_token}
        r = requests.get(trn_url + 'origin/' + Origin_id + '/', headers= header)
        player_data = r.json()
        stats = player_data['data']['segments'][0]['stats']

    except requests.exceptions.RequestException as e:
        print(e)
        return False
    except KeyError as e:
        print(e)
        return False
    else:
        return player_data, stats

def add_origin_id(discord_id, origin_id):
    '''discord idとorigin idを紐付け'''
    if not trn_api_stats(origin_id):
        return False
    
    df = pd.read_csv('users.csv')
    df.origin_id[df.discord_id == discord_id] = origin_id
    df.to_csv('users.csv')
    return True


def check_member_list(list_member_id):
    '''users.csvにdiscordIDが登録されていないユーザーがいた場合新たに登録'''
    df = pd.read_csv('users.csv')

    for _id in list_member_id:
        if _id not in list(df['discord_id']):
            _df = pd.DataFrame(columns=['discord_id', 'origin_id'])
            add_list = [str(_id), np.nan]
            add_row = pd.Series(add_list, index=_df.columns)
            _df = _df.append(add_row, ignore_index=True)
            df = pd.concat([df,_df], ignore_index=True, sort=False)

    df.to_csv('users.csv',index=False)