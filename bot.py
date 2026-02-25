import discord
from discord.ext import commands
import requests
import random
import json
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)


def acha_imagem():
    imagem = random.choice(os.listdir('images'))
    return imagem


def pokemon2():
    lista_url = "https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0"
    lista = requests.get(lista_url)
        
    dados_lista = lista.json()
    total_pokemons = dados_lista['count']
    
    id_aleatorio = random.randint(1, total_pokemons)
    
    pokemon_escolhido = f"https://pokeapi.co/api/v2/pokemon/{id_aleatorio}"
    resposta_pokemon = requests.get(pokemon_escolhido)


    if resposta_pokemon.status_code == 200:
        pokemon = resposta_pokemon.json()
        return {
            'nome': pokemon['name'].title(),
            'id': pokemon['id']
        }
    else:
        print(f"Erro ao buscar Pokémon ID {id_aleatorio}")
        return (f"Erro ao buscar Pokémon ID")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

fatos = [
    "O coração humano bombeia cerca de 7.500 litros de sangue por dia.",
    "Estudos mostram que abelhas aprendem a distinguir rostos específicos (como o do pesquisador) usando visão complexa, similar a reconhecimento facial básico.",
    "Vênus gira tão devagar que um dia (rotação) = 243 dias terrestres. Um ano (órbita) = 225 dias terrestres. Dia > ano!",
    "Guido van Rossum criou a linguagem python em 1989 assistindo Monty Python's Flying Circus, uma comédia britânica.",
    "Polvos têm três corações e sangue azul. 2 corações bombam sangue pros brânquios (oxigenação), 1 coração bombeia pros resto do corpo. Sangue azul por cobre (hemocianina), não ferro (hemoglobina).",
    "O menor osso humano é o estribo, que mede 3mm e se localiza no ouvido."
]

@bot.command()
async def fato(ctx):
    fato = random.choice(fatos)
    await ctx.send(fato)

@bot.command()
async def meme(ctx):
    with open(f'images/{acha_imagem()}', 'rb') as f:
        #Vamos armazenar o arquivo convertido da biblioteca do Discord nesta variável!
        picture = discord.File(f)
    # Podemos então enviar esse arquivo como um parâmetro
    await ctx.send(file=picture)

@bot.command()
async def pokemon(ctx):
      await ctx.send(pokemon2())



bot.run('Token')

bot.run('token')
