import discord

from keys import *

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

        # # ロール付与用メッセージ
        # role_channel = self.get_channel(role_channel_id)
        # text = "あなたの階級のボタンを押してください"
        # m = await role_channel.send(text)
        # await m.add_reaction('🟤')
        # await m.add_reaction('⚪')
        # await m.add_reaction('🟡')
        # await m.add_reaction('🔵')
        # await m.add_reaction('🔷')
        # await m.add_reaction('🔴')

        # text = ":arrow_down:階級ロールリセットボタン"
        # m = await role_channel.send(text)
        # await m.add_reaction('🔄')


    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        print('Message from {0.author}: {0.content}'.format(message))
        
        if message.content.startswith('!bye'):
            '''終了用コマンド'''
            await message.delete()
            await self.close()
        

    async def on_raw_reaction_add(self, payload):
        guild = self.get_guild(664748839256850474)
        member = guild.get_member(payload.user_id)
        channel = guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if payload.message_id == 664786846479417369: #階級選択ボタン

            for reaction in message.reactions:
                if str(reaction.emoji) != str(payload.emoji):
                    await reaction.remove(member)

            list_ranks_emoji = ['🟤','⚪','🟡','🔵','🔷','🔴']
            role_id_add = False

            if str(payload.emoji) in list_ranks_emoji:
                role_id_add = list_role_id_ranks[list_ranks_emoji.index(str(payload.emoji))]
                role_add = guild.get_role(role_id_add)

            if role_id_add:
                await member.add_roles(role_add)
        
        if payload.message_id == 664786857745317899: #階級リセットボタン
            message_class = await channel.fetch_message(664786846479417369)
            for reaction in message_class.reactions:
                await reaction.remove(member)
            message_reset = await channel.fetch_message(664786857745317899)
            for reaction in message_reset.reactions:
                await reaction.remove(member)

            for role_id_remove in list_role_id_ranks:
                role_remove = guild.get_role(role_id_remove)
                await member.remove_roles(role_remove)

    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 664786846479417369: #階級選択ボタン

            guild = self.get_guild(664748839256850474)
            member = guild.get_member(payload.user_id)

            list_ranks_emoji = ['🟤','⚪','🟡','🔵','🔷','🔴']
            role_id_remove = False

            if str(payload.emoji) in list_ranks_emoji:
                role_id_remove = list_role_id_ranks[list_ranks_emoji.index(str(payload.emoji))]
                role_remove = guild.get_role(role_id_remove)

            if role_id_remove:
                await member.remove_roles(role_remove)


client = MyClient()
client.run(discord_token)

