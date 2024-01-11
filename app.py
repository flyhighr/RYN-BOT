import discord
from discord.ext import commands # Import the Slash cog
from qotd import QOTD
from greet import WelcomeGoodbye
from slash import Slash

class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix=".",intents=intents ,case_insensitive=True)
    async def on_ready(self):
        await bot.change_presence(activity=discord.Game(name="Life", type=discord.ActivityType.competing), status=discord.Status.idle)
        print(f"Logged in as {self.user}")
        qotd_cog = QOTD(bot)
        await self.add_cog(qotd_cog)
        greet = (WelcomeGoodbye(bot))
        await self.add_cog(greet)
        slash = (Slash(bot))
        await self.add_cog(slash)
        loaded_cogs = [cog for cog in bot.cogs]
        if loaded_cogs:
            print(f"{len(loaded_cogs)} cogs added: {', '.join(loaded_cogs)}")
        else:
            print("No cogs loaded.")
   

        await self.tree.sync()
intents = discord.Intents.all()
bot = Bot(intents=intents)




bot.run('MTE5MjA1OTg5MTg4MDMxMjg4Mw.GP0H4Q.Vky7w9jP5W9IembJZnk0nPy0n44xeeWxhEUIHo')
