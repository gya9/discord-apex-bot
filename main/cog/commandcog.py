import re, requests, bisect
import discord
# import sys
import json
from discord.ext import commands, tasks
from ids import *
from keys import *
from func import *

class CommandCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot  
        self.index = 0
        self.update_task.start()

    @tasks.loop(hours=1)
    async def update_task(self):
        '''1時間おきに全userのrank情報を更新'''
        update_stats_all()
        print('updated')


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
        cat_id = ctx.author.voice.channel.category.id
        lfg_ch = guild.get_channel(list_lfg_id[list_vc_category.index(cat_id)])
        invite_str = await create_lfg_msg(guild, ctx.author.voice.channel, message)
        await lfg_ch.send(invite_str)

    @commands.command()
    async def rank(self, ctx, message: str):
        guild = ctx.guild

        if not trn_api_stats(message):
            await ctx.send('戦績の取得に失敗しました。IDが間違っていないかご確認ください。')
        else:
            player_data, stats = trn_api_stats(message)
            
            rank_str, rank = calculate_rank(stats)
            embed = discord.Embed(title='Rank', description=list_rank_name[rank], color=list_rank_colors[int(rank / 4)])

            for k,v in stats.items():
                value = v['value']
                if type(value) == float:
                    value = int(value)
                embed.add_field(name=v['displayName'], value=value)
                
            embed.set_author(name=message + 'さんの戦績', url='https://apex.tracker.gg/profile/pc/' + message, icon_url=player_data['data']['platformInfo']['avatarUrl'])
            # print(json.dumps(player_data['data']['segments'][0], indent=2))
            embed.set_thumbnail(url='https://trackercdn.com/cdn/apex.tracker.gg/ranks/' + list_rank_imgurl[rank] + '.png')
            await ctx.channel.send(embed=embed)

            update_stats(ctx.author.id, rank_str)

    @commands.command()
    async def update(self, ctx):
        update_stats_all()


    @commands.command()
    async def purge(self, ctx):
        channel = ctx.channel
        await channel.purge()

def setup(bot):
    bot.add_cog(CommandCog(bot))
    print('cog setup done')
