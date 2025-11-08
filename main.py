import os
import random
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

NFL_PLAYERS = [
    # --- 125+ player list ---
    "Patrick Mahomes", "Josh Allen", "Joe Burrow", "Lamar Jackson", "Justin Herbert",
    "Jalen Hurts", "Dak Prescott", "Aaron Rodgers", "Tua Tagovailoa", "Trevor Lawrence",
    "C.J. Stroud", "Brock Purdy", "Kirk Cousins", "Jared Goff", "Jordan Love", "Derek Carr",
    "Matthew Stafford", "Deshaun Watson", "Kyler Murray", "Baker Mayfield", "Geno Smith",
    "Mac Jones", "Russell Wilson", "Justin Fields", "Sam Howell", "Daniel Jones",
    "Anthony Richardson", "Will Levis", "Jimmy Garoppolo", "Kenny Pickett",
    "Christian McCaffrey", "Derrick Henry", "Saquon Barkley", "Nick Chubb", "Josh Jacobs",
    "Jonathan Taylor", "Bijan Robinson", "Austin Ekeler", "Alvin Kamara", "Tony Pollard",
    "Joe Mixon", "Aaron Jones", "Kenneth Walker III", "Rachaad White", "Breece Hall",
    "Najee Harris", "Isiah Pacheco", "James Cook", "Brian Robinson Jr.", "David Montgomery",
    "Jahmyr Gibbs", "Raheem Mostert", "De’Von Achane", "Miles Sanders", "Kareem Hunt",
    "Dameon Pierce", "Tyreek Hill", "Justin Jefferson", "Ja'Marr Chase", "A.J. Brown",
    "Stefon Diggs", "CeeDee Lamb", "Amon-Ra St. Brown", "Deebo Samuel", "Brandon Aiyuk",
    "Terry McLaurin", "DK Metcalf", "Chris Olave", "Garrett Wilson", "Mike Evans",
    "Davante Adams", "Jaylen Waddle", "Amari Cooper", "DeAndre Hopkins", "Keenan Allen",
    "DJ Moore", "Drake London", "Christian Kirk", "Calvin Ridley", "Tyler Lockett",
    "George Pickens", "Nico Collins", "Michael Pittman Jr.", "Courtland Sutton",
    "Marquise Brown", "Tank Dell", "Zay Flowers", "Puka Nacua", "Cooper Kupp",
    "Tee Higgins", "Travis Kelce", "George Kittle", "Mark Andrews", "T.J. Hockenson",
    "Sam LaPorta", "Kyle Pitts", "Darren Waller", "Dallas Goedert", "Evan Engram",
    "Dalton Schultz", "Cole Kmet", "Pat Freiermuth", "Jake Ferguson", "Micah Parsons",
    "Nick Bosa", "Myles Garrett", "T.J. Watt", "Maxx Crosby", "Aaron Donald", "Chris Jones",
    "Quinnen Williams", "Fred Warner", "Roquan Smith", "Bobby Wagner", "Sauce Gardner",
    "Jalen Ramsey", "Patrick Surtain II", "Derwin James", "Minkah Fitzpatrick",
    "Darius Slay", "L’Jarius Sneed", "Tariq Woolen", "Matthew Judon", "Haason Reddick",
    "Joey Bosa", "Danielle Hunter", "Brian Burns", "Aidan Hutchinson", "Jordan Poyer",
    "Tremaine Edmunds", "Dexter Lawrence", "Khalil Mack", "Chandler Jones",
    "Jeffery Simmons", "Justin Tucker", "Harrison Butker", "Evan McPherson",
    "Daniel Carlson", "Younghoe Koo", "Jake Elliott", "Tyler Bass", "Tom Brady",
    "Peyton Manning", "Drew Brees", "Brett Favre", "Ray Lewis", "Lawrence Taylor",
    "Jerry Rice", "Randy Moss", "Barry Sanders", "Emmitt Smith", "Deion Sanders",
    "Troy Polamalu", "Reggie White", "Ed Reed", "Joe Montana"
]

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        await bot.tree.sync()
        print("Slash commands synced.")
    except Exception as e:
        print(e)

@bot.tree.command(name="startimposter", description="Start an imposter game with 2–10 players.")
@app_commands.describe(players="Mention all players (2–10 total)")
async def startimposter(interaction: discord.Interaction, players: str):
    mentioned = [m for m in interaction.guild.members if f"<@{m.id}>" in players or f"<@!{m.id}>" in players]
    if len(mentioned) < 2 or len(mentioned) > 10:
        await interaction.response.send_message("❌ Include between 2–10 players.", ephemeral=True)
        return

    imposter = random.choice(mentioned)
    insiders = [p for p in mentioned if p != imposter]
    athlete = random.choice(NFL_PLAYERS)

    failed = []
    for insider in insiders:
        try:
            await insider.send(f"🏈 You are an **Insider**. The athlete is **{athlete}**.")
        except discord.Forbidden:
            failed.append(insider.name)

    try:
        await imposter.send("🕵️ You are the **Imposter**. You do **NOT** know the athlete.")
    except discord.Forbidden:
        failed.append(imposter.name)

    msg = f"✅ Roles assigned to {len(mentioned)} players! Check your DMs."
    if failed:
        msg += f"\n⚠️ Couldn't DM: {', '.join(failed)} (they may have DMs closed)."

    await interaction.response.send_message(msg, ephemeral=True)

bot.run(TOKEN)
