import discord
from discord.ext import commands
from config import TOKEN

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Бот запущен как {bot.user}")

# KICK
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Без причины"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.mention} кикнут. Причина: {reason}")

# BAN
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Без причины"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.mention} забанен. Причина: {reason}")

# MUTE
@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, send_messages=False, speak=False)
    await member.add_roles(role)
    await ctx.send(f"🔇 {member.mention} замучен")

# UNMUTE
@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if role:
        await member.remove_roles(role)
        await ctx.send(f"🔊 {member.mention} размучен")
    else:
        await ctx.send("❌ Роль Muted не найдена")

# ROLE
@bot.command()
@commands.has_permissions(manage_roles=True)
async def role(ctx, member: discord.Member, *, role_name):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        await ctx.send(f"✅ Роль {role_name} выдана {member.mention}")
    else:
        await ctx.send("❌ Такой роли нет")

bot.run(TOKEN)