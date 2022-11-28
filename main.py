#import
#https://discord.com/api/oauth2/authorize?client_id=1005476959591088179&permissions=8&scope=bot%20applications.commands
import discord,os,random,discord_slash,datetime
from Data.database_handler import DatabaseHandler
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option,create_choice
from discord.utils import get
from discord.ext import commands,tasks
intents = discord.Intents().default()
intents.members = True
bot = commands.Bot(command_prefix="!", description="bot test")
slash = SlashCommand(bot,sync_commands=True)
database_handler = DatabaseHandler("database.db")
print("starting...")

#----------------------------------------------
#------------------commandes--------------------
#dev db test tempmute
async def get_muted_role(guild : discord.Guild) -> discord.Role:
  role = get(guild.roles,name = "Muted")
  if role is not None:
    return role
  else:
    permissions = discord.Permissions(send_messages=False,)
    await guild.create_role(name = "Muted",permissions = permissions)
  return role

@bot.command()
async def mute(ctx, member : discord.Member, seconds : int):
	muted_role = await get_muted_role(ctx.guild)
	database_handler.add_tempmute(member.id, ctx.guild.id, datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds))
	await member.add_roles(muted_role)
	await ctx.send(f"{member.mention} a été muté ! 🎙")

@tasks.loop(minutes=1)
async def check_for_unmute():
	for guild in bot.guilds:
		active_tempmute = database_handler.active_tempmute_to_revoke(guild.id)
		if len(active_tempmute) > 0:
			muted_role = await get_muted_role(guild)
			for row in active_tempmute:
				member = guild.get_member(row["user_id"])
				database_handler.revoke_tempmute(row["id"])
				await member.remove_roles(muted_role)
  
#dev embed
@slash.slash(name="embed",description="NONE")
async def embed(ctx):
 embed = discord.Embed(title="**test**",description="cc")
 embed.set_thumbnail(url="https://saintebible.com/thumbatlas/philippi.jpg")
 await ctx.send(embed = embed)
 
  

#random guild id ne sert que a faire fonctioner sur 1 serv
@slash.slash(name="nombre_aleatoire",description="choisis un nombre aleatoire",options = [ 
create_option(name="tricher",description="Donne toujour le meme nombre",option_type = 3,required = True,choices=[
  create_choice(name = "Oui",value="y"),
  create_choice(name="Non", value="n")
]),
create_option(name="nombre_minimal",description="nombre minimal que le de va mettre",option_type = 4,required = False),
create_option(name="nombre_maximal",description="nombre maximal que le de va mettre",option_type = 4,required = False),
])
async def jsp(ctx,tricher,nombre_minimal=1,nombre_maximal=6):
  await ctx.send(f"Je lance le de :game_die: ...(chiffre entre **{nombre_minimal}** et **{nombre_maximal}**)")
  num = random.randint(nombre_minimal, nombre_maximal)
  if tricher=="y":
    await ctx.send(f"C'est pas bien de **tricher** ! :nerd:",hidden=True)
    num = 5
  await ctx.send(f":game_die: Le nombre est : **{num}** :game_die:")

#cc
@bot.command()
async def coucou(ctx):
    await ctx.send("coucou !")
@slash.slash(name="ephemeral",description="")
async def ephameral(ctx):
  await ctx.send("text", hidden=True)

#info
@bot.command()
async def serverInfo(ctx):
    server = ctx.guild
    textchannel_count = len(server.text_channels)
    vocchannel_count = len(server.voice_channels)
    description = server.description
    membres_count = server.member_count
    messages = f"le serveur **{server}** a **{membres_count}** membre :boy: :woman:. \n **{vocchannel_count}**  :loud_sound: salons vocaux et **{textchannel_count}** :book: salons textuels.  \n La description est {description}"
    await ctx.send(messages)


#dire du texte
@bot.command()
@commands.has_any_role("testeur officiel", "dev")
async def say(ctx, *texte):
    try:
        txt = " ".join(texte)
        texte = f"{ctx.message.author} veux que je dise ca:\n {txt}"
        await ctx.send(texte)
    except:
        await ctx.send("Tu n'as pas les permissions nescesaires")


#texte chinois
@bot.command()
@commands.has_any_role("testeur officiel", "dev")
async def chinois(ctx, *texte):
    try:
        chinois = "丹书匚刀巳下呂廾工丿片乚爪冂口尸Q尺丂丁凵V山乂Y乙"
        chinoistext = []
        for word in texte:
            for char in word:
                if char.isalpha():
                    index = ord(char) - ord("a")
                    transforme = chinois[index]
                    chinoistext.append(transforme)
                else:
                    chinoistext.append(char)
            chinoistext.append("   ")
        await ctx.send("".join(chinoistext))
    except:
        await ctx.send(
            "Tu n'as pas les permissions nescesaires **OU** il manque le texte a dire"
        )


#clear
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, nombre: int):
    await ctx.channel.purge(limit=nombre + 1)
    await ctx.send(f"**{nombre}** messages ont été supprimés")

#clear all
@bot.command()
@commands.has_any_role("testeur officiel", "dev")
async def clearall(ctx,):
  c = 1000000000
  await ctx.channel.purge(limit = c+1)
  await ctx.send(f"**TOUT** les messages ont été supprimés")
  

#kick
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason=reason)
    await ctx.send(
        f"**{user}** à été **kick** pour la raison suivante : {reason}")


#ban
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.ban(user, reason=reason)
    if reason == "":
        await ctx.send(f"**{user}** a ete **bannis**")
    else:
        await ctx.send(
            f"**{user}** a ete **bannis** pour la raison suivante : **{reason}**"
        )


#unban
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user, *reason):
    reason = " ".join(reason)
    userName, userId = user.split("#")
    bannedUsers = await ctx.guild.bans()
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userId:
            await ctx.guild.unban(i.user, reason=reason)
            await ctx.send(
                f"**{user}** à été **debannis** pour la raison suivante : {reason}."
            )
            return
    await ctx.send(f"Oups. on dirais que  **{user}** n'est **pas** bannis")


#cuisiner
@bot.command()
async def cuisiner(ctx):
    await ctx.send(f" {ctx.author.mention} on vous cuisine quoi ? Tout est **gratuit** !!")

    def checkMessage(message):
        return message.author == ctx.message.author and ctx.message.channel == message.channel

    try:
        recette = await bot.wait_for("message", timeout=10, check=checkMessage)
    except:
        await ctx.send(":watch: **temps ecoulé!!**")
        return
    message = await ctx.send(
        f' {ctx.author.mention} recapitulatif de la commande : **{recette.content}** pour commander reagis "✅"sinon reagis "❌"'
    )
    await message.add_reaction("✅")
    await message.add_reaction("❌")

    def checkEmoji(reaction, user):
        return ctx.message.author == user and message.id == reaction.message.id and (
            str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")

    try:
        reaction, user = await bot.wait_for("reaction_add",
                                            timeout=10,
                                            check=checkEmoji)
        if reaction.emoji == "✅":
            await ctx.send(
                f"Roger!!! tu me fais des **{recette.content}** pour la 5! ")
        else:
            await ctx.send(
                f" {ctx.author.mention} **Ok. on annule 😟** *tu peux recommencer si tu veux* :wink:")
    except:
        await ctx.send(":watch: temps **ecoulé!!**")

#mp
@bot.command()
@commands.bot_has_permissions(administrator=True)
async def mp(ctx,user : discord.User,*message):
 try:
  channel = await user.create_dm()
  message = " ".join(message)
  await channel.send(message)
  await ctx.send("message envoyé")
 except:
   await ctx.send("l'utilisateur n'a pas été trouvé")

@bot.event
async def on_ready():
    check_for_unmute.start
    print("started!")
    print("bot ready !")
    await bot.change_presence(activity=discord.Game(name="make your server awesone !"))
try:
  bot.run(os.environ["token"])
except discord.errors.HTTPException:
  print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
  os.system('kill 1')
  os.system("python restarter.py")