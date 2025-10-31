import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# ===== CONFIGURAÇÃO =====
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ===== ON READY =====
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    # Carrega o módulo de anúncios
    await bot.load_extension("anuncio")
    print("✅ Anúncio carregado e agendado!")
# Carrega o módulo de sorteio
    await bot.load_extension("sorteio")
    await bot.tree.sync()
    print("✅ Sorteio carregado e comandos / sincronizados!")

# ===== RODA O BOT =====
bot.run(TOKEN)
