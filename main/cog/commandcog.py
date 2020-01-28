import re
import discord
from discord.ext import commands

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

                if re.search(r'^[bsgpd][1-4]$', message, re.IGNORECASE):
                    if message[0] in ['b','B']:
                        await ctx.send(invite.url + ' bronze' + message[-1])
                    return
            
                await ctx.send('お前はカス(ランク指定を間違っている)')


    

def setup(bot):
    bot.add_cog(CommandCog(bot))
    print('cog setup done')
    