# sorteio.py
import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random
from typing import List, Dict, Any

# ====== CONFIGURAÇÃO POR SERVIDOR ======
# Substitua os IDs e URLs abaixo para cada servidor (até 8).
# Use inteiros para IDs (sem aspas). A imagem deve ser o link direto da imagem (copiar link da imagem).
SERVIDORES_CONFIG: Dict[int, Dict[str, Any]] = {
    # 🏰 Servidor 1
    1203791655321468928: {
        "cargos_iniciar": [1203793856592871504, 1410401933533122580, 1204544608286023741],
        "cargos_participar": [1418357273344086096],
        "imagem": "https://cdn.discordapp.com/attachments/1418038806690398300/1433256103092818020/ChatGPT_Image_29_de_out._de_2025_21_32_57.png?ex=69040743&is=6902b5c3&hm=24a818e0931efc5d552c1a025fd3c728a5c81c1e9536c0c94120f83ae7fab7a4&"
    },

    # 🏰 Servidor 2
    1398355798886715402: {
        "cargos_iniciar": [1399832535068049499, 1410374261234729130, 1399831878424330421],
        "cargos_participar": [1419834737534566531],
        "imagem": "https://cdn.discordapp.com/attachments/1409384719430455356/1433256982264938536/ChatGPT_Image_29_de_out._de_2025_21_32_52.png?ex=69040815&is=6902b695&hm=f6076c178dc6fed5430d98c1020346ca36c6f897bcd9500dd2e67afbe2b9839f&"
    },

    # 🏰 Servidor 3
    1408612825076731926: {
        "cargos_iniciar": [1408612825076731927, 1410056789285802116, 1408612825076731932],
        "cargos_participar": [1419846526477533286],
        "imagem": "https://cdn.discordapp.com/attachments/1409552933841932288/1433257587473776800/ChatGPT_Image_29_de_out._de_2025_21_32_50.png?ex=690408a5&is=6902b725&hm=857945d7ca89202bea25a19a65be511cd64a27b77c1f662534660f15f934beb4&"
    },

    # 🏰 Servidor 4
    1408987113835466824: {
        "cargos_iniciar": [1409659216687534141, 1410105389260996619, 1409657702262767656],
        "cargos_participar": [1433232426900914288],
        "imagem": "https://cdn.discordapp.com/attachments/1409661067545673818/1433260246721102005/ChatGPT_Image_29_de_out._de_2025_22_04_13.png?ex=69040b1f&is=6902b99f&hm=31efdf38b119ca07f4dbd664d7c2963ef2f358471c533c871f5793e4c749cd21&"
    },

    # 🏰 Servidor 5
    1408619437568950347: {
        "cargos_iniciar": [1426354312723955762, 1410051064111300708, 1433261105802645504],
        "cargos_participar": [1433261302423228447],
        "imagem": "https://cdn.discordapp.com/attachments/1415123237888856124/1433262858921185401/ChatGPT_Image_29_de_out._de_2025_21_32_54.png?ex=69040d8e&is=6902bc0e&hm=8f722232c99c3c4e5c22adfb188b1813c1298dca553033a7fa3a9ec7c3b1c591&"
    },

    # 🏰 Servidor 6 (adicione aqui)
    1361528458404167772: {  # Substitua pelo ID real
        "cargos_iniciar": [1362164105179562335, 1410374531758948392, 1362164282552484093],
        "cargos_participar": [1362164380342550631],
        "imagem": "https://cdn.discordapp.com/attachments/1407504455829688413/1433862682234191893/ChatGPT_Image_29_de_out._de_2025_21_32_48.png?ex=69063c2f&is=6904eaaf&hm=b1b96337fe31acc5cd2d73d833651fc2aa2cd16ea5b69a6094ee3b81fbb4138f&"
    }
}
# ====== FIM DA CONFIGURAÇÃO ======

class Sorteio(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _get_config_for_guild(self, guild: discord.Guild):
        return SERVIDORES_CONFIG.get(guild.id)

    def _has_iniciar_permission(self, member: discord.Member, cargos_iniciar: List[int]) -> bool:
        return any(role.id in cargos_iniciar for role in member.roles)

    def _member_has_participar(self, member: discord.Member, cargos_participar: List[int]) -> bool:
        return any(role.id in cargos_participar for role in member.roles)

    @app_commands.command(
        name="sorteio",
        description="Inicia um sorteio (apenas para servidores configurados)."
    )
    @app_commands.describe(
        tempo="Duração do sorteio (em segundos)",
        vencedores="Quantidade de ganhadores",
        premio="Qual é o prêmio?"
    )
    async def sorteio(
        self,
        interaction: discord.Interaction,
        tempo: int,
        vencedores: int,
        premio: str
    ):
        config = self._get_config_for_guild(interaction.guild)
        if not config:
            await interaction.response.send_message(
                "🚫 Este servidor não está configurado para sorteios.", ephemeral=True
            )
            return

        cargos_iniciar = config.get("cargos_iniciar", [])
        cargos_participar = config.get("cargos_participar", [])
        imagem_url = config.get("imagem")

        autor_member = interaction.user
        if not isinstance(autor_member, discord.Member):
            autor_member = interaction.guild.get_member(interaction.user.id)

        if not autor_member or not self._has_iniciar_permission(autor_member, cargos_iniciar):
            await interaction.response.send_message(
                "🚫 Você não tem permissão para iniciar o sorteio.", ephemeral=True
            )
            return

        await interaction.response.send_message("✅ Sorteio iniciado com sucesso!", ephemeral=True)

        embed = discord.Embed(
            title="🎉 SORTEIO DA REDENÇÃO ⚔️",
            description=(
                f"🔥 **Prêmio:** {premio}\n"
                f"⏳ **Duração:** {tempo} segundos\n"
                f"👑 **Vencedores:** {vencedores}\n\n"
                "Reaja com 🎉 para participar!\n"
                "Mostre sua sorte, guerreiro da RD!"
            ),
            color=discord.Color.red()
        )
        if imagem_url:
            embed.set_image(url=imagem_url)
        embed.set_footer(text="Sistema oficial de sorteios • RD BOT")

        msg = await interaction.channel.send(embed=embed)
        try:
            await msg.add_reaction("🎉")
        except Exception:
            await interaction.channel.send(
                "⚠️ Não consegui adicionar a reação automaticamente. Usuários precisam reagir manualmente com 🎉."
            )

        await asyncio.sleep(max(1, tempo))

        try:
            msg = await interaction.channel.fetch_message(msg.id)
        except Exception:
            await interaction.channel.send("⚠️ Não consegui recuperar a mensagem do sorteio.")
            return

        reacao = discord.utils.get(msg.reactions, emoji="🎉")
        if not reacao or reacao.count <= 1:
            await interaction.channel.send("⚠️ Ninguém participou do sorteio!")
            return

        participantes = []
        async for user in reacao.users():
            if user.bot:
                continue
            member = interaction.guild.get_member(user.id)
            if not member:
                try:
                    member = await interaction.guild.fetch_member(user.id)
                except Exception:
                    member = None
            if member and self._member_has_participar(member, cargos_participar):
                participantes.append(member)

        if not participantes:
            await interaction.channel.send("⚠️ Nenhum participante autorizado encontrado!")
            return

        winners = random.sample(participantes, min(vencedores, len(participantes)))
        winners_mentions = ", ".join(w.mention for w in winners)

        resultado = discord.Embed(
            title="🏆 SORTEIO ENCERRADO 🏆",
            description=f"🎁 **Prêmio:** {premio}\n🎉 **Vencedor(es):** {winners_mentions}",
            color=discord.Color.dark_red()
        )
        resultado.set_footer(text="Parabéns ao(s) vencedor(es)! ⚔️")

        await interaction.channel.send(embed=resultado)


async def setup(bot: commands.Bot):
    await bot.add_cog(Sorteio(bot))
