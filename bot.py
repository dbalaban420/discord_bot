import discord
import logging
from discord.ext import commands
import random
import os
import asyncio
import json

logging.basicConfig(level=logging.INFO)

client = discord.Client()
commands = ["!roll", "!hi", "!toss", "!shutdown", "!getinfo", "!updateinfo", "!addinfo", "!delinfo"]
infos = ["list of json files with info: users and their ids, channels and their ids"]

async def check(author):
    if author in allowed_list.values():
        return True

async def getinfo(message):
    if (not await check(message.author.id)):
        return
    try:
        request = str(message.content.split(' ')[1])
        if request not in infos:
            await message.channel.send("Bad request")
            return
    except Exception:
        await message.channel.send("Bad request")
        return

    with open (fr"{os.path.dirname(os.path.realpath(__file__))}\data\{request}.json", "r") as rq:
        await message.channel.send(rq.read())

async def addinfo(message):
    if (not await check(message.author.id)):
        return

    try:
        request = str(message.content.split(' ')[1])
        if request not in infos:
            await message.channel.send("Bad request")
            return

        req_name = str(message.content.split(' ')[2])
        req_ID = int(message.content.split(' ')[3])

    except Exception:
        await message.channel.send("Bad request")
        return

    update_dict = {req_name: req_ID}

    with open (fr"{os.path.dirname(os.path.realpath(__file__))}\data\{request}.json", "r+") as rq:
        data = json.load(rq)
        data.update(update_dict)
        rq.seek(0)
        json.dump(data, rq, indent = 4)

    await updateinfo()
    
async def delinfo(message):
    if (not await check(message.author.id)):
        return

    try:
        request = str(message.content.split(' ')[1])
        if request not in infos:
            await message.channel.send("Bad request")
            return

        req_ID = int(message.content.split(' ')[2])
        
    except Exception:
        await message.channel.send("Bad request")
        return

    with open (fr"{os.path.dirname(os.path.realpath(__file__))}\data\{request}.json", "r") as rq:
        data = json.load(rq)
    for name, ID in data.items():
        if ID == req_ID:
            req_name = name
    del data[req_name]

    with open (fr"{os.path.dirname(os.path.realpath(__file__))}\data\{request}.json", "w") as rq:
        json.dump(data, rq, indent = 4)

    await updateinfo()

async def updateinfo():
    try:
        with open (fr"{os.path.dirname(os.path.realpath(__file__))}\data\"server name, for which you update the channels".json", "r") as tr:
            "server name, for which you update the channels" = json.load(tr)

        await message.channel.send("Done")

    except Exception as ex:
        print(ex)
        await message.channel.send("Error")

async def toss(message):
    if (not await check(message.author.id)):
        return
    try:
        count = int(message.content.split(' ')[1])
        if count > 10:
            await message.channel.send("Too many flips, 10 maximum")
            count = 1
    except Exception:
        count = 1
        
    result1 = 0
    result2 = 0

    for _ in range(count):
        result = random.randrange(2)
        if result == 0:
            result1 += 1
            await message.channel.send("Орел")
        else:
            result2 += 1
            await message.channel.send("Решка")
    await message.channel.send(f"{result1} Орлов и {result2} Решек")

async def roll(message):
    if (not await check(message.author.id)):
        return
    try:
        dice = message.content.split(' ')[1]
        rolls, limit = map(int, dice.split('d'))
        if rolls > 10:
            await message.channel.send("Too many rolls, 10 maximum")
            rolls = 1
    except Exception:
        await message.channel.send('Format has to be in NdN!')
        return
    
    result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
    await message.channel.send(result)

async def shutdown(message):
    if (not await check(message.author.id)):
        return
    try:
        timeout = message.content.split(' ')[1]
        if timeout > 5000:
            await message.channel.send("Too high timeout")
            timeout = 0
    except Exception:
        timeout = 0

    await asyncio.sleep(timeout)
    os._exit(0)

async def greet(message):
    if (not await check(message.author.id)):
        return

    print(f"Responded {message.author} with haee")
    await message.channel.send("haee")

@client.event
async def on_ready():
    await updateinfo()
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):

    if message.author == client.user or (message.author.bot):
        return
    else:
        if message.content in commands:
            print(f"Got a {message.content} request from {message.author} on channel {message.channel}")
        else:
            print(f"Got a message {message.content} from {message.author} - {message.author.id} on channel {message.channel} - {message.channel.id}")
            if message.author.id in ban_list.values():
                await message.delete()

    if message.content.startswith("!toss"):
        await toss(message)

    if message.content.startswith("!roll"):
        await roll(message)

    if message.content.startswith("!hi"):
        await greet(message)
    
    if message.content.startswith("!shutdown"):
        await shutdown(message)

    if message.content.startswith("!getinfo") and message.channel.id == "privat chat with bot":
        await getinfo(message)

    if message.content.startswith("!addinfo") and message.channel.id == "privat chat with bot":
        await addinfo(message)

    if message.content.startswith("!delinfo") and message.channel.id == "privat chat with bot":
        await delinfo(message)

client.run("bot token")