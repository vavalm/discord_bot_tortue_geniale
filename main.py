from tortue_geniale.tg_channel_events import ClientEvents
import os

if __name__ == '__main__':
    client = ClientEvents()
    client.run(os.getenv('DISCORD_TG_KEY'))