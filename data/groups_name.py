from random import seed, randrange
from datetime import datetime
import discord

DUO = [
    'C-3PO & R2-D2',
    'Harry & Lloy',
    'Batman & Robin ',
    'Will & Carlton',
    'Michael & Kitt',
    'MR Burns & Smithers',
    'Mario & Luigi',
    'Starsky & Hutch',
    'Harold & Kumar',
    'Astérix & Obélix',
    'Dupond & Dupont ',
    'Spirou & Fantasio',
    'Tintin & Milou',
    'Olive & Tom',
    'Satanas & Diabolo',
    'Tic & Tac',
    'Titi & Grosminet',
    'Timon & Pumbaa',
    'Tom & Jerry',
    'Minux & Cortex ',
    'Ratchet & Clank',
    'MARTY & DOC',
    'Han Solo & Chewbacca',
    'Goku & Vegeta',
    'Woody & Buzz',
    'Itchy & Scratchy',
    'Sam & Frodon',
    'Boule & Bill',
    'Lilo & Stitch',
    'Rox & Rouky',
    'Laurel & Hardy'

]

QUATUOR = [
    'Les 4 fantastiques',
    'Adibou & Les 3 petits chats',
    'Ghostbusters',
    'Les tortues ninja',
    'Cartman, Stan, Kenny & Kyle',
    'Les Daltons',
    'Les Teletubbies',
    'Les power rangers',
    "Les Beatles"
]

OCTO = [
    "Les carottes sont qu'huit",
    "Les 8 rennes du père noël",
    "L'octet",
    "Les 8 chevrons SG1",
    "Les 8 bits"
]

GROUPS_NAMES = {
    2: DUO,
    4: QUATUOR,
    8: OCTO
}


def random_name(size):
    names = GROUPS_NAMES[size]
    seed(datetime.now())
    nb = randrange(0, len(names))
    return names[nb]


''' Generate a random name from the lists but verify if it's not already taken'''
# TODO : lorsque tous les noms sont utilisés : boucle infinie à régler
def free_random_name(size, guild: discord.guild):
    new_name = None
    channels = guild.voice_channels
    while new_name is None or new_name in channels:
        new_name = random_name(size)
    return new_name
