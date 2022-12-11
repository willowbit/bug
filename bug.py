import enum, spotipy, time, discord, random, time, asyncio
from discord.ext import tasks
from quote import quote
from genericpath import exists
from re import M
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from distutils.cmd import Command
from discord.ui import Button
from discord import ButtonStyle

spot = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

# Functions to be called by commands
async def getQuote(q):
    x = quote(q, limit=1, length=100)
    y = random.choice(x)
    return f'>>> *" {y["quote"]} "*\n— {y["author"]}'

async def morning(message):
    today = time.strftime("%B %d, %Y")
    morningList = ['love', 'morning', 'sunrise', 'day', 'peace', 'beauty', 'book', 'bed', 'breath']
    qt = await getQuote(random.choice(morningList))
    # mes = "🌄 **Good Morning, {mention}!!\n⏰ Today is " + today + ".**\nTo start your day today, grab a :drink ☕ and enjoy the quiet. 😴\n" + qu
    mes = discord.Embed(title=f"🌄 __Good Morning, {message.author.name}.__", color=0xe5a50a)
    # mes.set_author(name="bug", icon_url="https://cdn.discordapp.com/avatars/1025397580345118750/43ae831635f07ed13e655f9a7536cb1b.webp?size=80")
    mes.add_field(name="⏰ Today is " + today + ".", value=f"To start your day today, grab a !drink ☕ and enjoy the quiet. 😴")
    # mes.add_field(name="To start your day today, grab a !drink ☕ and enjoy the quiet. 😴", value=f"a good day always starts with something to sip.", inline=True)
    mes.add_field(name="🍐 Your quote ~", value=f"{qt}", inline=True)
    mes.set_footer(text="hello :3 i'm bug, if u would learn a bit more, i'll show you with !help 🐞")
    return mes

async def drink(message):
    i = []
    for x in commands['randomize'].keys():
        if x in ['!tea', '!coffee', 'cocoa']:
            for p in commands['randomize'][x]:
                i.append(p)
    return random.choice(i)
    # x = random.choice(list(commands['randomize'].items()))
    # x = random.choice(list(x[1].items()))[1]
    # return x

async def nowplaying(message):
    spot = message.author.activities[1]
    myurl = spot.track_url
    title = spot.title
    artist = spot.artist
    albmart = spot.album_cover_url
    myembed = discord.Embed(title=f"🎵  {title}  🎶", description=f"~ *{artist}*", color=0xe5a50a)
    myembed.set_thumbnail(url=albmart)
    myembed.set_author(name=f"{message.author.nick}'s headphones 🎧", icon_url=f"{message.author.display_avatar}")

    mybutton = discord.ui.Button(style=ButtonStyle.link, url=myurl, label="open track")
    myview = discord.ui.View()
    myview.add_item(mybutton)

    return myembed, myview

async def commandlist(message):
    mes = discord.Embed(title="command list 🐞", description="""here is all the commands I can do! but there is also lots of secret ones ^^
    **!help** ~ *this one displays the help page*
    **!commands** ~ *ur here right now!*
    **!morning** ~ *a little message to jumpstart your day. 🌄*
    **!np** ~ *displays the name, artist, + album art of your current song!! 🎶*
    **!hug** ~ *feelin bad? feelin sad? <3*
    **!compliment** ~ *i've got loads of them, there's so much i like about you!*
    **!drink** ~ *siipppppp ☕*
    **!coffee** ~ *hot brew, just for you!*
    **!tea** ~ *boiled and fresh. 🍵*
    """, color=0xe5a50a)
    mes.set_author(name="bug", icon_url="https://cdn.discordapp.com/avatars/1025397580345118750/43ae831635f07ed13e655f9a7536cb1b.webp?size=80")
    return mes
    
# A dictionary containing commands + output
commands = {
    'simple': {
        '!helnelo': 'helo !! ^^',
        '!help': "hello, {mention}! my name is bug, and i'm just here to have some fun, and help out when I can :] if you would like to see the commands i can do, you can check them out with !commands. 🐞",
        '!gay': 'this bug is bi! ^^ 🏳️‍🌈',
        '!hug': "oh! a hug? absolutely! **you deserve to feel safe, {mention}.**\nhttps://i.pinimg.com/originals/ab/78/37/ab7837f1496fc2b48080976c6bdd2f8c.gif",
        '!nomnom': "",
    },
    '!compliment': [
            "{mention}, did you know you make my day?",
            "there is no sight more wonderful than you, {mention}",
    ],
    'hard': {
        '!drink': drink,
    },
    'button': {
        '!np': nowplaying,
    },
    'embed': {
        '!morning': morning,
        '!commands': commandlist,
    },
    'randomize': {
        '!tea': [
            'here you go, {mention}, 🍵',
            "a perfect cup of tea for a perfect person, 🍵 {mention}",
            "brewed up just for you! 🍵 {mention}",
            "{mention} 🍵 i remembered and prepared it just how you like it. <3",
            "don't worry about finishing it all, {mention}. 🍵",
            "sometimes a nice, easy drink is all we need, {mention} 🍵",
        ],
        '!coffee': [
            'served in your favorite mug~ 🤎 ☕ {mention}',
            '{mention} "bvvv grrrr crcrrjkhfggg" - *the coffee machine* ☕',
            "heres a drink to wake you up, {mention} ☕",
            "coffee is love, coffee is life. {mention} ☕",
        ],
        '!cocoa': [
            "a warm, sweet drink is important for days like this. {mention} ☕",
            "your hot cocoa, {mention}. ☕",
            "with extra sugar, {mention}. ☕",
            "make sure not to spill it on your shirt, {mention}. ☕",
            "made with love, {mention} ☕ drink carefully."
        ],
        '!compliment': [
            "{mention}, did you know you make my day?",
            "there is no sight more wonderful than you, {mention}",
        ],
        '!flirt': [
            "heyy, {mention}, the forecast predicts a shower later, make sure you bundle up because sugar melts in rain ;)",
            "do you work with bees, {mention}? because you're a keeper 🐝🍯",
            "are you a bumblebee, {mention}? because I think I'm pollen for you. <3",
        ]
    },
    'trigger': {
        'amongus': 'https://media.tenor.com/YebbLUmkg9YAAAAM/among-us.gif',
    }

}

@tasks.loop(seconds=180)
async def ch_pr():
    # get spotify stuff
    plstid = random.choice(['https://open.spotify.com/playlist/37i9dQZF1EpviwO4QqFK8r?si=33cc40ace5ce4516','https://open.spotify.com/playlist/37i9dQZF1EpuGCtVi5JaUY?si=4d8a8f439c7c42fc'])
    plst = spot.playlist_tracks(playlist_id=plstid)
    rndsong = random.choice(plst['items'])['track']
    rndsong_name = rndsong['name']
    rndsong_artist = rndsong['artists'][0]['name']
    rndsong_albumart = rndsong['album']['images']

    # set status
    stts = discord.Activity(name=f"{rndsong_name} by {rndsong_artist}", type=discord.ActivityType.listening,)
    await client.change_presence(status=discord.Status.idle, activity=stts)
    
@client.event   # Send a message when the bot is ready
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.wait_until_ready()
    ch_pr.start()

@client.event   # When a message is sent...
async def on_message(message):

    # Check if the author is a user
    if message.author == client.user:
        return

    # Check whether the bot should act on the message
    isCommand = False
    for value in commands.values():
        for v in value:
            if message.content in v:
                isCommand = True
                await message.channel.typing()


    # Act on the message
    if isCommand == True:

        # If the message is in the simple keys
        if message.content in list(commands['simple'].keys()):
            await message.channel.send(commands['simple'][message.content].format(mention = message.author.mention))

        if message.content in list(commands['hard'].keys()):
            res = commands['hard'][message.content]
            res = await res(message)
            await message.channel.send(res.format(mention = message.author.mention))

        # If the message calls an embed
        if message.content in list(commands['embed'].keys()):
            res = commands['embed'][message.content]
            res = await res(message)
            await message.channel.send(embed=res)

        # If the message calls a button
        if message.content in list(commands['button'].keys()):
            res = commands['button'][message.content]
            myembed, myview = await res(message)
            await message.channel.send(embed=myembed, view=myview)

        # If the message is in the randomized keys
        if message.content in list(commands['randomize'].keys()):
            x = random.choice(commands['randomize'][message.content])
            await message.channel.send(x.format(mention = message.author.mention))

        # If the message contains a trigger word
        for x in message.content.split():
            if x in list(commands['trigger']):
                await message.channel.send(commands['trigger'][x])


def run_client():   # Run the bot with the token in botToken.txt
    f = open('botToken.txt', 'r')
    botToken = f.read()
    client.run(botToken)

run_client()