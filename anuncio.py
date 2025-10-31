import discord
from discord.ext import commands
import datetime, os, json, asyncio

CANAIS_ID = [
    1340435779947593832,
    1419837402721026058,
    1419844439538401331
]
HORARIO_ENVIO = 18  # horário de envio (horário de Brasília)
ARQUIVO_BACKUP = "enviados.json"
ARQUIVO_LOG = "log_envios.txt"

MENSAGENS_DIARIAS = {
    "2025-11-01": {"title": "🚀 RECRUTAMENTO EM MASSA!", "description": "Recrutamento aberto em massa."},
    "2025-11-02": {"title": "🔥 SISTEMA VIPS!", "description": "Sistema VIPs com recompensas."},
    "2025-11-03": {"title": "⚔️ XTREINO!", "description": "Novidades no Xtreino, evite faltas."},
    "2025-11-04": {"title": "🏹 METAS!", "description": "Pontue para subir no ranking."},
    "2025-11-05": {"title": "🛡️ REDENÇÃO SUL (RDS)!", "description": "Defesa da guilda Redenção Sul."},
    "2025-11-06": {"title": "💥 REDENÇÃO NORTE (RDN)!", "description": "Ataque da guilda Redenção Norte."},
    "2025-11-07": {"title": "🎯 CENTRAL RD!", "description": "Todos devem estar na Central RD."},
    "2025-11-08": {"title": "🏆 LINES!", "description": "Sistema de lines finalizado."},
    "2025-11-09": {"title": "⚡ INFRAÇÕES!", "description": "Infrações quando regras são violadas."},
    "2025-11-10": {"title": "🎉 FINAL!", "description": "RD aberta para todos os jogos!"}
}

def carregar_backup():
    if os.path.exists(ARQUIVO_BACKUP):
        try:
            with open(ARQUIVO_BACKUP, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def salvar_backup(dados):
    with open(ARQUIVO_BACKUP, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def logar(texto):
    data = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{data}] {texto}\n")

async def enviar_mensagem_diaria(bot):
    agora = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3)))
    data_hoje = agora.date().isoformat()
    enviados = carregar_backup()

    if data_hoje in MENSAGENS_DIARIAS and data_hoje not in enviados:
        info = MENSAGENS_DIARIAS[data_hoje]
        embed = discord.Embed(
            title=info["title"],
            description=info["description"],
            color=0xFF0000
        )
        embed.set_footer(text="Sistema oficial de anúncios • RD BOT")
        sucesso = 0
        for canal_id in CANAIS_ID:
            canal = bot.get_channel(canal_id)
            if canal:
                try:
                    await canal.send(embed=embed)
                    sucesso += 1
                except Exception as e:
                    logar(f"❌ Erro ao enviar para canal {canal_id}: {e}")
        enviados.append(data_hoje)
        salvar_backup(enviados)
        logar(f"✅ Mensagem de {data_hoje} enviada para {sucesso} canais.")
        print(f"✅ Mensagem de {data_hoje} enviada para {sucesso} canais.")
    else:
        logar(f"⚠️ Nenhuma mensagem programada ou já enviada para {data_hoje}.")
        print(f"⚠️ Nenhuma mensagem programada ou já enviada para {data_hoje}.")

# ===== COG =====
class Anuncio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.agendar_envio_diario())

    async def agendar_envio_diario(self):
        while True:
            agora = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3)))
            proximo_envio = agora.replace(hour=HORARIO_ENVIO, minute=0, second=0, microsecond=0)
            if agora >= proximo_envio:
                proximo_envio += datetime.timedelta(days=1)
            segundos_ate_envio = (proximo_envio - agora).total_seconds()
            print(f"⏳ Próximo envio em {segundos_ate_envio/3600:.2f} horas")
            await asyncio.sleep(segundos_ate_envio)
            await enviar_mensagem_diaria(self.bot)

async def setup(bot):
    await bot.add_cog(Anuncio(bot))
