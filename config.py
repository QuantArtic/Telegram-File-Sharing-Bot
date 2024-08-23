#(©) QuantArtic 2024 License



import os
import logging
from logging.handlers import RotatingFileHandler


USELESS_TEXT = os.environ.get("USELESS_TEXT", "1")
#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", ""))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "")

#Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-100"))

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "1435293433"))

#Port
PORT = os.environ.get("PORT", "8080")

#Database 
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://Complex:Complex@cluster0.e6wgtmq.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "Eru-chii")

#force sub channel id, if you want enable force sub
#FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1001569040317"))
#FORCE_SUB_CHANNEL = find_channel_1(USELESS_TEXT)
#SECOND_FORCE_SUB_CHANNEL = int(os.environ.get("SECOND_FORCE_SUB_CHANNEL", "-1001920913833"))
#SECOND_FORCE_SUB_CHANNEL = find_channel_2(USELESS_TEXT)

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "800"))

#start message
START_MSG = os.environ.get("START_MESSAGE", "Konnichiwa {first},\n\nI am pleased to inform you that I can provide you with anime files from your favorite series.\n\nTo access these files, please visit our repository at @Anime_Arsenal.\n\nYou will have the option to select the format of your choice, whether it be 720p, 1080p, or any other preference you may have.\n\nWe are here to cater to your anime needs with the utmost professionalism and quality.")
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "917790252 1435293433 1435293433 1476517140 1172340595 917790252 6622031162 1380685014").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")
        
try:
    CHANNEL_ADMINS=[]
    for x in (os.environ.get("CHANNEL_ADMINS", "917790252 1435293433 1858995207 6208943761").split()):
        CHANNEL_ADMINS.append(int(x))
except ValueError:
        raise Exception("Your channel Admins list does not contain valid integers.")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "<b>Hey {first}\n\nTo access these files you have to join our channel first.\n\nPlease subscribe to our channels through the buttons below and then tap on try again to get your files.</b>")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = False #if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = True #os.environ.get("DISABLE_CHANNEL_BUTTON", False) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "Hello super weeb! I am just a file share bot, please don't send any messages to me."

ADMINS.append(OWNER_ID)
ADMINS.extend(CHANNEL_ADMINS)
CHANNEL_ADMINS.append(OWNER_ID)
#ADMINS.append(917790252)

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
