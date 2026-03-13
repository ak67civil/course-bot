from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = 31283151
API_HASH = "e9a61f982f39658edd07149cbcff427b"
BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"

UPLOAD_CHANNEL = -1003580669566
INDEX_CHANNEL = -1003760662643

app = Client(
    "coursebot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

videos = {}

@app.on_message(filters.video & filters.chat(UPLOAD_CHANNEL))
async def auto_copy(client, message):

    copied = await message.copy(INDEX_CHANNEL)

    file_id = copied.video.file_id
    msg_id = copied.id

    videos[str(msg_id)] = file_id

    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("▶ Watch Video", callback_data=str(msg_id))]]
    )

    await client.send_message(
        INDEX_CHANNEL,
        "Click below to watch the video",
        reply_markup=button
    )

@app.on_callback_query()
async def send_video(client, callback):

    vid = videos.get(callback.data)

    if vid:
        await client.send_video(
            callback.message.chat.id,
            vid,
            protect_content=True
        )

app.run()
