import discord
from discord.ext import commands, tasks
import json
import asyncio

# 🛠️ Configuration

TOKEN = "TON_TOKEN_ICI"  # Remplace par ton vrai token
GUILD_ID = 123456789012345678  # Remplace par l'ID de ton serveur
OBJECTIVE_CHANNEL_ID = 123456789012345678  # ID du salon d'engagement
VALIDATION_CHANNEL_ID = 123456789012345678  # ID du salon de validation
POWER_ELITE_CHANNEL_ID = 123456789012345678  # ID du salon privé des Power Élite
ROLE_POWER_GUERRIER = 123456789012345678  # ID du rôle Power Guerrier
ROLE_POWER_ELITE = 123456789012345678  # ID du rôle Power Élite

ENGAGEMENT_EMOJI = "⚔️"  # Emoji engagement
VALIDATION_EMOJI = "✅"  # Emoji validation
EMOJI_POWER_GUERRIER = "🛡️"
EMOJI_POWER_ELITE = "⚔️"

# 📂 Chargement des données d'engagement

try:
    with open("engagements.json", "r") as file:
        engagements = json.load(file)
except FileNotFoundError:
engagements = {}
with open("engagements.json", "w") as file:
json.dump({}, file)

# 🔧 Définition des permissions

intents = discord.Intents.default()
intents.message_content = True  # Activation de la lecture des messages
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 🔹 Sauvegarde des engagements

def save_engagements():
with open("engagements.json", "w") as file:
json.dump(engagements, file)

# 📌 Événement : engagement des membres (⚔️)

@bot.event
async def on_raw_reaction_add(payload):
if payload.channel_id == OBJECTIVE_CHANNEL_ID and [payload.emoji.name](http://payload.emoji.name/) == ENGAGEMENT_EMOJI:
guild = bot.get_guild(GUILD_ID)
member = guild.get_member(payload.user_id)
if member:
if str([member.id](http://member.id/)) not in engagements:
engagements[str([member.id](http://member.id/))] = {"weeks_validated": 0, "engaged": True}
else:
engagements[str([member.id](http://member.id/))]["engaged"] = True
save_engagements()
await member.send(f"✅ Tu t'es engagé(e) pour cette semaine dans {[guild.name](http://guild.name/)} !")

# 📌 Événement : validation des objectifs (✅)

@bot.event
async def on_message(message):
if [message.channel.id](http://message.channel.id/) == VALIDATION_CHANNEL_ID and VALIDATION_EMOJI in message.content:
member = message.author
if str([member.id](http://member.id/)) in engagements and engagements[str([member.id](http://member.id/))]["engaged"]:
engagements[str([member.id](http://member.id/))]["weeks_validated"] += 1
engagements[str([member.id](http://member.id/))]["engaged"] = False  # Réinitialisation pour la semaine suivante
save_engagements()

```
        # 🔹 Attribution des rôles
        guild = bot.get_guild(GUILD_ID)
        role_power_guerrier = guild.get_role(ROLE_POWER_GUERRIER)
        role_power_elite = guild.get_role(ROLE_POWER_ELITE)
        power_elite_channel = bot.get_channel(POWER_ELITE_CHANNEL_ID)

        if engagements[str(member.id)]["weeks_validated"] == 4:
            await member.add_roles(role_power_guerrier)
            await message.channel.send(f"{EMOJI_POWER_GUERRIER} {member.mention} a atteint **4 semaines** et devient un **Power Guerrier** !")

        elif engagements[str(member.id)]["weeks_validated"] == 12:
            await member.add_roles(role_power_elite)
            await power_elite_channel.set_permissions(member, read_messages=True)
            await message.channel.send(f"{EMOJI_POWER_ELITE} {member.mention} a atteint **12 semaines** et devient un **Power Élite** ! 🎉")

```

# 🕒 Tâche automatique : envoyer l’objectif chaque dimanche à 14h

@tasks.loop(hours=168)  # Toutes les semaines
async def send_weekly_objective():
channel = bot.get_channel(OBJECTIVE_CHANNEL_ID)
if channel:
await channel.send(f"🚀 **Nouvel Objectif de la Semaine !**\nRéagissez avec {ENGAGEMENT_EMOJI} pour vous engager !")

@send_weekly_objective.before_loop
async def before_weekly_objective():
await bot.wait_until_ready()

send_weekly_objective.start()

# 🚀 Lancement du bot

bot.run(TOKEN)




       
