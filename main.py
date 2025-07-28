import os
import discord
from discord import app_commands
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True  # szükséges az üzenetek olvasásához

bot = commands.Bot(command_prefix="!", intents=intents)

# Csatornák, ahol automatikusan reagálunk
CHANNEL_IDS = [1397602383764262982, 1397602385244717187]  # ide írd a csatorna ID-kat számként

# Az emoji, amivel minden üzenetre reagálunk automatikusan
AUTO_EMOJI = {
    1397602383764262982: "<a:whiteheart:1397855818543665303>",  # 1. channel fix emoji
    1397602385244717187: "<a:Legit:1399098372224323604>"  # 2. channelhez még nincs fix emoji, random lesz
}


class React(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash parancs: /react channel message_id emoji
    @app_commands.command(name="react", description="Reagálj egy üzenetre emoji-val")
    @app_commands.describe(
        channel="A csatorna, ahol az üzenet van",
        message_id="Az üzenet ID-je, amire reagálni akarsz",
        emoji="Az emoji amit rá szeretnél rakni"
    )
    async def react(self, interaction: discord.Interaction, channel: discord.TextChannel, message_id: str, emoji: str):
        try:
            message = await channel.fetch_message(int(message_id))
        except discord.NotFound:
            await interaction.response.send_message("Nem találtam az üzenetet!", ephemeral=True)
            return
        except discord.Forbidden:
            await interaction.response.send_message("Nincs jogosultságom az üzenethez!", ephemeral=True)
            return
        except Exception as e:
            await interaction.response.send_message(f"Hiba történt: {e}", ephemeral=True)
            return

        try:
            await message.add_reaction(emoji)
            await interaction.response.send_message(f"Sikeresen reagáltam az üzenetre ezzel: {emoji}", ephemeral=True)
        except discord.HTTPException:
            await interaction.response.send_message("Nem tudtam hozzáadni a reakciót. Lehet, hogy az emoji nem érvényes vagy nincs engedélyem.", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Bejelentkezve: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Szinkronizált slash parancsok: {len(synced)}")
    except Exception as e:
        print(f"Hiba a slash parancs szinkronizálásakor: {e}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id in CHANNEL_IDS:
        try:
            await message.add_reaction(AUTO_EMOJI)
        except Exception as e:
            print(f"Hiba az automatikus reakciónál: {e}")
    await bot.process_commands(message)  # nagyon fontos, hogy a parancsokat is kezelje!

async def main():
    async with bot:
        await bot.add_cog(React(bot))
        await bot.start(os.getenv("DISCORD_TOKEN"))  # token most már környezeti változóból jön

asyncio.run(main())
intents = discord.Intents.default()
intents.message_content = True