import os
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()
import discord
from libsql_client import Value

import db

def val_to_date(val: Value) -> datetime:
    return datetime.fromtimestamp(int(str(val)) / 1000.0)


Context = discord.commands.context.ApplicationContext

bot = discord.Bot()
goals = bot.create_group("goals", "Make and maintain goals")

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@goals.command()
async def create(ctx: Context, goal: discord.SlashCommandOptionType.string): # type: ignore
    success = db.create_goal(ctx.user.id, goal)
    if success:
        await ctx.respond("Successfully created your goal!")
    else:
        await ctx.respond("Unable to create your goal.")


@goals.command(name="list", description="Get your goals")
async def glist(ctx: Context):
    rows, _ = db.list_goals(ctx.user.id)
    embed = discord.Embed(title=f"{ctx.user.name}'s Goals", color=discord.Color.teal())
    for i, row in enumerate(rows):
        embed.add_field(name=f"Goal {i + 1}", value=str(row[0]))

    await ctx.respond(f"", embed=embed)


@goals.command(name="info", description="Get more information about a specific goal")
async def ginfo(ctx: Context, goal_num: discord.SlashCommandOptionType.integer): # type: ignore
    rows, _ = db.list_goals(ctx.user.id)
    if len(rows) == 0:
        await ctx.respond("You have no goals. Add one using `/goals create`!")
        return
    elif goal_num < 1 or goal_num > len(rows):
        await ctx.respond("Invalid goal number!")
        return

    dt = datetime.now()
    row = rows[goal_num - 1]
    current_streak_start = val_to_date(row[3])
    current_streak = dt.date() - current_streak_start.date()
    embed = discord.Embed(title=f"Goal {goal_num}: {row[0]} :fire: {current_streak.days} {'day' if current_streak.days == 1 else 'days' }", color=discord.Color.teal())

    if row[2]:
        longest_streak_start = val_to_date(row[1])
        longest_streak_end = val_to_date(row[2])
        longest_streak = longest_streak_end.date() - longest_streak_start.date()
        longest_streak_str = f"{longest_streak_start.date().strftime('%x')} - {longest_streak_end.date().strftime('%x') if longest_streak_end else dt.date().strftime('%x')}\n({longest_streak.days} days)"
        embed.add_field(name="Longest Streak", value=longest_streak_str)

    current_streak_start = val_to_date(row[3])
    current_streak = dt.date() - current_streak_start.date()
    current_streak_str = f"{current_streak_start.date().strftime('%x')} - {dt.date().strftime('%x')}"
    embed.add_field(name="Current Streak", value=current_streak_str)

    created_at = val_to_date(row[4])
    embed.add_field(name="Created On", value=created_at.date().strftime("%x"))
    prompt_at = val_to_date(row[5])
    embed.add_field(name="Remind At", value=prompt_at.time().strftime("%I:%M %p"))

    await ctx.respond("", embed=embed)


bot.run(os.getenv("DISCORD_TOKEN")) # run the bot with the token
db.close()

