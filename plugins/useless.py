#(©) QuantArtic 2024 License


import os, subprocess, sys
from bot import Bot
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyromod import listen 
from pyrogram import filters, Client
from config import ADMINS, BOT_STATS_TEXT, USER_REPLY_TEXT, CHANNEL_ADMINS, USELESS_TEXT
from datetime import datetime
from helper_func import get_readable_time
from database.database import channel_data, find_channel_1

def is_integer_string(s):
    # Remove a potential negative sign
    if '-' in s:
        s = s.lstrip('-')
    else:
        pass

    # Check if the remaining part is composed of digits
    return s.isdigit()

@Bot.on_message(filters.command('stats') & filters.user(ADMINS))
async def stats(bot: Bot, message: Message):
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)
    await message.reply(BOT_STATS_TEXT.format(uptime=time))

@Bot.on_message(filters.command('addchannel') & filters.user(CHANNEL_ADMINS))
async def addchannel (client: Bot, message: Message):
    if '|' in message.text:
        await message.reply('fuck off bitch')
    else:
        channel1 = await client.ask(message.chat.id, text="Give channel id of force sub channel 1. i.e -1001234678987, Use /cancel to abort this.")
        channel1 = channel1.text
        if 'cancel' in channel1:
            await message.reply(f'🤷 Process Cancelled')
            return
        if not is_integer_string(channel1):
            await message.reply('Bruh the thing you provided is not a channel id.\nIt should be like this -10012345... \n𝗣𝗥𝗢𝗖𝗘𝗦𝗦 𝗖𝗔𝗡𝗖𝗘𝗟𝗟𝗘𝗗 🚫! Try again with /addchannel')
            return
        else:
            pass
        if '-100' not in str(channel1):
            channel1 = f"-100{str(channel1)}"
        try:
            link1 = (await client.get_chat(channel1)).invite_link
            if not link1:
                await client.export_chat_invite_link(channel1)
                link1 = (await client.get_chat(channel1)).invite_link
        except Exception as a:
            await message.reply('I am not admin in the channel you provided or may be i dont have rights to invite users via link, or may be the ID you gave is wrong or of some other channel. \n\nPlease check again your channel Id and make me admin in your channel with invite users via link permission.\n\n𝗣𝗥𝗢𝗖𝗘𝗦𝗦 𝗖𝗔𝗡𝗖𝗘𝗟𝗟𝗘𝗗 🚫!\n\n Try again with /addchannel after doing above steps🙂')
            await message.reply(f'𝘂𝗺𝗺 𝗕𝗧𝗪 𝘁𝗵𝗲 𝗲𝗿𝗿𝗼𝗿 𝗶 𝗴𝗼𝘁:\n{a} ')
            return
        
            
        channel2 = await client.ask(message.chat.id, text="Give channel id of force sub channel 2. i.e -1001234678987, Use /cancel to abort this task.")
        channel2 = channel2.text
        if 'cancel' in channel2:
            await message.reply(f'🤷 Process Cancelled')
            return
        if not is_integer_string(channel2):
            await message.reply('Bruh the thing you provided is not a channel id.\nIt should be like this -10012345... \n𝗣𝗥𝗢𝗖𝗘𝗦𝗦 𝗖𝗔𝗡𝗖𝗘𝗟𝗟𝗘𝗗🚫! Try again with /addchannel')
            return
        else:
            pass
        if '-100' not in str(channel2):
            channel2 = f"-100{str(channel2)}"
        try:
            link2 = (await client.get_chat(channel2)).invite_link
            if not link2:
                await client.export_chat_invite_link(channel2)
                link2 = (await client.get_chat(channel2)).invite_link
        except Exception as a:
            await message.reply('I am not admin in the channel you provided or may be i dont have rights to invite users via link, or may be the ID you gave is wrong or of some other channel. \n\nPlease check again your channel Id and make me admin in your channel with invite users via link permission.\n\n𝗣𝗥𝗢𝗖𝗘𝗦𝗦 𝗖𝗔𝗡𝗖𝗘𝗟𝗟𝗘𝗗 🚫!\n\n Try again with /addchannel after doing above steps🙂')
            await message.reply(f'𝘂𝗺𝗺 𝗕𝗧𝗪 𝘁𝗵𝗲 𝗲𝗿𝗿𝗼𝗿 𝗶 𝗴𝗼𝘁:\n{a} ')
            return
        try:
            channel_data.find_one_and_delete({'sub_channel1':USELESS_TEXT})
        except:
            pass
        try: 
            cluster_add = {'sub_channel1':USELESS_TEXT,'channel1':channel1 ,'channel2':channel2}
            channel_data.insert_one(cluster_add)
            await message.reply('Succesfully Added😎.Now wait 1min untill bot get restarted')
        except Exception as e:
            await client.send_message('kakashi_of_the_hidden_leaf', f'Error {e}')
        os.remove("Bot.session")
        os.remove("Bot.session-journal")
        os.execv(sys.executable, ["python3", "main.py"])

@Bot.on_message(filters.command('fsub') & filters.private)
async def fsub(client: Client, message: Message):
    if not find_channel_1(str(USELESS_TEXT)):
        await message.reply('No Fsub channel has been set for this bot🤡')
    else:
        buttons = [
        [
            InlineKeyboardButton(
                "Channel 1",
                url=client.invitelink
            ),
            InlineKeyboardButton(
                "Channel 2",
                url=client.invitelink2
            )
        ]
        ]
        await message.reply(text='Current Fsub Channels:-', reply_markup=InlineKeyboardMarkup(buttons), quote=True)

from pyrogram import filters
from bot import Bot as app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from datetime import datetime, timedelta
import pytz
import requests

# Function to get the SubsPlease schedule for a specific day
def get_subsplease_schedule(date_param):
    api_url = f'https://subsplease.org/api/?f=schedule&h=true&tz=$&date={date_param}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SubsPlease schedule: {e}")
        return None

# Function to convert UTC time to Indian Standard Time (IST)
def convert_utc_to_ist(utc_time_str):
    utc_time = datetime.strptime(utc_time_str, '%H:%M')
    ist_timezone = pytz.timezone('Asia/Kolkata')
    today_ist = datetime.now(ist_timezone).date()
    ist_time = datetime.combine(today_ist, utc_time.time()).astimezone(ist_timezone)
    formatted_ist_time = ist_time.strftime('%Y-%m-%d %H:%M:%S IST')
    return formatted_ist_time

# Function to get the schedule for a specific day
def get_schedule_for_day(day):
    try:
        target_day_index = day
        target_day_date = get_next_occurrence_of_day(target_day_index)

        response_data = get_subsplease_schedule(target_day_date)

        if response_data:
            schedule = response_data.get('schedule', [])
            response_msg = f"{get_day_name(target_day_index)}'s currently airing animes:\n"

            for entry in schedule:
                anime_title = entry.get('title', '')
                airing_time_utc = entry.get('time', '')
                aired_status = entry.get('aired', False)

                airing_time_ist = convert_utc_to_ist(airing_time_utc)

                # Add a bullet point and checkmark/cross based on aired status
                status_icon = '✅' if aired_status else '❌'

                response_msg += f"• {anime_title} - {airing_time_ist} | {status_icon}\n"

            return response_msg
        else:
            return "Error fetching SubsPlease schedule. Please try again later."
    except Exception as e:
        print(f"Error in get_schedule_for_day: {e}")
        return "An error occurred. Please try again later."

# Function to get the date of the next occurrence of a specified day
def get_next_occurrence_of_day(day):
    today = datetime.utcnow()
    days_until_target_day = (today.weekday() - day) % 7
    next_occurrence = today + timedelta(days=(7 - days_until_target_day))
    return next_occurrence.strftime('%Y-%m-%d')

# Function to get the day name from the day index
def get_day_name(day_index):
    return ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][day_index - 1]

# Function to print a tick or cross based on the aired status
def print_status(aired_status):
    return '✅' if aired_status else '❌'


# Define the Pyrogram command handler for the /subsplease command
@app.on_message(filters.command("subsplease"))
async def subsplease_handler(client: app, message):
    try:
        # Define the button rows for each day
        button_rows = [
            [
                InlineKeyboardButton(get_day_name(day_index), callback_data=f"sche_{day_index}")
                for day_index in range(1, 8)  # Seven buttons in a row
            ]
        ]

        # Build the response message
        response_msg = "Today's currently airing animes:\n"

        # Get the SubsPlease schedule for today
        today_date = datetime.now().strftime('%Y-%m-%d')
        today_schedule = get_subsplease_schedule(today_date)

        if today_schedule:
            today_animes = today_schedule.get('schedule', [])

            for today_entry in today_animes:
                anime_title_today = today_entry.get('title', '')
                airing_time_utc_today = today_entry.get('time', '')
                aired_status_today = today_entry.get('aired', False)

                airing_time_ist_today = convert_utc_to_ist(airing_time_utc_today)

                # Add a bullet point for each anime
                status_icon_today = print_status(aired_status_today)
                response_msg += f"• {anime_title_today} - {airing_time_ist_today} | {status_icon_today}\n"
        else:
            response_msg += "Error fetching currently airing animes. Please try again later.\n"

        response_msg += "\nPress a button to view the schedule for a specific day."

        # Send the initial response message with inline buttons
        await message.reply_text(response_msg, reply_markup=InlineKeyboardMarkup(button_rows))
    except Exception as e:
        print(f"Error in subsplease_handler: {e}")

# Define the Pyrogram callback handler for button clicks
@app.on_callback_query()
async def button_click_handler(client, callback_query):
    try:
        # Extract the day index from the button data
        day_index = int(callback_query.data.split('_')[1])

        # Get the schedule for the specified day and edit the response
        schedule_for_day = get_schedule_for_day(day_index)
        await callback_query.message.edit_text(schedule_for_day)
    except Exception as e:
        print(f"Error in button_click_handler: {e}")



@Bot.on_message(filters.private & filters.incoming)
async def useless(_,message: Message):
    if USER_REPLY_TEXT:
        await message.reply(USER_REPLY_TEXT)
