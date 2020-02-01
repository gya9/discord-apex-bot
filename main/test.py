import discord
import cog.commandcog as commandCog
from discord.ext import commands

from ids import *
from keys import *

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))
    guild = bot.get_guild(guild_id)

    commandCog.setup(bot)

    # # ロール付与用メッセージ
    # role_channel = bot.get_channel(role_channel_id)
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


@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return

    print('Message from {0.author}: {0.content}'.format(message))

    if message.content.startswith('!bye'):
        '''終了用コマンド'''
        await message.delete()
        await bot.close()

    # コマンド共存用
    await bot.process_commands(message)


@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(guild_id)
    member = guild.get_member(payload.user_id)
    channel = guild.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if payload.message_id == give_role_msg:  # 階級選択ボタン

        for reaction in message.reactions:
            if str(reaction.emoji) != str(payload.emoji):
                await reaction.remove(member)

        list_ranks_emoji = ['🟤', '⚪', '🟡', '🔵', '🔷', '🔴']
        role_id_add = False

        if str(payload.emoji) in list_ranks_emoji:
            role_id_add = list_role_id_ranks[list_ranks_emoji.index(
                str(payload.emoji))]
            role_add = guild.get_role(role_id_add)

        if role_id_add:
            await member.add_roles(role_add)

    if payload.message_id == reset_role_msg:  # 階級リセットボタン
        message_class = await channel.fetch_message(reset_role_msg)
        for reaction in message_class.reactions:
            await reaction.remove(member)
        message_reset = await channel.fetch_message(reset_role_msg)
        for reaction in message_reset.reactions:
            await reaction.remove(member)

        for role_id_remove in list_role_id_ranks:
            role_remove = guild.get_role(role_id_remove)
            await member.remove_roles(role_remove)


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == give_role_msg:  # 階級選択ボタン

        guild = bot.get_guild(guild_id)
        member = guild.get_member(payload.user_id)

        list_ranks_emoji = ['🟤', '⚪', '🟡', '🔵', '🔷', '🔴']
        role_id_remove = False

        if str(payload.emoji) in list_ranks_emoji:
            role_id_remove = list_role_id_ranks[list_ranks_emoji.index(
                str(payload.emoji))]
            role_remove = guild.get_role(role_id_remove)

        if role_id_remove:
            await member.remove_roles(role_remove)


@bot.event
async def on_voice_state_update(member, before, after):
    guild = bot.get_guild(guild_id)
    # cat_rank1 = guild.get_channel(664773527735500802)

    for i, cat in enumerate(list_vc_category):
        cat = guild.get_channel(cat)

        flg_allfull = True
        for vc in cat.channels:
            if vc.members == []:
                if flg_allfull:
                    flg_allfull = False
                else:
                    await vc.delete()

        if flg_allfull:
            await cat.create_voice_channel('tmp', user_limit=3)

        for j, vc in enumerate(cat.channels,1):
            await vc.edit(name='{}{}'.format(list_vc_category_str[i], str(j).zfill(2)))


bot.run(discord_token)
