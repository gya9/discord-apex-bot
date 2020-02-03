import re, requests, bisect
import discord
# import sys
import json
from discord.ext import commands
from ids import *
from keys import *

class CommandCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot  

    @commands.command()
    async def lfg(self, ctx, message: str):
        
        try:
            voice_channel = ctx.author.voice.channel
        except AttributeError as e:
            print(e)
            await ctx.send('お前はカス(ボイスチャンネルに居ない)')
        else:
            if voice_channel != None:
                invite = await voice_channel.create_invite(reason='!lfg')

                message = message.lower()

                rank_search_list = [['b'],['s'],['g'],['p'],['d']]
                rank_str_list = [' bronze',' silver',' gold',' platinum',' diamond']

                if re.search(r'^[bsgpd][1-4]$', message, re.IGNORECASE):
                    for i in range(len(rank_search_list)):
                        if message[0] in rank_search_list[i]:
                            await ctx.send(invite.url + rank_str_list[i] + message[-1])
                            return

                await ctx.send('お前はカス(ランク指定を間違っている)')

    @commands.command()
    async def bo(self, ctx, message: str):
        guild = ctx.guild

        try:
            invite_channel = ctx.author.voice.channel
        except AttributeError as e:
            print(e)
            pass
        else:
            tmp = invite_channel.category_id
            lfg_ch = guild.get_channel(list_lfg_id[list_vc_category.index(tmp)])

            invite = await invite_channel.create_invite()
            
            lfg_members = []
            for m in invite_channel.members:
                lfg_members.append(m.name) 

            await lfg_ch.send(invite.url + ' ' +  message + '\n現在のメンバー\n```' + '\n'.join(lfg_members) + '```')

    @commands.command()
    async def rank(self, ctx, message: str):
        guild = ctx.guild

        try:
            #request部分は後々別メソッドに分けたほうが良さそう
            header = {'TRN-Api-Key': trn_token}
            r = requests.get(trn_url + 'origin/' + message + '/', headers= header)
            player_data = r.json()
            stats = player_data['data']['segments'][0]['stats']

            #2分探索
            rank = bisect.bisect_left(list_rank_rp,stats['rankScore']['value']) - 1

            if rank == 20 :
                embed = discord.Embed(title='Rank', description=list_rank_name[rank] + ' #' + str(stats['rankScore']['rank']), color=list_rank_colors[int(rank / 4)])
            else:
                embed = discord.Embed(title='Rank', description=list_rank_name[rank], color=list_rank_colors[int(rank / 4)])

            for k,v in stats.items():
                value = v['value']
                if type(value) == float:
                    value = int(value)
                embed.add_field(name=v['displayName'], value=value)
                

            embed.set_author(name=message + 'さんの戦績', url='https://apex.tracker.gg/profile/pc/' + message, icon_url=player_data['data']['platformInfo']['avatarUrl'])
            # print(json.dumps(player_data['data']['segments'][0], indent=2))
            embed.set_thumbnail(url='https://trackercdn.com/cdn/apex.tracker.gg/ranks/' + list_rank_imgurl[rank] + '.png')

        except requests.exceptions.RequestException as e:
            print(e)
            await ctx.channel.send('データを取得できませんでした。')
            pass
        except KeyError as e:
            print(e)
            await ctx.channel.send('指定されたプレイヤーは見つかりませんでした。')
            pass
        else:
            await ctx.channel.send(embed=embed)
    

def setup(bot):
    bot.add_cog(CommandCog(bot))
    print('cog setup done')
