import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.members = True  # Needed to fetch server members

bot = commands.Bot(command_prefix="!", intents=intents)


nfl_players = [
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

# Store current game
current_game = {
    "imposter": None,
    "athlete": None,
    "insiders": []
}

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands synced ({len(synced)})")
    except Exception as e:
        print(e)

# Start a new imposter game
@bot.tree.command(name="startimposter", description="Start an NFL Imposter game with 2–10 players.")
@discord.app_commands.describe(players="Mention 2–10 Discord members to play")
async def startimposter(interaction: discord.Interaction, players: str):
    # Split player input by spaces (plain names or mentions)
    player_names = players.split()
    
    # Match Discord members by username or mention
    mentioned = [m for m in interaction.guild.members if m.name in player_names or f"<@{m.id}>" in player_names or f"<@!{m.id}>" in player_names]
    
    if len(mentioned) < 2 or len(mentioned) > 10:
        await interaction.response.send_message("❌ Include between 2–10 players.", ephemeral=True)
        return
    
    # Pick random NFL player
    athlete = random.choice(nfl_players)
    
    # Pick imposter
    imposter = random.choice(mentioned)
    insiders = [m for m in mentioned if m != imposter]
    
    # DM players
    for insider in insiders:
        try:
            await insider.send(f"You're an insider! The NFL player is: **{athlete}**")
        except:
            await interaction.channel.send(f"⚠️ Couldn't DM {insider.display_name}.")
    
    try:
        await imposter.send(f"You're the IMPOSTER! Try to blend in while everyone else knows the NFL player.")
    except:
        await interaction.channel.send(f"⚠️ Couldn't DM {imposter.display_name}.")

    # Save game state
    current_game["imposter"] = imposter
    current_game["athlete"] = athlete
    current_game["insiders"] = insiders

    await interaction.response.send_message(f"🎮 Game started with {len(mentioned)} players! Check your DMs.", ephemeral=True)

# Reveal the imposter and NFL player
@bot.tree.command(name="reveal", description="Reveal the imposter and NFL player for the last game.")
async def reveal(interaction: discord.Interaction):
    if not current_game["imposter"] or not current_game["athlete"]:
        await interaction.response.send_message("❌ No game in progress to reveal.", ephemeral=True)
        return

    imposter_name = current_game["imposter"].display_name
    athlete_name = current_game["athlete"]

    await interaction.response.send_message(
        f"🏁 The round is over!\n"
        f"🕵️ Imposter: **{imposter_name}**\n"
        f"🏈 NFL Player: **{athlete_name}**"
    )

    # Reset game
    current_game["imposter"] = None
    current_game["athlete"] = None
    current_game["insiders"] = []

# Run the bot
TOKEN = "token"
bot.run(TOKEN)
