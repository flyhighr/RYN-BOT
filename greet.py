import discord
from discord.ext import commands
from PIL import Image,ImageDraw,ImageFont
import requests
from io import BytesIO 
import io

class WelcomeGoodbye(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(name="Life", type=discord.ActivityType.competing), status=discord.Status.idle)
        print(f'{self.bot.user.name} is now active!')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if guild.id != 1141252756150173718: 
            default_channel = guild.system_channel
            background_path = "/home/container/assets/Welcome!.png" 
            background_img = Image.open(background_path)
            avatar_url = str(member.avatar.url)
            draw = ImageDraw.Draw(background_img)
            font = ImageFont.truetype("/home/container/SukarBold.woff", 37)
            avatar_image = Image.open(requests.get(avatar_url, stream=True).raw)
            avatar_image = avatar_image.resize((161, 161))
            background_img.paste(avatar_image, (270, 103))
            draw.text((348, 324), f"{member.display_name}", fill=(0,0,0), font=font)

            background_img = background_img.resize((500,300 ))
            image_io = io.BytesIO()
            background_img.save(image_io, format='PNG')
            image_io.seek(0)
            
            file = discord.File(image_io, filename="welcome.png")
            if default_channel is not None:
                await default_channel.send(file=file)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        if guild.id != 1141252756150173718: 
            default_channel = guild.system_channel
            background_path = "/home/container/assets/Goodbye!.png" 
            background_img = Image.open(background_path)
            avatar_url = str(member.avatar.url)
            draw = ImageDraw.Draw(background_img)
            font = ImageFont.truetype("/home/container/SukarBold.woff", 37)
            avatar_image = Image.open(requests.get(avatar_url, stream=True).raw)
            avatar_image = avatar_image.resize((161, 161))
            background_img.paste(avatar_image, (270, 103))
            draw.text((348, 324), f"{member.display_name}", fill=(0,0,0), font=font)

            background_img = background_img.resize((500,300 ))
            image_io = io.BytesIO()
            background_img.save(image_io, format='PNG')
            image_io.seek(0)
            
            file = discord.File(image_io, filename="goodbye.png")
            if default_channel is not None:
                await default_channel.send(file=file)
    
