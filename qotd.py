import discord
import random
import sqlite3
from discord.ext import commands, tasks

class QOTD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database_setup()
        self.qotd_task.start()
        self.question_count = 0
        self.servers_count = 8
        self.qotd_channel_id = 2112132

    def database_setup(self):
        conn = sqlite3.connect('qotd.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS question (question_id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT, author TEXT)')
        cursor.execute('CREATE TABLE IF NOT EXISTS user (user_id INTEGER PRIMARY KEY, channel_id INTEGER, server_name TEXT, role_id INTEGER)')
        conn.commit()
        conn.close()


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Qotd Cog was Added')
        self.database_setup()

    @commands.hybrid_command(name="addquestion", description="Add Questions For QOTD")
    async def addquestion(self, interaction:discord.Interaction, *, question):
        conn = sqlite3.connect('qotd.db')
        cursor = conn.cursor()
        
        

        while True:
            question_id = random.randint(10000, 99999)
            cursor.execute('SELECT question_id FROM question WHERE question_id = ?', (question_id,))
            existing_id = cursor.fetchone()
            if not existing_id:
                break
        nums =  self.servers_count
        
        cursor.execute('INSERT INTO question (question_id, question, author) VALUES (?, ?, ?)', (question_id, question, interaction.author.display_name))
        conn.commit()
        conn.close()
        embed = discord.Embed(description=f"<:spiderman_sunglasses8:1193976864448970762>Your Question Will Asked Randomly In One Of the {nums} Registered Servers", color=0xcffc03)
        embed.set_author(name="Registered Succesfully!",icon_url = "https://static-00.iconduck.com/assets.00/success-icon-512x512-qdg1isa0.png")
        embed.set_footer(text=f"Note Question ID: {question_id:05} : For Removing This Question")
        await interaction.reply(embed=embed)
        em = discord.Embed(description =f"Question Was Added To QOTD\nQuestion: {question}\nID: {question_id:05}",color=0x42f5d1)
        member = self.bot.get_user(1134467862703132683)
        await member.send(embed=em)
        

    @tasks.loop(hours=24) 
    async def qotd_task(self):
        conn = sqlite3.connect('qotd.db')
        cursor = conn.cursor()

        if self.get_questions_count() <= 1:
            cursor.execute('SELECT user_id FROM user')
            users = cursor.fetchall()
            conn.close()
            

            for user in users:
                user_id = user[0]
                member = self.bot.get_user(user_id)
                if member:
                    try:
                       embed= discord.Embed(title="Please add more questions For The QOTD",description="Only One Question Remainn",color=0xfc0303)
                       embed.set_author(name="Logs For QOTD - RYN",icon_url="https://png.pngtree.com/png-clipart/20190629/original/pngtree-vector-message-icon-png-image_4083513.jpg")
                       embed.set_footer(text="Tip: Add Atleast 2 New Questions To Avoid Getting This Notification in Days")
                       await member.send(embed=embed)
                    except discord.HTTPException:
                       pass 
            
        
        if self.qotd_channel_id:
            conn = sqlite3.connect('qotd.db')
            cursor = conn.cursor()
            self.question_count+= 1
            cursor.execute('SELECT DISTINCT server_name FROM user')
            servers = cursor.fetchall()

            for server_name in servers:
                server_name = server_name[0]

                cursor.execute('SELECT * FROM user WHERE server_name = ?', (server_name,))
                users_data = cursor.fetchall()

                for user_data in users_data:
                    if isinstance(user_data, tuple) and len(user_data) >= 4:
                        user_id, channel_id, server_name, role_id = user_data
                        channel = self.bot.get_channel(int(channel_id))

                        if channel:
                            cursor.execute('SELECT * FROM question')
                            question = cursor.fetchone()
   
                            if isinstance(question, tuple):
                                if len(question) >= 3:
                                    question_id, question_text , author = question[0], str(question[1]) , str(question[2])
                                    
                                    num = self.question_count
                                    role_mention = f'<@&{role_id}>'
                                    embed = discord.Embed(title=f"{question_text} <:Spiderman_Thonk19:1193539339716665496>", description=f"<:hhhhhhhhhhh:1193538231443140709> {role_mention} <:hhhhhhhhhhh:1193538231443140709>", color=0x593fb5)
                                    embed.set_author(name=f"Question Of the Day #️ {num}     PG-13", icon_url="https://i.pinimg.com/564x/c4/81/ca/c481caec77886e13117719aa539e7afa.jpg")
                                    embed.set_footer(text=f"Question author: {author}\n╰┈➤ Answer In AOTD of {server_name}")
                                    await channel.send(f"{role_mention}")
                                    await channel.send(embed=embed)

                                    cursor.execute('DELETE FROM question WHERE question_id = ?', (question_id,))
                                    conn.commit()
                                else:
                                    print(f"No valid question fetched for server {server_name}")
                            else:
                                print(f"No valid question fetched for server {server_name}")
                    else:
                        print(f"Channel not found for user {user_id} in server {server_name}")
    
            conn.close()



    @commands.hybrid_command(name="setqotd", description="Set Question Of the Day For This Server")
    async def setqotd(self, interaction: discord.Interaction, channel: discord.TextChannel, role: discord.Role):
        if interaction.author.guild_permissions.administrator:
           
            guid_name = channel.guild.name
            self.qotd_channel_id = channel.id
            conn = sqlite3.connect('qotd.db')
            cursor = conn.cursor()
            self.servers_count += 1
    
            cursor.execute('SELECT user_id FROM user WHERE user_id = ?', (interaction.author.id,))
            existing_user = cursor.fetchone()
            if not existing_user:
                print(f"{channel.id}")
                print(f"{role.id}")
                print(f"{guid_name}")
                cursor.execute('''INSERT INTO user (user_id, channel_id , server_name ,role_id ) VALUES (?,?,?,?)''', (interaction.author.id, channel.id, guid_name, role.id))
                conn.commit()
                embed = discord.Embed(title=f"Success!", description=f"QOTD channel set to {channel.name}, \nRole to Mention: {role.name}", color=0xcffc03)
                embed.set_footer(text=f"To Remove The QOTD From {guid_name}  Use /removeqotd", icon_url="https://img.lovepik.com/png/20231013/Rubik-s-cube-game-toy-puzzle-fun-red-puzzle-toys_196092_wh1200.png")
                await interaction.reply(embed=embed)
            
            else:
                print("Usere With Existing Data Tried To SetQOTD")
                cursor.execute('SELECT server_name FROM user WHERE user_id = ?', (interaction.author.id,))
                guild = cursor.fetchone()
                guid_name = guild[0]
                embed1 = discord.Embed(description=f"Your Already Used This Command For {guid_name}",color=0xfc0303)
                embed1.set_author(name=f"{interaction.author.name}",url=f"{interaction.author.avatar.url}")
                embed1.set_footer(text="Please Remove Your Associated Server First")
                await interaction.reply(embed=embed1,ephemeral=True)
            conn.close()
    
           
        else:
            embed1= discord.Embed(description="Only User's With Administrator permissions Can Use This Command!")
            embed1.set_author(name="Restricted! ",icon_url="https://e7.pngegg.com/pngimages/10/205/png-clipart-computer-icons-error-information-error-angle-triangle-thumbnail.png")
            await interaction.reply(embed=embed1,ephemeral=True)

    def get_questions_count(self):
        conn = sqlite3.connect('qotd.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM question')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    

    def get_random_question(self):
        conn = sqlite3.connect('qotd.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM question ORDER BY RANDOM() LIMIT 1')
        question = cursor.fetchone()
        conn.close()
        return question
    @commands.hybrid_command(name="removequestion" , description = "Remove A Question For QOTD")
    async def removequestion(self, interaction:discord.Interaction, question_id: int):
        conn = sqlite3.connect('qotd.db')
        cursor = conn.cursor()
        cursor.execute('SELECT question_id, question FROM question WHERE question_id = ?', (question_id,))
        existing_question = cursor.fetchone()
        if existing_question:
            question_text = existing_question[1]
            cursor.execute('DELETE FROM question WHERE question_id = ?', (question_id,))
            conn.commit()
            embed = discord.Embed(title="Succesful Removal! ", description= f"Question with ID {question_id} `'{question_text}'` has been removed")
            await interaction.reply(embed=embed)
        else:
            embed= discord.Embed(description= f"Question With ID {question_id} does not Exist",color =0xFF0000)
            embed.set_author(name="🚫 Error!")
            await interaction.reply(embed=embed)
        conn.close()

    @commands.hybrid_command(name="removeqotd",description="Remove QOTD From Your Server")
    async def removeqotd(self, interaction:discord.Interaction, channel:discord.TextChannel):
        if interaction.author.guild_permissions.administrator:
            conn = sqlite3.connect('qotd.db')
            cursor = conn.cursor()
            server = channel.guild.name  
            cursor.execute('SELECT channel_id FROM user WHERE channel_id = ?', (channel.id,))
            existing_channel = cursor.fetchone()
            if existing_channel:    
               cursor.execute('DELETE FROM user WHERE channel_id = ?', (channel.id,))
               conn.commit()
               embed = discord.Embed(title=f"QOTD Was Removed From {server}",color=0x03dffc)
               embed.set_footer(text="If You Wanted To Change The Channel Use /setqotd Again")
               await interaction.reply(embed=embed)
            else:
               embed = discord.Embed(title="ERROR! ",description="QOTD Was Not Registered For Your Server",color=0x03dffc)
               embed.set_footer(text="I cannot Remove QOTD From Unregistered Servers")
               await interaction.reply(embed=embed)   

        else:
            embed1= discord.Embed(description="Only User's With Administrator permissions Can Use This Command!")
            embed1.set_author(name="Restricted! ",icon_url="https://e7.pngegg.com/pngimages/10/205/png-clipart-computer-icons-error-information-error-angle-triangle-thumbnail.png")
            await interaction.reply(embed=embed1,ephemeral=True)
        conn.close()

def setup(bot):
    bot.add_cog(QOTD(bot))
