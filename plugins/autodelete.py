#(©) QuantArtic 2024 License


from pyrogram import Client, filters
from config import OWNER_ID, ADMINS
from bot import Bot as app
from database.database import autodelete_data as collection


# Function to check the auto delete setting
def get_auto_delete_setting():
    settings = collection.find_one({"_id": "autodelete"})
    if settings:
        return settings["enabled"]
    else:
        return False


# Function to get the delete time setting
def get_delete_time_setting():
    settings = collection.find_one({"_id": "deletetime"})
    if settings:
        return settings.get("time_in_seconds", 600)
    else:
        return 600  # Default value: 600 seconds (10 minutes)

# Command handler for /autodelete command
@app.on_message(filters.command("autodelete") & filters.user(ADMINS) & filters.private)
async def autodelete_command(client, message):
    args = message.text.split()
    if len(args) != 2 or args[1] not in ["on", "off"]:
        await message.reply_text("Usage: /autodelete [on/off]")
        return

    enabled = args[1] == "on"
    current_setting = get_auto_delete_setting()

    if enabled == current_setting:
        await message.reply_text(f"Auto delete is already {'enabled' if enabled else 'disabled'}.")
    else:
        collection.update_one({"_id": "autodelete"}, {"$set": {"enabled": enabled}}, upsert=True)
        await message.reply_text(f"Auto delete setting has been set to {'on' if enabled else 'off'}.")

@app.on_message(filters.command("setdeletetime") & filters.user(ADMINS) & filters.private)
async def deletetime_command(client, message):
    args = message.text.split()
    if len(args) == 1:
        await message.reply_text("Usage: /deletetime [time_in_seconds]")
        return

    try:
        time_in_seconds = int(args[1])
    except ValueError:
        await message.reply_text("Please provide a valid integer for the time.")
        return

    collection.update_one({"_id": "deletetime"}, {"$set": {"time_in_seconds": time_in_seconds}}, upsert=True)
    await message.reply_text(f"Auto delete time has been set to {time_in_seconds} seconds.")

# Command handler for /autodeletestatus command
@app.on_message(filters.command("autotdeletestatus"))
async def status_command(client, message):
    auto_delete_enabled = get_auto_delete_setting()
    auto_delete_time = get_delete_time_setting()
    
    if auto_delete_enabled:
        await message.reply_text(f"Auto delete is enabled. Files will be deleted after {auto_delete_time} seconds.")
    else:
        await message.reply_text("Auto delete is disabled.")



