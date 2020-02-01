import re
import discord
from discord.ext import commands
from ids import *

class CommandCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot  

    @commands.command()
    async def lfg(self, ctx, message: str):
        
        try:
            voice_channel = ctx.author.voice.channel
        except AttributeError:
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
        except AttributeError:
            pass
        else:
            tmp = invite_channel.category_id
            lfg_ch = guild.get_channel(list_lfg_id[list_vc_category.index(tmp)])

            invite = await invite_channel.create_invite()
            
            lfg_members = []
            for m in invite_channel.members:
                lfg_members.append(m.name) 

            await lfg_ch.send(invite.url + ' ' +  message + '\n現在のメンバー\n```' + '\n'.join(lfg_members) + '```')
    

def setup(bot):
    bot.add_cog(CommandCog(bot))
    print('cog setup done')
    