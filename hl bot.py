import discord
from discord.ext import commands, tasks
import asyncio
import pytz
import datetime
from discord.ext import commands

# 봇 설정
intents = discord.Intents.default()
intents.messages = True

client = bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())

# 진행도를 알려주는 명령
@bot.command()
async def progress(ctx):
    total_duration = 10  # 총 작업 시간(예시로 10초 설정)
    embed = discord.Embed(title="작업 진행 상황", description="0% 완료", color=discord.Color.red())
    embed.add_field(name="진행도", value="□□□□□□□□□□", inline=False)
    message = await ctx.send(embed=embed)  # 초기 임베드 메시지 전송

    for i in range(1, total_duration + 1):
        progress_percent = int((i / total_duration) * 100)  # 진행도 계산
        progress_bar = '■' * i + '□' * (total_duration - i)  # 진행도 바 업데이트
        embed = discord.Embed(title="작업 진행 상황", description=f"{progress_percent}% 완료", color=discord.Color.red())
        embed.add_field(name="진행도", value=progress_bar, inline=False)
        await message.edit(embed=embed)  # 임베드 메시지 업데이트
        await asyncio.sleep(1000)  # 다음 업데이트까지 1000초 대기

    embed = discord.Embed(title="작업 완료", description="100% 완료", color=discord.Color.green())
    embed.add_field(name="진행도", value="■■■■■■■■■■", inline=False)
    await message.edit(embed=embed)  # 최종 임베드 메시지로 업데이트

@client.event
async def on_ready():
    print("D-BOT 관리봇이 실행됩니다.")
    await client.change_presence(status=discord.Status.online, activity=discord.Game("컨텐츠팀 보조"))

@client.event
async def on_message(message):
    if message.content.startswith ("!청소"):
        if message.author.guild_permissions.administrator:
            amount = message.content[4:]
            await message.delete()
            await message.channel.purge(limit=int(amount))
            embed = discord.Embed(title="메시지 삭제 알림", description="최근 디스코드 채팅 {}개가\n관리자 {}님의 요청으로 인해 정상 삭제 조치 되었습니다".format(amount, message.author), color=0x000000)
            embed.set_footer(text="담당 운영자 : {}".format(message.author), icon_url="result.png%22")
            await message.channel.send(embed=embed)

    if message.content.startswith ("!공지"):
        notice = message.content[4:]
        channel_id = 1217472772305977465
        channel = client.get_channel(channel_id)

        embed = discord.Embed(title="공지사항", description="공지사항 내용은 항상 숙지 해주시기 바랍니다\n――――――――――――――――――――――――――――\n\n{}\n\n――――――――――――――――――――――――――――".format(notice), color=0x00ff00)
        embed.set_footer(text="담당 운영자 : {}".format(message.author))
        await channel.send("@here", embed=embed)
    await bot.process_commands(message)

# 봇의 토큰을 이용해 실행
bot.run('MTIxNzQ3NDE3NDkzNTYyOTkxNA.GnPfkP.XT4DIxynzkpTUIs0nVYRZHG4W9gSy4y8Lz9qpI')
