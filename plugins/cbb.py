#(©) QuantArtic 2024 License


from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"Bot For - <a href=''>Anime Arsenal</a>\nMaster : <a href='https://t.me/TheGreninja'>Greninja</a>",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔒 Close", callback_data="close")
                    ]
                ]
            )
        )
    elif data == "admin":
        admin_commands_text = (
            "<b>☠️Admin Commands:</b>\n\n"
            "◆/adduser - Add user IDs to the database to get acces of bot\n\n"
            "◆/removeuser - Remove user IDs from the database to remove acces of bot\n\n"
            "◆/authusers - Get authorized user IDs and names\n\n"
            "◆/users - See the total number of users in the Bot\n\n"
            "◆/broadcast - Broadcast a message\n\n"
            "◆/addchannel - Change/set force sub in the bot\n\n"
            "◆/fsub - To check current Force sub channels.\n\n"
            "◆/autodelete - To enable auto delete of files sent by the bot\n\n"
            "◆/setdeletetime - Change/set auto delete time of bot.\n\n"
            "◆/autotdeletestatus - To check if autodelete is enabled or not with how much seconds.\n\n"
            "⚡𝗡𝗢𝗧𝗘:- 𝘖𝘯𝘭𝘺 𝘉𝘰𝘵 𝘢𝘶𝘵𝘩𝘰𝘳𝘪𝘻𝘦𝘥 𝘶𝘴𝘦𝘳𝘴 𝘤𝘢𝘯 𝘰𝘯𝘭𝘺 𝘶𝘴𝘦 𝘵𝘩𝘪𝘴 𝘢𝘣𝘰𝘷𝘦 𝘤𝘰𝘮𝘮𝘢𝘯ds"
        )
        await query.message.edit_text(
            text=admin_commands_text,
            #parse_mode="html"
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔒 Close", callback_data="close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
