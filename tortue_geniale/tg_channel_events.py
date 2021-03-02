import discord
import asyncio
import re
import logging
from data.groups_name import free_random_name

logging.basicConfig(level=logging.INFO)
client = discord.Client()


class ClientEvents(discord.Client):
    '''
    Classe initialization
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def my_background_task(self):
        await self.wait_until_ready()
        counter = 0
        channel = self.get_channel(1234567)  # channel ID goes here
        while not self.is_closed():
            counter += 1
            await channel.send(counter)
            await asyncio.sleep(60)  # task runs every 60 seconds

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    ''' ############### EVENTS ABOUT CHANNELS AND SERVERS MANAGEMENT ###############'''

    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
            await guild.system_channel.send(to_send)

    '''
        Permet la création et la suppression automatique de channels
    '''

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState,
                                    after: discord.VoiceState):

        await self.wait_until_ready()
        after_channel: discord.VoiceChannel = after.channel
        before_channel: discord.VoiceChannel = before.channel

        # We enter in a channel
        if type(after_channel) is discord.VoiceChannel:
            category: discord.CategoryChannel = after_channel.category
            guild: discord.guild = member.guild

            if "Escouade".lower() in str(category.name).lower() and (
                    "Créer channel").lower() == after_channel.name.lower():

                team_size = re.findall(r'\d+', category.name)
                if len(team_size) == 0:
                    return
                else:
                    team_size = int(re.findall(r'\d+', category.name)[0])
                print("Création nouveau Channel")

                new_name = free_random_name(team_size, guild)
                new_channel: discord.VoiceChannel = await guild.create_voice_channel(
                    new_name,
                    category=category,
                    user_limit=int(team_size))
                await member.move_to(new_channel)

        # If we quit a channel and no one else is in, deletion of the channel
        if type(before_channel) is discord.VoiceChannel \
                and ("Créer channel").lower() != before_channel.name.lower():
            if len(before_channel.members) == 0:
                await before_channel.delete(reason="Channel empty")

    ''' ############### EVENTS ABOUT REPLIES ON MESSAGE ###############'''

    @client.event
    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!hello'):
            await message.channel.send('Hello {0.author.mention} sur le serveur {1.guild}'.format(message, message))


class CommandsClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
            await guild.system_channel.send(to_send)

    async def on_message(message):
        if message.content.startswith('$greet'):
            channel = message.channel
            await channel.send('Say hello!')

            def check(m):
                return m.content == 'hello' and m.channel == channel

            msg = await client.wait_for('message', check=check)
            await channel.send('Hello {.author}!'.format(msg))
