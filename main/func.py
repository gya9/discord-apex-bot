import re, requests, bisect
import numpy as np
import pandas as pd
from ids import *
from keys import *
import discord

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
    df.to_csv('users.csv', index=False)
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

    df.to_csv('users.csv', index=False)


def get_origin_id(discord_id):
    '''users.csvに登録されているoriginIDを参照'''
    df = pd.read_csv('users.csv')
    ans_origin_id = df.origin_id[df.discord_id == discord_id].values[0]

    if ans_origin_id == np.NaN:
        return False
    else:
        return ans_origin_id


def get_rank(stats):
    '''statsデータのrankscoreから「silver4」などのdivisionを算出し文字列を返す'''
    rank = bisect.bisect_left(list_rank_rp,stats['rankScore']['value']) - 1

    if rank == 20 :
        return list_rank_name[rank] + ' #' + str(stats['rankScore']['rank']), rank
    else:
        return list_rank_name[rank], rank

async def create_lfg_msg(guild, voice_channel):

    tmp = voice_channel.category_id
    lfg_ch = guild.get_channel(list_lfg_id[list_vc_category.index(tmp)])

    invite = await voice_channel.create_invite()
    
    lfg_members = []
    for m in voice_channel.members:
        if not get_origin_id(m.id):
            lfg_members.append(m.name)
        else:
            origin_id = get_origin_id(m.id)
            if not trn_api_stats(origin_id):
                lfg_members.append(m.name + '   Origin:' + origin_id)
            else:
                player_data, stats = trn_api_stats(origin_id)
                rank_str, rank = get_rank(stats)
                lfg_members.append(m.name + '   Origin:' + origin_id + '   Rank:' + rank_str)
    invite_msg_str = invite.url + ' \n現在のメンバー\n```' + '\n'.join(lfg_members) + '```'
    print(invite_msg_str)
    return invite_msg_str
        

def update_rank(origin_id, rank_str):
    df = pd.read_csv('users.csv')
    df.apex_rank[df.origin_id == origin_id] = rank_str
    df.to_csv('users.csv', index=False)


async def update_rank_all():
    df = pd.read_csv('users.csv')
    for origin_id in df['origin_id'].dropna().values:
        _, stats = trn_api_stats(origin_id)
        rank_str, _ = get_rank(stats)
        update_rank(origin_id, rank_str)
