import os
import time
import asyncio
import json
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient

# ====== CONFIG DARI ENV ======
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
OWNER_ID = int(os.environ.get("OWNER_ID", 0))
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", 0))
MONGO_URL = os.environ.get("MONGO_URL", "")

app = Client("fsub_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
db = MongoClient(MONGO_URL).fsub_bot
users, admins, buttons_db, konten_db, settings = db.users, db.admins, db.buttons, db.konten, db.settings
START_TIME = time.time()

def get_setting(key, default=None):
    data = settings.find_one({"key": key})
    return data["val"] if data else default

async def fsub_check(user_id):
    btns = [b["id"] for b in buttons_db.find({})]
    kb = []
    for cid in btns:
        try:
            if (await app.get_chat_member(int(cid), user_id)).status == "left":
                chat = await app.get_chat(int(cid))
                kb.append([InlineKeyboardButton(f"JOIN {chat.title}", url=chat.invite_link)])
        except: pass
    return len(kb) == 0, kb

async def auto_delete(msg):
    try:
        await asyncio.sleep(int(get_setting("autodel", 10)))
        await msg.delete()
    except: pass

# ====== SEMUA COMMAND ======
@app.on_message(filters.command("start"))
async def start(_, m):
    ok, kb = await fsub_check(m.from_user.id)
    if not ok:
        return await m.reply(get_setting('fsub_msg', '⚠️ Wajib Join Semua Channel'), reply_markup=InlineKeyboardMarkup(kb))
    if not users.find_one({"id": m.from_user.id}):
        users.insert_one({"id": m.from_user.id, "join": datetime.now(), "name": m.from_user.first_name})
        if get_setting("notif") == "on" and LOG_CHANNEL:
            await app.send_message(LOG_CHANNEL, f"➕ Member Baru: {m.from_user.first_name} | `{m.from_user.id}`")
    menu = InlineKeyboardMarkup([
        [InlineKeyboardButton("📥 AMBIL KONTEN", callback_data="view")],
        [InlineKeyboardButton("💎 VIP", callback_data="vip"), InlineKeyboardButton("ℹ️ INFO", callback_data="info")]
    ])
    msg = await m.reply("✅ Bot FSUB Aktif", reply_markup=menu)
    asyncio.create_task(auto_delete(msg))

@app.on_message(filters.command("users") & filters.user(OWNER_ID))
async def get_users(_, m): await m.reply(f"--Mengecek pengguna Bot--\nTotal: {users.count_documents({})} user")

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(_, m):
    if not m.reply_to_message: return await m.reply("Balas pesan yang mau di broadcast")
    msg = await m.reply("Sedang broadcast..."); count=0
    for u in users.find({}):
        try: await m.reply_to_message.copy(u["id"]); count+=1; await asyncio.sleep(0.05)
        except: pass
    await msg.edit(f"--Kirim pesan siaran ke-- pengguna bot\nTerkirim: {count}")

@app.on_message(filters.command("addadmin") & filters.user(OWNER_ID))
async def add_admin(_, m):
    try: uid=int(m.command[1]); admins.update_one({"id":uid},{"$set":{"id":uid}},upsert=True); await m.reply("--Menambahkan admin-- Sukses")
    except: await m.reply("Format: /addadmin [id pengguna]")

@app.on_message(filters.command("deladmin") & filters.user(OWNER_ID))
async def del_admin(_, m): admins.delete_one({"id":int(m.command[1])}); await m.reply("--Menghapus admin-- Sukses")
@app.on_message(filters.command("getadmin") & filters.user(OWNER_ID))
async def get_admin(_, m): data=[str(a["id"]) for a in admins.find({})]; await m.reply("--Melihat admin--\n"+"\n".join(data) if data else "Kosong")
@app.on_message(filters.command("info") & filters.user(OWNER_ID))
async def info(_, m): await m.reply(f"--Cek status bot fsub--\nUsers: {users.count_documents({})}\nButtons: {buttons_db.count_documents({})}\nKonten: {konten_db.count_documents({})}")
@app.on_message(filters.command("ping"))
async def ping(_, m): s=time.time(); msg=await m.reply("Ping..."); await msg.edit(f"--Cek ping bot--\n{round((time.time()-s)*1000)}ms"); asyncio.create_task(auto_delete(msg))
@app.on_message(filters.command("uptime"))
async def uptime(_, m): up=int(time.time()-START_TIME); await m.reply(f"--Cek waktu bot--\n{up//3600}j {up%3600//60}m {up%60}d")
@app.on_message(filters.command("addbutton") & filters.user(OWNER_ID))
async def add_button(_, m): buttons_db.update_one({"id":m.command[1]},{"$set":{"id":m.command[1]}},upsert=True); await m.reply("--Tambah button bot-- Sukses")
@app.on_message(filters.command("delbutton") & filters.user(OWNER_ID))
async def del_button(_, m): buttons_db.delete_one({"id":m.command[1]}); await m.reply("--Hapus button bot-- Sukses")
@app.on_message(filters.command("getbutton") & filters.user(OWNER_ID))
async def get_button(_, m): data=[b["id"] for b in buttons_db.find({})]; await m.reply("--Cek
