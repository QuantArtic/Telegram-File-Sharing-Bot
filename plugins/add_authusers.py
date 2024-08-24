#(©) QuantArtic 2024 License


from pyrogram import Client, filters
from pyrogram.types import Message
from config import ADMINS, OWNER_ID
from bot import Bot as app
from database.database import auth_users as user_collection


async def is_authorized_user(_, __, message: Message):
    if message.from_user:
        user_id = message.from_user.id
        user_data = user_collection.find_one({})
    
        return user_data and 'user_ids' in user_data and user_id in user_data['user_ids']

    return False 

# Add userIDs to the database
@app.on_message(filters.command("adduser") & filters.user(ADMINS) & filters.private)
async def add_user_to_db(client, message):
    user_ids_to_add = message.text.split()[1:]  # Extract userIDs from the command
    user_ids_to_add = [int(user_id) for user_id in user_ids_to_add if user_id.isdigit()]  # Ensure they are integers

    if not user_ids_to_add:
        await message.reply_text("Invalid user IDs provided.")
        return

    user_data = user_collection.find_one({})
    existing_user_ids = user_data.get('user_ids', []) if user_data else []

    # Separate userIDs into already added and not added
    already_added_ids = [user_id for user_id in user_ids_to_add if user_id in existing_user_ids]
    new_user_ids = [user_id for user_id in user_ids_to_add if user_id not in existing_user_ids]

    if not user_data:
        # If the document doesn't exist, create a new one
        user_collection.insert_one({'user_ids': new_user_ids})
    else:
        pass


    # Add new userIDs to the database
    if new_user_ids:
        user_collection.update_one({}, {'$addToSet': {'user_ids': {'$each': new_user_ids}}})
        await message.reply_text(f"Added {len(new_user_ids)} new user(s) to the database.")

    # Reply with already added userIDs
    if already_added_ids:
        await message.reply_text(f"User IDs {', '.join(map(str, already_added_ids))} already in db and so ignored.")

    # Reply with the whole list of users finally added to the database
    final_user_list = user_collection.find_one({})['user_ids']
    await message.reply_text(f"Final list of user IDs in the database: {', '.join(map(str, final_user_list))}")

# Command to remove userIDs from the database
@app.on_message(filters.command("removeuser") & filters.user(ADMINS) & filters.private)
async def remove_user_from_db(client, message):
    user_ids_to_remove = message.text.split()[1:]  # Extract userIDs from the command
    user_ids_to_remove = [int(user_id) for user_id in user_ids_to_remove if user_id.isdigit()]  # Ensure they are integers

    if not user_ids_to_remove:
        await message.reply_text("Invalid user IDs provided.")
        return

    user_data = user_collection.find_one({})
    existing_user_ids = user_data.get('user_ids', []) if user_data else []

    # Separate user IDs into existing and not existing in the database
    existing_ids_to_remove = [user_id for user_id in user_ids_to_remove if user_id in existing_user_ids]
    non_existing_ids = [user_id for user_id in user_ids_to_remove if user_id not in existing_user_ids]

    # Remove existing userIDs from the database
    if existing_ids_to_remove:
        user_collection.update_one({}, {'$pull': {'user_ids': {'$in': existing_ids_to_remove}}})
        await message.reply_text(f"Removed {len(existing_ids_to_remove)} user(s) from the database.")

    # Reply with non-existing user IDs
    if non_existing_ids:
        await message.reply_text(f"User IDs {', '.join(map(str, non_existing_ids))} not found in the database and therefore ignored.")

    # Reply with the whole list of users finally added to the database
    final_user_list = user_collection.find_one({})['user_ids']
    await message.reply_text(f"Final list of user IDs in the database: {', '.join(map(str, final_user_list))}")

# Command to get authorized user IDs and names
@app.on_message(filters.command("authusers") & filters.user(ADMINS) & filters.private)
async def get_authorized_users(client, message):
    user_data = user_collection.find_one({})
    authorized_user_ids = user_data.get('user_ids', []) if user_data else []

    if not authorized_user_ids:
        await message.reply_text("No authorized users found.")
        return

    user_list_text = "Authorized User IDs:\n"
    
    for user_id in authorized_user_ids:
        try:
            user_info = await client.get_chat(user_id)
            user_name = user_info.first_name if user_info.first_name else "None"
            user_list_text += f"{user_id} - {user_name}\n"
        except Exception as e:
            user_list_text += f"{user_id} - None\n"
            print(f"Error fetching user info for ID {user_id}: {e}")

    await message.reply_text(user_list_text)

# Command to clear all user IDs from the database
@app.on_message(filters.command("cleanusers") & filters.user(OWNER_ID) & filters.private)
async def clear_all_users(client, message):
    user_collection.update_one({}, {'$set': {'user_ids': []}})
    await message.reply_text("All user IDs have been cleared from the database.")
