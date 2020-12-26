import discord
import asyncio
from googlei import search
client = discord.Client()

import logging, random
import dotenv
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

logging.basicConfig(level=logging.INFO)

def processPokemon(embed):
    url = embed['image']['url']
    res = search(url)
    print(res)

    for l in res['links']:
        if "https://pokemondb.net/pokedex/" in l:
            s = l.replace("https://pokemondb.net/pokedex/", "").strip()
            return "p!catch " + s.lower()
        if "https://bulbahandbook.bulbagarden.net/pokemonsunmoon/pokemon/" in l:
            s = l.replace(
                "https://bulbahandbook.bulbagarden.net/pokemonsunmoon/pokemon/", "").strip()
            return "p!catch " + s.lower()

    s = res['best_guess']
    s = s.replace("pokemon", "").strip()
    return "p!catch " + s.lower()



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if len(message.embeds) != 0 and message.embeds[0]['title'] == 'A wild pokémon has appeared!':
        print(message.content)
        print(message.embeds)
        await client.send_message(message.channel, processPokemon(message.embeds[0]))

client.run(token,bot=False)
