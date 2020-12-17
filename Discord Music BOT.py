from youtube_search import YoutubeSearch
from discord.ext import commands as com
from os import remove, rename
from spotdl import Spotdl
import discord as dis
import pafy
import glob as G
import asyncio

#! Coding by Ai-Sasit
#! Last Modified: 12 Dec 2020

client = com.Bot(command_prefix='$')
Token_ID = 'NDAxMzk2NzM5NDg1MDczNDA4.WljT2A.CguKkQnfiknQ89mZfHagFm0FXiU'

TubeList = list()
NameList = list()
np_name = ["Null"]

def PyTube(search):
    if ("$music_temp.m4a" in G.glob("*.m4a")): remove("$music_temp.m4a")
    if ("www" in search or "http" in search): 
        result = pafy.new(search)
    else:
        results = YoutubeSearch(search, max_results=1).to_dict()
        result = pafy.new("www.youtube.com" + dict(results[0])["url_suffix"])
    m4a = result.m4astreams[0]
    m4a.download()
    name = G.glob("*.m4a")[0]
    rename(name, "$music_temp.m4a")
    return result.title

def PySpot(Search):
    if ("$music_temp.m4a" in G.glob("*.m4a")): remove("$music_temp.m4a")
    with Spotdl() as spotdl_handler:
        spotdl_handler.download_track(Search)
    rename(G.glob("*.mp3")[0], "$music_temp.m4a")

def AddTubeList(Search):
    if ("www" in Search or "http" in Search): TubeList.append(Search)
    else:
        Y = YoutubeSearch(Search, max_results=1).to_dict()
        Search = "www.youtube.com" + dict(Y[0])["url_suffix"]
        TubeList.append(Search)
    result = pafy.new(Search)
    NameList.append(result.title)
    return result.title

def PlayQueue(ctx):
    print("Music is End!")
    if ("$music_temp.m4a" in G.glob("*.m4a")): remove("$music_temp.m4a")
    try:
        Inlist = TubeList.pop(0)
        NameList.pop(0)
    except:
        np_name[0] = "Nothing is playing."
        return None
    result = pafy.new(Inlist)
    np_name[0] = result.title
    m4a = result.m4astreams[0]
    m4a.download()
    name = G.glob("*.m4a")[0]
    rename(name, "$music_temp.m4a")
    ctx.voice_client.play(dis.FFmpegPCMAudio("$music_temp.m4a"), after=lambda e: PlayQueue(ctx))

@client.event
async def on_ready():
    print("------- System is Activated -------")
    print("-          BOT is Online          -")
    print("- Connected to Discord as {}. -".format(client.user.name))
    print("-----------------------------------")
    await client.change_presence(activity = dis.Activity(type = dis.ActivityType.listening, name = '$help'))

@client.command()
async def Direct(ctx):
    await ctx.author.send('ดีจ้าาา')

@client.command(aliases=['view', 'pro'])
async def Profile(ctx, member: dis.Member):
    print(f"Viewing Picture Profile : {member}")
    Show_Profile = dis.Embed(color=dis.Color.dark_gold())
    Show_Profile.set_image(url=f'{member.avatar_url}')
    await ctx.send(embed=Show_Profile)

@client.command(aliases=['Play', 'P', 'p', 'play'])
async def Youtube(ctx, *text):
    try: np_name[0] = Title = PyTube(" ".join(text))
    except:
        Queue_Title = AddTubeList(" ".join(text))
        Show_Adding = dis.Embed(color=0x00ff9d)
        Show_Adding.add_field(name='Adding to queue ...',value=Queue_Title, inline=False)
        await ctx.send(embed=Show_Adding)
        return None
    Show_Playing = dis.Embed(color=dis.Color.dark_green())
    Show_Playing.add_field(name="Now Playing ...", value=Title, inline=False)
    await ctx.send(embed=Show_Playing)
    channel = ctx.author.voice.channel
    try: await channel.connect()
    except: pass
    finally: vc = ctx.voice_client.play(dis.FFmpegPCMAudio("$music_temp.m4a"), after=lambda e: PlayQueue(ctx))

@client.command(aliases=['spot', 'sp'])
async def Spotify(ctx, Link):
    PySpot(Link)
    channel = ctx.author.voice.channel
    try: await channel.connect()
    except: pass
    finally: ctx.voice_client.play(dis.FFmpegPCMAudio("$music_temp.m4a"), after=lambda e: print('Done!'))

@client.command()
async def stop(ctx):
    try:
        ctx.voice_client.pause()
        await ctx.send(":white_check_mark: Music is Paused!")
        await asyncio.sleep(2)
    except:
        await ctx.send(":warning: Somethings is Wrong!")

@client.command(aliases=["re"])
async def resume(ctx):
    try:
        ctx.voice_client.resume()
        await ctx.send(":white_check_mark: Music is Resumed!")
        await asyncio.sleep(2)
    except:
        await ctx.send(":warning: Somethings is Wrong!")

@client.command(aliases=['sk'])
async def skip(ctx):
    try:
        ctx.voice_client.stop()
        await ctx.send(":white_check_mark: Music is Skipped!")
        await asyncio.sleep(2)
    except:
        await ctx.send(":warning: Somethings is Wrong!")

@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await ctx.send(":beginner: In your service.")
    await channel.connect()

@client.command(aliases=['dc', 'leave', 'quit', 'exit'])
async def Disconnect(ctx):
    print("BOT is Disconnected the voice channel")
    await ctx.send(":regional_indicator_g: :regional_indicator_o: :regional_indicator_o: :regional_indicator_d:   :regional_indicator_b: :regional_indicator_y: :regional_indicator_e: ")
    await ctx.voice_client.disconnect()

@client.command(aliases=['Q', 'q', 'qu'])
async def Queue(ctx):
    if(len(TubeList) == 0):
        await ctx.send(":package: Queue is empty!")
    else:
        Show_Queue = dis.Embed(color=0x00ff9d)
        Show_Queue.add_field(name="In Queue.", value='\n'.join(NameList), inline=False)
        await ctx.send(embed=Show_Queue)

@client.command()
async def clear(ctx):
    if(len(TubeList) == 0):
        await ctx.send(":warning: Queue is already clear!")
    else:
        TubeList.clear()
        await ctx.send(":broom: Queue is clearing completed!")

@client.command(aliases=['np'])
async def NowPlaying(ctx):
    Show_NP = dis.Embed(color=0xffd333)
    Show_NP.add_field(name="Current Playing ...", value=np_name[0], inline=False)
    await ctx.send(embed=Show_NP)

@client.command(aliases=["rq"])
async def removequeue(ctx, index:int):
    Remove = dis.Embed(color=0xff0066)
    Remove.add_field(name="Remove queue! ", value=NameList.pop(index-1), inline=False)
    TubeList.pop(index-1)
    await ctx.send(embed=Remove)

client.run(Token_ID)
