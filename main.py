import os
import re
from telethon.tl.functions.account import UpdateProfileRequest, UpdateUsernameRequest
from telethon.tl.functions.channels import CreateChannelRequest, LeaveChannelRequest
from telethon.tl.functions.users import GetFullUserRequest
import sys  # <--- ضيف هذا السطر هنا
import asyncio
from datetime import datetime
from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
from datetime import datetime
import pytz
import random
import asyncio
from telethon.tl.functions.messages import DeleteHistoryRequest
from telethon.tl.types import PeerUser
from telethon.tl.custom.button import Button
import json
from telethon import TelegramClient, events, utils, types
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest, GetAuthorizationsRequest, ResetAuthorizationRequest
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest, CreateChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest 
import asyncio
import time
REPLY_FILE = "auto_replies.json"
api_id = 21100923
api_hash = 'deb6dc38b1af6b940b94f843caf151e5'
session_string = "1ApWapzMBu02FpG6d4pf9OvClbzV7oLGvKlKmD1mNEsO3W9yiN-0ZLT6vK5RKiqSb_zWhRw2OyZTkaQtvKHsLw0d-a0bD-N-IeCHBik8QwhCnPu6EcQqbYSkSVEEPHLvlbN5u-dn1NHwlnOwX9-fr2OrP6oqgwEMXabKPCZPD1OQ5SSuJDnuuqYsDBqtP5bDyP8QsvqE77_ZBzfz2-gHMfoj75kCEOOqhMhCgaLo62bdOtCycgrYt7ZH9klYNW4v22iHeKqphbMIROJE5m4TM9WdeZx0xRh2ihjtB1XNiGJ7V9tv9pYnzM75nqb7jq_TLzFgYIW2c0J_bz0a_3Uc2fjfpG5a6yqQ="
client = TelegramClient(StringSession(session_string), api_id, api_hash)

target_group_id = -1005196109912
owner_id = 6651418703
self_destruct_save_enabled = True
bold_text_enabled = False 
name_update_enabled = False
original_name = None
auto_reply_enabled = False
auto_reply_enabled2 = False
GROUP_REPLY_FILE = "group_replies.json"
group_reply_enabled = True 
banned_words = {'aydgdgd', 'كلمة2', 'احتيال', 'شتيمة', 'ممنوع'}
ban_message = "🚫 تم حظرك لأنك قلت كلمة ممنوعة."

@client.on(events.NewMessage(pattern=r"\.الرد الخاص (تفعيل|تعطيل)"))
async def toggle_auto_reply(event):
    if event.sender_id != owner_id:
        return
    
    global auto_reply_enabled2
    cmd = event.pattern_match.group(1)
    
    if cmd == "تفعيل":
        auto_reply_enabled2 = True
        await event.respond("✅ **تم تفعيل الردود الخاصة بنجاح.**")
    else:
        auto_reply_enabled2 = False
        await event.respond("❌ **تم تعطيل الردود الخاصة.**")

@client.on(events.NewMessage(incoming=True)) # يستجيب للرسائل القادمة فقط
async def auto_responder(event):
    global auto_reply_enabled2
  
    if not auto_reply_enabled2 or not event.is_private:
        return
    
    sender = await event.get_sender()
    if sender and getattr(sender, 'bot', False):
        return

    
    text = event.raw_text.strip()
   
    for word, response in keywords.items():
        if text == word.strip(): 
            await event.reply(response)
            break # توقف بعد إرسال الرد

# دالة لتحميل الردود من الملف
def load_replies():
    if os.path.exists(REPLY_FILE):
        with open(REPLY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# دالة لحفظ الردود في الملف
def save_replies(replies):
    with open(REPLY_FILE, "w", encoding="utf-8") as f:
        json.dump(replies, f, ensure_ascii=False, indent=4)

# تحميل الردود عند بدء التشغيل
keywords = load_replies()

@client.on(events.NewMessage(pattern=r"\.اضف رد خاص (.+) - (.+)"))
async def add_reply(event):
    if event.sender_id != owner_id: return
    word = event.pattern_match.group(1).strip()
    response = event.pattern_match.group(2).strip()
    
    keywords[word] = response
    save_replies(keywords)
    await event.respond(f"✅ تم إضافة الرد بنجاح الى الردود الخاصة!\n📝 الكلمة: {word}\n💬 الرد: {response}")

@client.on(events.NewMessage(pattern=r"\.حذف رد خاص (.+)"))
async def delete_reply(event):
    if event.sender_id != owner_id: return
    word = event.pattern_match.group(1).strip()
    
    if word in keywords:
        del keywords[word]
        save_replies(keywords)
        await event.respond(f"🗑 تم حذف الرد الخاص بكلمة ({word}) بنجاح.")
    else:
        await event.respond(f"❌ الكلمة ({word}) غير موجودة في قائمة الردود.")

@client.on(events.NewMessage(pattern=r"\.ردود الخاص"))
async def list_replies(event):
    if event.sender_id != owner_id: return
    if not keywords:
        return await event.respond("📭 قائمة الردود الخاصة فارغة حالياً.")
    
    msg = "📋 **قائمة الردود الخاصة الحالية:**\n\n"
    for word, resp in keywords.items():
        msg += f"🔹 **{word}** ← {resp}\n"
    
    await event.respond(msg)

@client.on(events.NewMessage(pattern=r"\.تصفير الردود الخاصة"))
async def clear_all_replies(event):
    if event.sender_id != owner_id: return
    global keywords
    keywords = {}
    save_replies(keywords)
    await event.respond("🗑 تم مسح وتصفير جميع الردود الخاصة بنجاح.")

# --- [ محرك الردود التلقائي ] ---
@client.on(events.NewMessage(incoming=True))
async def auto_responder(event):
    if not auto_reply_enabled2 or event.is_bot: return
    
    text = event.raw_text
    for word, response in keywords.items():
        if word in text:
            await event.reply(response)
            break

# --- [ أمر عرض الإعدادات ] ---
@client.on(events.NewMessage(pattern=r"\.الاعدادات"))
async def show_settings(event):
    if event.sender_id != owner_id:
        return
    
    settings_text = (
        f"⚙️ **لوحة تحكم سورس الطائي (دائمية):**\n"
        f"─── • 💠 • ───\n"
        f"🔑 **API ID:** `{api_id}`\n"
        f"🔑 **API HASH:** `{api_hash}`\n"
        f"👤 **OWNER ID:** `{owner_id}`\n"
        f"📢 **TARGET GROUP:** `{target_group_id}`\n"
        f"─── • 🔐 • ───\n"
        f"📜 **SESSION:**\n"
        f"`{session_string}` \n"
        f"─── • 💠 • ───\n"
        f"💡 **أوامر التحديث الدائم (تعدل ملف الكود):**\n"
        f"• `.تحديث الايدي` + الرقم\n"
        f"• `.تحديث الهاش` + الكود\n"
        f"• `.تحديث السيشن` + الكود\n"
        f"• `.تحديث المالك` + الايدي\n"
        f"• `.تحديث الكروب` + الايدي\n"
        f"─── • 🦅 • ─── \n"
        f" ارسل `.ريستارت` عند التحديث."
    )
    await event.respond(settings_text)

@client.on(events.NewMessage(pattern=r"\.تحديث الايدي (\d+)"))
async def up_api_id(event):
    global api_id
    if event.sender_id != owner_id: return
    new_val = int(event.pattern_match.group(1).strip())
    current_file = sys.argv[0]
    try:
        with open(current_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(current_file, "w", encoding="utf-8") as f:
            found = False
            for line in lines:
                if line.strip().startswith("api_id =") or line.strip().startswith("api_id="):
                    f.write(f'api_id = {new_val}\n')
                    found = True
                else:
                    f.write(line)
        if found:
            await event.respond(f"✅ تم تحديث **API ID** بنجاح في السورس والذاكرة.\nالقيمة الحالية: `{api_id}`")
        else:
            await event.respond("❌ لم أجد متغير `api_id` في السورس.")
    except Exception as e:
        await event.respond(f"❌ خطأ: {e}")

# --- أمر تحديث API HASH ---
@client.on(events.NewMessage(pattern=r"\.تحديث الهاش (.+)"))
async def up_api_hash(event):
    global api_hash
    if event.sender_id != owner_id: return
    new_val = event.pattern_match.group(1).strip()
    current_file = sys.argv[0]
    try:
        with open(current_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(current_file, "w", encoding="utf-8") as f:
            found = False
            for line in lines:
                if line.strip().startswith("api_hash =") or line.strip().startswith("api_hash="):
                    f.write(f'api_hash = "{new_val}"\n')
                    found = True
                else:
                    f.write(line)
        if found:
            api_hash = new_val  # تحديث في الذاكرة
            await event.respond(f"✅ تم تحديث **API HASH** بنجاح في السورس والذاكرة.")
        else:
            await event.respond("❌ لم أجد متغير `api_hash` في السورس.")
    except Exception as e:
        await event.respond(f"❌ خطأ: {e}")

# --- أمر تحديث السيشن ---
@client.on(events.NewMessage(pattern=r"\.تحديث السيشن (.+)"))
async def up_session(event):
    global session_string
    if event.sender_id != owner_id: return
    new_val = event.pattern_match.group(1).strip()
    current_file = sys.argv[0]
    try:
        with open(current_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(current_file, "w", encoding="utf-8") as f:
            found = False
            for line in lines:
                if line.strip().startswith("session_string =") or line.strip().startswith("session_string="):
                    f.write(f'session_string = "{new_val}"\n')
                    found = True
                else:
                    f.write(line)
        if found:
            await event.respond(f"✅ تم تحديث **SESSION STRING** بنجاح في السورس والذاكرة.")
        else:
            await event.respond("❌ لم أجد متغير `session_string` في السورس.")
    except Exception as e:
        await event.respond(f"❌ خطأ: {e}")
@client.on(events.NewMessage(pattern=r"\.تحديث المالك (\d+)"))
async def up_owner_id(event):
    global owner_id
    if event.sender_id != owner_id: return
    
    new_val = int(event.pattern_match.group(1).strip())
    current_file = sys.argv[0]
    
    try:
        with open(current_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(current_file, "w", encoding="utf-8") as f:
            found = False
            for line in lines:
                if line.strip().startswith("owner_id =") or line.strip().startswith("owner_id="):
                    f.write(f'owner_id = {new_val}\n')
                    found = True
                else:
                    f.write(line)
        
        if found:
            # تحديث القيمة في الذاكرة فوراً
            await event.respond(f"✅ تم تحديث **ايدي المالك** بنجاح في السورس والذاكرة.\nالايدي الجديد: `{owner_id}`")
        else:
            await event.respond("❌ لم أجد متغير `owner_id` في الملف.")
    except Exception as e:
        await event.respond(f"❌ خطأ: {e}")

# --- أمر تحديث ايدي الكروب المستهدف (بدون ريستارت) ---
@client.on(events.NewMessage(pattern=r"\.تحديث الكروب (-?\d+)"))
async def up_target_group(event):
    global target_group_id
    if event.sender_id != owner_id: return
    
    new_val = int(event.pattern_match.group(1).strip())
    current_file = sys.argv[0]
    
    try:
        with open(current_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(current_file, "w", encoding="utf-8") as f:
            found = False
            for line in lines:
                if line.strip().startswith("target_group_id =") or line.strip().startswith("target_group_id="):
                    f.write(f'target_group_id = {new_val}\n')
                    found = True
                else:
                    f.write(line)
        
        if found:
            # تحديث القيمة في الذاكرة فوراً
            await event.respond(f"✅ تم تحديث **ايدي الكروب** بنجاح.\nالايدي الجديد: `{target_group_id}`")
        else:
            await event.respond("❌ لم أجد متغير `target_group_id` في الملف.")
    except Exception as e:
        await event.respond(f"❌ خطأ: {e}")

# دوال الحفظ والتحميل الخاصة بالمجموعات
def load_group_replies():
    if os.path.exists(GROUP_REPLY_FILE):
        with open(GROUP_REPLY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_group_replies(replies):
    with open(GROUP_REPLY_FILE, "w", encoding="utf-8") as f:
        json.dump(replies, f, ensure_ascii=False, indent=4)

group_keywords = load_group_replies()

# --- [ أوامر التحكم بالمجموعات ] ---

@client.on(events.NewMessage(pattern=r"\.الرد العام (تفعيل|تعطيل)"))
async def toggle_group_reply(event):
    if event.sender_id != owner_id: return
    global group_reply_enabled
    action = event.pattern_match.group(1)
    group_reply_enabled = (action == "تفعيل")
    await event.respond(f"✅ تم **{action}** ردود المجموعات بنجاح.")

@client.on(events.NewMessage(pattern=r"\.اضف رد عام (.+) - (.+)"))
async def add_group_reply(event):
    if event.sender_id != owner_id: return
    word = event.pattern_match.group(1).strip()
    resp = event.pattern_match.group(2).strip()
    group_keywords[word] = resp
    save_group_replies(group_keywords)
    await event.respond(f"✅ تم إضافة رد للمجموعات:\n🔹 {word} ← {resp}")

@client.on(events.NewMessage(pattern=r"\.حذف رد عام (.+)"))
async def del_group_reply(event):
    if event.sender_id != owner_id: return
    word = event.pattern_match.group(1).strip()
    if word in group_keywords:
        del group_keywords[word]
        save_group_replies(group_keywords)
        await event.respond(f"🗑 تم حذف رد المجموعات لـ ({word})")
    else:
        await event.respond("❌ الرد غير موجود.")

@client.on(events.NewMessage(pattern=r"\.ردود العام"))
async def list_group_replies(event):
    if event.sender_id != owner_id: return
    if not group_keywords: return await event.respond("📭 قائمة ردود المجموعات فارغة.")
    msg = "📋 **قائمة ردود المجموعات:**\n\n"
    for w, r in group_keywords.items(): msg += f"• `{w}` ← {r}\n"
    await event.respond(msg)
@client.on(events.NewMessage(pattern=r"\.تصفير الردود العام"))
async def clear_all_replies(event):
    if event.sender_id != owner_id: return
    global keywords
    keywords = {}
    save_replies(keywords)
    await event.respond("🗑 تم مسح وتصفير جميع الردود العام بنجاح.")    

# --- [ محرك الردود للمجموعات فقط ] ---

@client.on(events.NewMessage(incoming=True))
async def group_auto_responder(event):
    global group_reply_enabled
    
    # الشروط: مفعل + في مجموعة + ليس بوتاً + ليس المالك
    if not group_reply_enabled or not event.is_group or event.sender_id == owner_id:
        return
    
    sender = await event.get_sender()
    if sender and getattr(sender, 'bot', False):
        return

    # المطابقة التامة
    text = event.raw_text.strip()
    if text in group_keywords:
        await event.reply(group_keywords[text])

@client.on(events.NewMessage(pattern=r"\.اوامر الردود"))
async def help_group_replies(event):
    if event.sender_id != owner_id: return
    await event.respond(
        "**** سورس الطائي 🦅\n"
        "⚙️ **قائمة أوامر الردود الخاصة:**\n"
        "─── • 💠 • ───\n"
        "🔹 **للتفعيل والتعطيل:**\n"
        "• `.الرد الخاص تفعيل` ← لتشغيل ميزة الرد.\n"
        "• `.الرد الخاص تعطيل` ← لإيقاف ميزة الرد.\n"
        "─── • 💠 • ───\n"
        "🔹 **إدارة الردود:**\n"
        "• `.اضف رد خاص (الكلمة) - (الرد)`\n"
        "• `.حذف رد خاص (الكلمة)`\n"
        "• `.ردود الخاص` ← لعرض كل الردود المضافة.\n"
        "• `.تصفير الردود الخاصة` ← لحذف كل الردود.\n"
        "─── • 💠 • ───\n"
        "💡 **مثال للإضافة:**\n"
        "`.اضف رد خاص السلام - وعليكم السلام يغالي`\n"
        "─── • 🦅 • ───\n"
        "🦅 **أوامر ردود المجموعات:**\n"
        "🔹 **للتفعيل والتعطيل:**\n"
        "• `.الرد العام تفعيل` ← لتشغيل ميزة الرد.\n"
        "• `.الرد العام تعطيل` ← لإيقاف ميزة الرد.\n"
        "─── • 💠 • ───\n"
        "🔹 **إدارة الردود:**\n"
        "• `.اضف رد عام (الكلمة) - (الرد)`\n"
        "• `.حذف رد عام (الكلمة)`\n"
        "• `.ردود العام` ← لعرض كل الردود المضافة.\n"
        "• `.تصفير الردود العام` ← لحذف كل الردود.\n"
        "─── • 💠 • ───\n"
        "💡 **مثال للإضافة:**\n"
        "`.اضف رد عام السلام - وعليكم السلام يغالي`\n"
    )


muted_users = set()
excluded_users = set()
@client.on(events.NewMessage(pattern=r"\.حذف المحادثة"))
async def delete_conversation(event):
    if event.sender_id != owner_id:
        await event.reply("⚠️ لا تملك صلاحية استخدام هذا الأمر.")
        return
    if not event.is_reply:
        await event.reply("❗ يجب الرد على رسالة من الشخص الذي تريد حذف المحادثة معه.")
        return

    try:
        replied_msg = await event.get_reply_message()
        user = await replied_msg.get_sender()
        user_entity = await client.get_entity(user.id)

        await client(DeleteHistoryRequest(
            peer=PeerUser(user_entity.id),
            max_id=0,
            revoke=True
        ))

        await event.reply("✅ تم حذف المحادثة بالكامل من الطرفين.")
        print(f"🗑️ تم حذف المحادثة بالكامل مع: {user.id}")

    except Exception as e:
        await event.reply(f"❌ حدث خطأ أثناء محاولة الحذف: {e}\nقد يكون الشخص الآخر قد حظر حسابك، أو هناك مشكلة في الصلاحيات.")


@client.on(events.NewMessage(pattern=r"\.ايدي"))
async def get_user_info(event):
    # التحقق من المالك
    if event.sender_id != owner_id:
        await event.reply("⚠️ **عذراً، هذا الأمر مخصص للمطور فقط.**")
        return
    
    # الحصول على الشخص (سواء بالرد أو الشخص نفسه إذا لم يوجد رد)
    if event.is_reply:
        replied = await event.get_reply_message()
        user = await replied.get_sender()
    else:
        user = await event.get_sender()

    if not user or not isinstance(user, types.User):
        await event.reply("❗ **لم أتمكن من العثور على معلومات المستخدم.**")
        return

    # إرسال حالة "جارِ جلب البيانات" ليعطي طابع احترافي
    status_msg = await event.reply("🔍 **جارِ جلب معلومات المستخدم...**")

    try:
        # جلب البيانات الكاملة (Bio، عدد الصور، الخ)
        full = await client(functions.users.GetFullUserRequest(user.id))
        
        # تحديد الحالة (متصل أو غير متصل)
        if isinstance(user.status, types.UserStatusOnline):
            status = "🟢 متصل الآن"
        elif isinstance(user.status, types.UserStatusOffline):
            status = "🔴 غير متصل"
        else:
            status = "⚪ غير معروف"

        # تحميل الصورة
        photo = await client.download_profile_photo(user.id, file=f"info_{user.id}.jpg")

        # تنسيق النص البروفايل
        info_text = (
            f"✨ **معلومات المستخدم** ✨\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 **الاسم:** {user.first_name} {user.last_name or ''}\n"
            f"🆔 **الآيدي:** `{user.id}`\n"
            f"🔗 **اليوزر:** @{user.username if user.username else 'لا يوجد'}\n"
            f"📡 **الحالة:** {status}\n"
            f"🤖 **نوع الحساب:** {'بوت' if user.bot else 'مستخدم حقيقي'}\n"
            f"🖼️ **عدد الصور:** {full.full_user.profile_photo.dc_id if hasattr(full.full_user.profile_photo, 'dc_id') else '0'}\n"
            f"📝 **البايو:** `{full.full_user.about or 'لا يوجد بايو'}`\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🌐 **رابط الحساب:** [اضغط هنا](tg://user?id={user.id})"
        )

        if photo:
            await client.send_file(event.chat_id, photo, caption=info_text, reply_to=event.reply_to_msg_id or event.id)
            os.remove(photo) # حذف الصورة من الملفات بعد الإرسال
        else:
            await event.reply(info_text)
        
        # حذف رسالة "جارِ الجلب"
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit(f"❌ **حدث خطأ:**\n`{str(e)}`")

##ٍ
muted_users = set()
# --- 1. أمر كتم المستخدم ---
@client.on(events.NewMessage(pattern=r"\.كتم"))
async def mute_user(event):
    if event.sender_id != owner_id: return
    if not event.is_reply:
        return await event.reply("❗ يجب الرد على رسالة الشخص الذي تريد كتمه.")

    replied = await event.get_reply_message()
    user = await replied.get_sender()
    
    if user.id not in muted_users:
        muted_users.add(user.id)
        await event.reply(f"🔇 تم كتم **{user.first_name}** بنجاح.")
    else:
        await event.reply("ℹ️ المستخدم مكتوم بالفعل.")

# --- 2. أمر إلغاء كتم المستخدم ---
@client.on(events.NewMessage(pattern=r"\.الغاء كتم"))
async def unmute_user(event):
    if event.sender_id != owner_id: return
    if not event.is_reply:
        return await event.reply("❗ يجب الرد على رسالة الشخص الذي تريد فك كتمه.")

    replied = await event.get_reply_message()
    user = await replied.get_sender()

    if user.id in muted_users:
        muted_users.remove(user.id)
        await event.reply(f"🔊 تم فك الكتم عن **{user.first_name}**.")
    else:
        await event.reply("ℹ️ هذا المستخدم غير مكتوم.")

# --- 3. أمر عرض قائمة المكتومين (الجديد) ---
@client.on(events.NewMessage(pattern=r"\.المكتومين"))
async def list_muted(event):
    if event.sender_id != owner_id: return
    
    if not muted_users:
        return await event.reply("📝 **قائمة المكتومين فارغة.**")

    msg_text = "🚫 **قائمة المستخدمين المكتومين:**\n━━━━━━━━━━━━━━━━━━\n"
    
    for count, m_id in enumerate(muted_users, 1):
        try:
            # محاولة جلب اسم المستخدم من الآيدي ليكون العرض أجمل
            u_entity = await client.get_entity(m_id)
            name = u_entity.first_name
        except:
            name = "مستخدم غير معروف"
        
        msg_text += f"{count} - {name} » (`{m_id}`)\n"
    
    msg_text += "━━━━━━━━━━━━━━━━━━"
    await event.reply(msg_text)

# --- محرك الحذف التلقائي ---
@client.on(events.NewMessage)
async def delete_muted_messages(event):
    if event.is_private and not event.out:
        if event.sender_id in muted_users:
            try:
                await event.delete()
                # إرسال رسالة تنبيه (اختياري يمكنك حذف السطر بالأسفل إذا أردت صمتاً تاماً)
                await client.send_message(event.sender_id, "❌ أنتَ مكتوم، لا تتعب نفسك 🌚")
            except:
                pass      
##
from telethon import events, functions, types

# --- 1. أمر الحظر الحقيقي (Block) ---
@client.on(events.NewMessage(pattern=r"\.حظر"))
async def real_ban(event):
    if event.sender_id != owner_id: return
    
    # تحديد الشخص بالرد أو اليوزر أو الايدي
    if event.is_reply:
        replied = await event.get_reply_message()
        user = await replied.get_sender()
    else:
        parts = event.text.split()
        if len(parts) > 1:
            try: user = await client.get_entity(parts[1])
            except: return await event.reply("❌ لم أجد هذا المستخدم.")
        else:
            return await event.reply("❗ رد على الشخص أو ضع يوزره.")

    try:
        # إرسال رسالة أخيرة قبل الحظر (اختياري)
        await client.send_message(user.id, "🚫 **تم حظرك نهائياً، لن تستطيع رؤية معلوماتي بعد الآن.**")
        
        # الأمر البرمجي للحظر المباشر من سيرفرات تليجرام
        await client(functions.contacts.BlockRequest(id=user.id))
        
        await event.reply(f"✅ تم حظر **{user.first_name}** حظراً حقيقياً (Block).")
    except Exception as e:
        await event.reply(f"❌ حدث خطأ: {e}")

# --- 2. أمر فك الحظر الحقيقي (Unblock) ---
@client.on(events.NewMessage(pattern=r"\.الغاء حظر"))
async def real_unban(event):
    if event.sender_id != owner_id: return
    
    if event.is_reply:
        replied = await event.get_reply_message()
        user = await replied.get_sender()
    else:
        parts = event.text.split()
        if len(parts) > 1:
            try: user = await client.get_entity(parts[1])
            except: return await event.reply("❌ لم أجد هذا المستخدم.")
        else:
            return await event.reply("❗ رد على الشخص أو ضع يوزره.")

    try:
        # الأمر البرمجي لفك الحظر من سيرفرات تليجرام
        await client(functions.contacts.UnblockRequest(id=user.id))
        
        await event.reply(f"✅ تم فك الحظر عن **{user.first_name}** بنجاح.")
        # إخباره (اختياري)
        await client.send_message(user.id, "😇 **تم فك الحظر عنك، يمكنك مراسلتي الآن.**")
    except Exception as e:
        await event.reply(f"❌ حدث خطأ: {e}")

# --- 3. عرض قائمة المحظورين من تليجرام ---
@client.on(events.NewMessage(pattern=r"\.المحظورين"))
async def list_blocked(event):
    if event.sender_id != owner_id: return
    
    try:
        # جلب القائمة السوداء الفعلية من حسابك
        result = await client(functions.contacts.GetBlockedRequest(offset=0, limit=1000))
        if not result.users:
            return await event.reply("📝 قائمة الحظر فارغة.")
        
        msg = "🚫 **قائمة المحظورين (Block List):**\n━━━━━━━━━━━━━━━━━━\n"
        for count, user in enumerate(result.users, 1):
            msg += f"{count} - {user.first_name} » (`{user.id}`)\n"
        
        msg += "━━━━━━━━━━━━━━━━━━"
        await event.reply(msg)
    except Exception as e:
        await event.reply(f"❌ فشل جلب القائمة: {e}")
@client.on(events.NewMessage(pattern=r"^\.اوامر الحظر و الكتم"))
async def show_help(event):
    help_text = """
🛡️ **قائمة الحظر و الكتم**
━━━━━━━━━━━━━━━━━━
📌 **اوامر الكتم**
• `.كتم `: كتم مستخدم معين بالرد
• `.الغاء كتم` (لفك القيد)

📌 **أوامر الحظر:**
• `.حظر` (بالرد)
• `.الغاء حظر` (لفك القيد)
📌 **أوامر العرض:**
• `.المكتومين` | `.المحظورين`
━━━━━━━━━━━━━━━━━━
"""
    await event.reply(help_text)
# أوامر التحكم بالكلمات الممنوعة
@client.on(events.NewMessage(pattern=r"\.اضف منع (.+)"))
async def add_banned_word(event):
    if event.sender_id != owner_id:
        await event.reply("⚠️ لا تملك صلاحية استخدام هذا الأمر.")
        return
    
    word = event.pattern_match.group(1).strip().lower()
    if word not in banned_words:
        banned_words.add(word)
        await event.reply(f"✅ تم إضافة الكلمة `«{word}»` إلى قائمة الممنوعات.")
    else:
        await event.reply(f"ℹ️ الكلمة `«{word}»` موجودة مسبقًا في قائمة الممنوعات.")

@client.on(events.NewMessage(pattern=r"\.حذف منع (.+)"))
async def remove_banned_word(event):
    if event.sender_id != owner_id:
        await event.reply("⚠️ لا تملك صلاحية استخدام هذا الأمر.")
        return
    
    word = event.pattern_match.group(1).strip().lower()
    if word in banned_words:
        banned_words.remove(word)
        await event.reply(f"✅ تم حذف الكلمة `«{word}»` من قائمة الممنوعات.")
    else:
        await event.reply(f"ℹ️ الكلمة `«{word}»` غير موجودة في قائمة الممنوعات.")

@client.on(events.NewMessage(pattern=r"\.قائمة المنع"))
async def list_banned_words(event):
    if event.sender_id != owner_id:
        await event.reply("⚠️ لا تملك صلاحية استخدام هذا الأمر.")
        return
    
    if not banned_words:
        await event.reply("ℹ️ قائمة الكلمات الممنوعة فارغة.")
    else:
        words_list = "\n".join(f"- `{word}`" for word in sorted(list(banned_words)))
        await event.reply(f"🚫 **قائمة الكلمات الممنوعة:**\n{words_list}")
@client.on(events.NewMessage(pattern=r"^\.اوامر المنع"))
async def show_help(event):
    help_text = """
🛡️ **أهلاً بك في أوامر المنع - سورس الطائي** 🛡️
━━━━━━━━━━━━━━━━━━━━

📋 **الأوامر المتاحة:**

🔹 `.قائمة المنع`
   - لعرض جميع الكلمات التي تم منعها في السورس.

🔹 `.اضف منع` + (الكلمة)
   - لإضافة كلمة جديدة إلى قائمة الكلمات المحظورة.

🔹 `.حذف منع` + (الكلمة)
   - لإزالة كلمة معينة من قائمة المنع.

━━━━━━━━━━━━━━━━━━━━
💡 **ملاحظة:** عند إضافة كلمة، سيقوم البوت بحذف أي رسالة تحتوي عليها تلقائياً.
"""
    await event.reply(help_text)
@client.on(events.NewMessage(pattern=r"\.السورس"))
async def show_source_info(event):
    if event.sender_id != owner_id:
        await event.reply("⚠️ **عذراً، هذا الأمر مخصص لمالك السورس فقط.**")
        return

    startup_message_text = """
🦅 **أهلاً بك في سورس الطائي - الإصدار [V2]** 🦅
━━━━━━━━━━━━━━━━━━━━

🛠️ **قائمة التحكم والأوامر المتاحة:**

💬 **قسم الردود:**
• ارسل `.اوامر الردود` - لإدارة الردود التلقائية.
ارسل `.اوامر النوم` لوضع الحساب في وضع النوم.

⚙️ **إعدادات الحساب:**
• ارسل `.الاعدادات` - لعرض (الآيبي، الجلسة، والبيانات).
ارسل `.تخزين نشغيل`لتخزين الرسائل في المجموعة.
ارسل `.تخزين ايقاف`لايقاف تخزين الرسائل في المجموعة.


**الترفية والتحميل**
ارسل `الخدمات الترفيهية` للاطلاع على هذه الخدمات.

🕒 **اوامر الوقتي:**
• ارسل `.الاسم وقتي تفعيل` - لتفعيل الساعة والتاريخ في اسمك.
• ارسل `.الاسم وقتي تعطيل` - لإيقاف الساعة واسترجاع اسمك.
• ارسل `.البايو وقتي تفعيل` - لتفعيل الساعة والتاريخ في البايو.
• ارسل `.البايو وقتي تعطيل` - لإيقاف الساعة واسترجاع البايو.

🛡️ **الحماية والإدارة:**
• ارسل `.اوامر الحظر` - لإدارة الحظر والكتم (المؤقت والدائم).
• ارسل `.اوامر المنع` - لإدارة فلترة الكلمات والمنع التلقائي.
ارسل `.تحكم الحساب`لتحكم في حسابك بشكل متقدم.

━━━━━━━━━━━━━━━━━━━━
🚀 **حالة السورس:** مستقر ويعمل بنظام 24 ساعة.
👨‍💻 **مطور السورس:** [علي الطائي @altaee_z]
"""
    
    await event.reply(startup_message_text)
import asyncio
from datetime import datetime
import pytz
from telethon.tl.functions.account import UpdateProfileRequest
from telethon import events

# المتغيرات
name_update_enabled = False
original_name = ""

# دالة التحديث السريع (توقيت بغداد)
async def update_name_now():
    try:
        timezone = pytz.timezone('Asia/Baghdad')
        now = datetime.now(timezone)
        # تنسيق 12 ساعة مع زخرفة خفيفة لجمالية الاسم
        current_time = now.strftime("%I:%M %p")
        current_date = now.strftime("%m/%d")
        new_name = f"‹ {current_time} | {current_date} ›"
        
        await client(UpdateProfileRequest(first_name=new_name))
    except Exception as e:
        print(f"Update Error: {e}")

# دالة الحلقة (تحديث كل ثانيتين)
async def name_time_loop():
    global name_update_enabled
    while True:
        if name_update_enabled:
            await update_name_now()
            await asyncio.sleep(2) # تأخير ثانيتين فقط كما طلبت
        else:
            await asyncio.sleep(5) # انتظار أطول قليلاً عند التعطيل لتوفير الجهد

# --- [ أوامر التحكم المحدثة ] ---
@client.on(events.NewMessage(pattern=r"^\.الاسم وقتي (تفعيل|تعطيل)"))
async def toggle_name_time(event):
    global name_update_enabled, original_name
    if event.sender_id != owner_id: return

    cmd = event.pattern_match.group(1)

    if cmd == "تفعيل":
        if not name_update_enabled:
            me = await client.get_me()
            original_name = me.first_name
            name_update_enabled = True
            
            # التحديث الفوري الأول قبل إرسال الرسالة
            await update_name_now()
            
            await event.respond("🕒 **تم التفعيل بنجاح!**\nالاسم يتحدث الآن كل ثانيتين بتوقيت بغداد.")
        else:
            await event.respond("ℹ️ الاسم الوقتي يعمل بالفعل.")

    elif cmd == "تعطيل":
        if name_update_enabled:
            name_update_enabled = False
            # انتظار بسيط لضمان توقف الدالة ثم استعادة الاسم
            await asyncio.sleep(2.5) 
            await client(UpdateProfileRequest(first_name=original_name))
            await event.respond(f"✅ تم التعطيل وإعادة اسمك: `{original_name}`")
        else:
            await event.respond("ℹ️ الاسم الوقتي معطل مسبقاً.")

# تشغيل المهمة في الخلفية
client.loop.create_task(name_time_loop())
bio_update_enabled = False
original_bio = ""

# دالة تحديث البايو اللحظية
async def update_bio_now():
    try:
        timezone = pytz.timezone('Asia/Baghdad')
        now = datetime.now(timezone)
        
        # تنسيق الوقت والتاريخ للبايو
        current_time = now.strftime("%I:%M %p")
        current_date = now.strftime("%Y/%m/%d")
        
        # كليشة البايو (تقدر تغيرها)
        new_bio = f"🕒 بغداد: {current_time} | 📅 {current_date}"
        
        # أمر تحديث البايو في تليجرام
        await client(functions.account.UpdateProfileRequest(about=new_bio))
    except Exception as e:
        print(f"Bio Update Error: {e}")

# دالة الحلقة (تحديث البايو كل دقيقة - البايو لا يحتاج تحديث كل ثانيتين لتجنب الحظر)
async def bio_time_loop():
    global bio_update_enabled
    while True:
        if bio_update_enabled:
            await update_bio_now()
            await asyncio.sleep(60) # تحديث البايو كل دقيقة كافي جداً ومريح للحساب
        else:
            await asyncio.sleep(5)

# --- [ أوامر التحكم بالبايو ] ---
@client.on(events.NewMessage(pattern=r"^\.البايو وقتي (تفعيل|تعطيل)"))
async def toggle_bio_time(event):
    global bio_update_enabled, original_bio
    if event.sender_id != owner_id: return

    cmd = event.pattern_match.group(1)

    if cmd == "تفعيل":
        if not bio_update_enabled:
            # جلب البايو الحالي لحفظه قبل التغيير
            full = await client(functions.users.GetFullUserRequest('me'))
            original_bio = full.full_user.about or ""
            
            bio_update_enabled = True
            await update_bio_now() # تحديث فوري
            await event.respond("📝 **تم تفعيل البايو الوقتي بنجاح.**\nسيتحدث البوت وقتك في البايو تلقائياً.")
        else:
            await event.respond("ℹ️ البايو الوقتي مفعل مسبقاً.")

    elif cmd == "تعطيل":
        if bio_update_enabled:
            bio_update_enabled = False
            await asyncio.sleep(1)
            # استعادة البايو الأصلي
            await client(functions.account.UpdateProfileRequest(about=original_bio))
            await event.respond(f"✅ تم تعطيل البايو الوقتي وإعادة بايو حسابك السابق.")
        else:
            await event.respond("ℹ️ البايو الوقتي معطل بالفعل.")

# تشغيل المهمة في الخلفية
client.loop.create_task(bio_time_loop())
@client.on(events.NewMessage)
async def all_messages_handler(event):
    # هنا تضيف السطر
    global name_update_enabled, original_name, bold_text_enabled, self_destruct_save_enabled

    sender = await event.get_sender()
    sender_id = event.sender_id
    sender_name = sender.first_name or "غير معروف"
    sender_username = f"@{sender.username}" if sender.username else "لا يوجد"
    message_text = event.raw_text.strip()

    for word in banned_words:
        if word in message_text.lower():
            try:
                await event.respond(ban_message)
            except:
                pass # إذا فشل الرد، لا تتوقف
            try:
                await client(functions.contacts.BlockRequest(event.sender_id))
                print(f"🚫 تم حظر {sender_id} بسبب الكلمة: {word}")
            except Exception as e:
                print(f"❌ فشل الحظر: {e}")
            return # توقف هنا بعد الحظر والرد

    if not event.out and event.is_private:
        if self_destruct_save_enabled and event.media:
            if hasattr(event.media, 'ttl_seconds') and event.media.ttl_seconds:
                try:
                    file_path = await event.download_media()
                    if file_path:
                        await client.send_message(
                            'me', 
                            f"📥 **تم حفظ وسائط ذاتية التدمير من:**\n"
                            f"👤 الاسم: {sender_name}\n"
                            f"🆔 ID: `{sender_id}`\n"
                            f"🔗 Username: {sender_username}\n", 
                            file=file_path
                        )
                        os.remove(file_path) # حذف الملف بعد إرساله للرسائل المحفوظة
                        print(f"✅ تم حفظ وحذف وسائط ذاتية التدمير من: {sender_id}")
                       
                        return 
                except Exception as e:
                    print(f"❌ خطأ في حفظ الوسائط ذاتية التدمير: {e}")
                   

    if sender_id == owner_id:
        if message_text.lower() == ".تلاتللتلتلتلتلتلتل":
            me = await client.get_me()
            await event.respond(f"🆔 ايدي حسابك هو: `{me.id}`")
            print(f"✅ تم طلب ID المالك من قبل: {sender_id}")
            return


        elif message_text.lower() == '.خط':
            bold_text_enabled = True
            await event.respond("✅ تم تفعيل وضع الخط الغامق. أي رسالة ترسلها الآن ستكون بخط غامق.")
            return
        elif message_text.lower() == '.الغاءخط' or message_text.lower() == '.الغاء الخط':
            bold_text_enabled = False
            await event.respond("🚫 تم إيقاف وضع الخط الغامق. الرسائل ستعود لطبيعتها.")
            return
        elif message_text.lower() == '.ذاتيه':
            self_destruct_save_enabled = True
            await event.respond("✅ تم تفعيل حفظ الوسائط ذاتية التدمير إلى الرسائل المحفوظة.")
            print("✅ تم تفعيل حفظ الوسائط ذاتية التدمير من:", sender_id)
            return
        elif message_text.lower() == '.تعطيل الذاتيه':
            self_destruct_save_enabled = False
            await event.respond("🚫 تم إيقاف حفظ الوسائط ذاتية التدمير.")
            print("🚫 تم إيقاف حفظ الوسائط ذاتية التدمير من:", sender_id)
            return            

    else: 
        pass 
            
    if event.out and bold_text_enabled:
        if not message_text.lower().startswith('.') and not message_text.lower().startswith('/'):
            try:
                await event.edit(f"**{message_text}**")
                print(f"✅ تم تعديل رسالة بخط غامق في: {event.chat_id}")
                return
            except Exception as e:
                print(f"❌ خطأ أثناء تعديل الرسالة إلى خط غامق: {e}")

async def update_name_periodically():
    global name_update_enabled
    while True:
        if name_update_enabled:
            try:
                baghdad_time = datetime.now(pytz.timezone('Asia/Baghdad'))
                formatted_time = baghdad_time.strftime("%I:%M %p")
                formatted_time = formatted_time.replace("AM", "ص").replace("PM", "م")
                new_name = f"🕒 {formatted_time}"
                await client(UpdateProfileRequest(first_name=new_name, last_name=""))
                print(f"✅ تم تحديث الاسم إلى: {new_name}")
            except Exception as e:
                print(f"❌ فشل تحديث الاسم: {e}")
        await asyncio.sleep(60)

print("userbot is ruuning.....")
client.loop.create_task(update_name_periodically())
client.start()

# --- دالة رسالة التشغيل التلقائي ---
async def send_startup_message():
    try:
        # تأكد من وجود ملف الصورة 'A.jpg' في نفس مجلد السورس
        await client.send_file(
            'me',  # إرسال إلى الرسائل المحفوظة
            file='A.jpg', 
            caption=(
                "🚀 **تم تشغيل سورس الطائي بنجاح!**\n"
                "تاريخ التشغيل: `{}`\n".format(datetime.now().strftime("%Y/%m/%d - %I:%M %p")) +
                "━━━━━━━━━━━━━━━━━━━━\n\n"
                "• `.السورس` - عرض  قاىمة الاوامر\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "🦅 سورس الطائي V2 يعمل الآن.."
            )
        )
        print(" تم إرسال رسالة التشغيل إلى المحفوظات.")
    except Exception as e:
        print(f" فشل إرسال رسالة التشغيل: {e}")


import time

import time
import os
from datetime import datetime
import pytz
from telethon import events, functions, types

# نستخدم الترتيب 0 (الأولوية) لضمان استجابة الأمر قبل أي دالة أخرى
@client.on(events.NewMessage(pattern=r"\.فحص"))
async def check_source(event):
    if event.sender_id != owner_id:
        return 

    # 1. حساب سرعة الاستجابة (Ping)
    start_time = time.time()
    msg = await event.reply("🔍 **جاري فحص سورس الطائي...**")
    end_time = time.time()
    ping = round((end_time - start_time) * 1000)

    # 2. جلب معلومات الحساب
    me = await client.get_me()
    name = f"{me.first_name} {me.last_name or ''}"
    username = f"@{me.username}" if me.username else "لا يوجد"
    user_id = me.id

    # 3. جلب الوقت والتاريخ بتوقيت بغداد
    tz = pytz.timezone('Asia/Baghdad')
    now = datetime.now(tz)
    date_str = now.strftime("%Y/%m/%d")
    time_str = now.strftime("%I:%M %p").replace("AM", "ص").replace("PM", "م")

    # 4. النص البرمجي المنسق
    caption = (
        f"🙋‍♂️ **أهلاً بك في فحص سورس الطائي**\n"
        f"─── • ⚡️ • ───\n"
        f"👤 **الاسم:** {name}\n"
        f"🆔 **الايدي:** `{user_id}`\n"
        f"🔗 **اليوزر:** {username}\n"
        f"─── • 🌍 • ───\n"
        f"🚀 **سرعة السيرفر:** `{ping}ms`\n"
        f"📅 **التاريخ:** {date_str}\n"
        f"⏰ **الوقت (بغداد):** {time_str}\n"
        f"─── • ⚙️ • ───\n"
        f"🤖 **حالة الرد:** {'مفعل ✅' if 'auto_reply_enabled' in globals() and auto_reply_enabled else 'معطل ❌'}\n"
        f"✍️ **الخط العريض:** {'مفعل ✅' if 'bold_text_enabled' in globals() and bold_text_enabled else 'معطل ❌'}\n"
        f"🕒 **الاسم الوقتي:** {'مفعل ✅' if 'name_update_enabled' in globals() and name_update_enabled else 'معطل ❌'}\n"
        f"─── • 💠 • ───\n"
        f"**سورس الطائي V2 🦅**"
    )

    try:
        # جلب صورة البروفايل وحذفها بعد الإرسال لتوفير مساحة
        photo = await client.download_profile_photo(me.id)
        if photo:
            await client.send_file(event.chat_id, photo, caption=caption)
            await msg.delete()
            if os.path.exists(photo):
                os.remove(photo)
        else:
            await msg.edit(caption)
    except Exception as e:
        # في حال حدوث أي خطأ يرسل النص فقط لضمان عمل الدالة
        await msg.edit(caption + f"\n\n⚠️ (ملاحظة: تعذر جلب الصورة)")

# --- ملاحظة هامة جداً ---
# تأكد أن هذا السطر موجود في آخر سطر بالملف تماماً:
# client.run_until_disconnected()
import time
import asyncio

# --- [ إعدادات وضع النوم ] ---
is_sleeping = False
sleep_reason = ""
sleep_start_time = 0
missed_messages = [] # قائمة لحفظ من راسلك

# --- [ 1. أمر تفعيل وضع النوم ] ---
# الاستخدام: .سليب (دقائق) (السبب) | مثال: .سليب 30 غداء
@client.on(events.NewMessage(pattern=r"\.سليب (\d+) (.+)"))
async def set_sleep(event):
    if event.sender_id != owner_id: return
    
    global is_sleeping, sleep_reason, sleep_start_time, sleep_duration, missed_messages
    
    sleep_duration = int(event.pattern_match.group(1)) # حفظ المدة الكلية
    sleep_reason = event.pattern_match.group(2).strip()
    sleep_start_time = time.time()
    missed_messages = []
    is_sleeping = True
    
    await event.respond(f"💤 **تم تفعيل وضع النوم لمدة {sleep_duration} دقيقة.**\n📝 **السبب:** {sleep_reason}")
    
    await asyncio.sleep(sleep_duration * 60)
    if is_sleeping:
        await wakeup(event)


# --- [ 2. أمر الاستيقاظ وعرض السجل ] ---
@client.on(events.NewMessage(pattern=r"\.صحيت"))
async def wakeup(event):
    if event.sender_id != owner_id: return
    global is_sleeping, missed_messages
    
    if not is_sleeping:
        return await event.respond("🧐 أنت مستيقظ بالفعل!")

    is_sleeping = False
    report = "☀️ **أهلاً بعودتك! تم إيقاف وضع النوم.**\n\n"
    
    if missed_messages:
        report += "📋 **قائمة الأشخاص الذين راسلوك:**\n"
        for user, msg in missed_messages:
            report += f"👤 **{user}**: `{msg}`\n"
    else:
        report += "✨ لم يراسلـك أحد أثناء غيابك."
    
    await event.respond(report)
    missed_messages = []

# --- [ 3. المحرك الشامل (نوم + ردود) ] ---
# نحتاج تخزين مدة النوم الكلية في متغير عام
sleep_duration = 0 

@client.on(events.NewMessage(incoming=True))
async def global_responder(event):
    global is_sleeping, sleep_reason, sleep_start_time, sleep_duration, missed_messages, auto_reply_enabled2, keywords
    
    sender = await event.get_sender()
    if not sender or getattr(sender, 'bot', False) or event.sender_id == owner_id:
        return

    # --- [ نظام وضع النوم مع عد تنازلي ] ---
    if is_sleeping:
        if event.is_private or event.mentioned:
            # حفظ الرسالة في السجل
            user_name = sender.first_name or "مستخدم مجهول"
            missed_messages.append((user_name, event.raw_text))
            
            # حساب الوقت المنقضي والمتبقي
            elapsed_time = time.time() - sleep_start_time
            remaining_time = (sleep_duration * 60) - elapsed_time
            
            if remaining_time < 0: remaining_time = 0 # لضمان عدم ظهور أرقام سالبة
            
            rem_minutes = int(remaining_time // 60)
            rem_seconds = int(remaining_time % 60)
            
            sleep_msg = (
                f"💤 **عذراً، المالك في وضع النوم حالياً.**\n"
                f"─── • 💠 • ───\n"
                f"📝 **السبب:** {sleep_reason}\n"
                f"⏳ **الوقت المتبقي للعودة:** `{rem_minutes}` دقيقة و `{rem_seconds}` ثانية.\n"
                f"─── • 💠 • ───\n"
                f"💡 سيتم إبلاغه برسالتك فور استيقاظه."
            )
            return await event.reply(sleep_msg)

    # --- [ نظام الردود التلقائية ] ---
    if not is_sleeping and auto_reply_enabled2 and event.is_private:
        text = event.raw_text.strip()
        if text in keywords:
            await event.reply(keywords[text])
# --- [ أمر عرض تعليمات نظام النوم ] ---
@client.on(events.NewMessage(pattern=r"\.اوامر النوم"))
async def sleep_help(event):
    if event.sender_id != owner_id:
        return

    help_text = (
        "💤 **قائمة أوامر نظام النوم (AFK):**\n"
        "─── • 💠 • ───\n"
        "🔹 **تفعيل الوضع:**\n"
        "• `.سليب (الدقائق) (السبب)`\n"
        "💡 *مثال:* `.سليب 30 غداء` \n"
        "*(سيفعل النوم لمدة 30 دقيقة ويخبر الناس بالسبب)*\n\n"
        "🔹 **إلغاء الوضع:**\n"
        "• `.صحيت` \n"
        "*(لإيقاف الوضع يدوياً وعرض سجل الرسائل)*\n"
        "─── • 💠 • ───\n"
        "⚙️ **مميزات النظام:**\n"
        "1️⃣ **العد التنازلي:** يخبر من يراسلك بالوقت المتبقي لعودتك بالدقيقة والثانية.\n"
        "2️⃣ **سجل الغياب:** عند استيقاظك، يرسل لك قائمة بأسماء الأشخاص ورسائلهم.\n"
        "3️⃣ **كشف المنشن:** الرد يعمل في الخاص وأيضاً عند الإشارة إليك (@) في المجموعات.\n"
        "4️⃣ **الاستيقاظ الذكي:** ينتهي الوضع تلقائياً فور انتهاء الوقت المحدد.\n"
        "─── • 🦅 • ───"
    )
    
    await event.respond(help_text)

import os

# متغير للتحكم بتشغيل/إطفاء التخزين
storage_enabled = True
target_group_id = -1003374397792

# --- [ أمر تفعيل وتعطيل التخزين ] ---
@client.on(events.NewMessage(pattern=r"\.تخزين (تفعيل|تعطيل)"))
async def toggle_storage(event):
    if event.sender_id != owner_id: return
    global storage_enabled
    action = event.pattern_match.group(1)
    storage_enabled = (action == "تفعيل")
    await event.respond(f"✅ تم **{action}** نظام التخزين الشامل.")

# --- [ محرك التخزين والتحويل ] ---
@client.on(events.NewMessage(incoming=True))
async def storage_engine(event):
    global storage_enabled, target_group_id
    
    if not storage_enabled or event.sender_id == owner_id:
        return

    # الشروط: (رسالة بالخاص) أو (تاك بالمجموعات) أو (رد على رسالتك)
    is_reply_to_me = False
    if event.is_group and event.reply_to_msg_id:
        reply_msg = await event.get_reply_message()
        if reply_msg and reply_msg.sender_id == owner_id:
            is_reply_to_me = True

    if event.is_private or event.mentioned or is_reply_to_me:
        sender = await event.get_sender()
        name = sender.first_name if sender else "مجهول"
        username = f"@{sender.username}" if sender and sender.username else "لا يوجد"
        user_id = event.sender_id
        
        # تحديد نوع المحتوى
        content_type = "نص 📝"
        if event.photo: content_type = "صورة 🖼"
        elif event.video: content_type = "فيديو 🎬"
        elif event.voice: content_type = "بصمة صوت 🎤"
        elif event.audio: content_type = "ملف صوتي 🎵"
        elif event.sticker: content_type = "ملصق 🎭"
        elif event.document: content_type = "ملف/مستند 📄"
        elif event.video_note: content_type = "رسالة فيديو (نوت) 📹"

        # تجهيز كليشة المعلومات
        info_text = (
            f"📥 **رسالة جديدة للتخزين:**\n"
            f"─── • 💠 • ───\n"
            f"👤 **الاسم:** {name}\n"
            f"🆔 **الايدي:** `{user_id}`\n"
            f"🔗 **اليوزر:** {username}\n"
            f"📂 **النوع:** {content_type}\n"
            f"📍 **المصدر:** {'خاص 👤' if event.is_private else 'مجموعة 👥'}\n"
            f"─── • 💠 • ───\n"
            f"💬 **المحتوى:**\n"
        )

        try:
            # التحويل إلى كروب التخزين
            if event.message.text and not event.media:
                # إذا كانت رسالة نصية فقط
                await client.send_message(target_group_id, info_text + f" {event.raw_text}")
            else:
                # إذا كانت ميديا (صورة، فيديو، الخ)
                await client.send_message(target_group_id, info_text)
                await client.forward_messages(target_group_id, event.message)
        except Exception as e:
            print(f"خطأ في التخزين: {e}")


from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.errors import UsernameOccupiedError, UsernameInvalidError
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تحكم الحساب"))
async def help_cmd(event):
    help_text = """
**🚀 أوامر سورس التحكم الشامل (Userbot):**
─── • 💠 • ───
🔹 **الحساب الشخصي:**
• `.معلوماتي` : عرض معلومات حسابك.
• `.اسم (الاسم)` : تغيير اسمك.
• `.بايو (الوصف)` : تغيير البايو.
• `.يوزر (اليوزر)` : تغيير اليوزرنيم.

🔹 **المجموعات والقنوات:**
• `.انضم (رابط/يوزر)` : انضمام سريع.
• `.غادر (يوزر)` : مغادرة القناة/الكروب.
• `.صنع قناة (الاسم)` : إنشاء قناة جديدة.
• `.صنع كروب (الاسم)` : إنشاء مجموعة.

🔹 **الخصوصية والجلسات:**
• `.الجلسات` : عرض الأجهزة المتصلة بحسابك.
• `.انهاء (رقم)` : تسجيل خروج لجهاز معين.

🔹 **أوامر عامة:**
• `.فحص` : للتأكد أن السورس يعمل.
• `صنع بوت الاسم - اليوزر `: انشاء بوت في التلجرام.

**جميع الاوامر لا تحتاج الى @ 🤍 **

─── • 🦅 • ───
**سورس الطائي**
"""
    await event.edit(help_text)
# أمر تغيير الاسم
@client.on(events.NewMessage(outgoing=True, pattern=r"\.اسم (.+)"))
async def change_name(event):
    new_name = event.pattern_match.group(1)
    first_name = new_name.split(' ', 1)[0]
    last_name = new_name.split(' ', 1)[1] if ' ' in new_name else ''
    await client(UpdateProfileRequest(first_name=first_name, last_name=last_name))
    await event.edit(f"✅ تم تغيير الاسم إلى: **{new_name}**")

# أمر عرض الجلسات النشطة
@client.on(events.NewMessage(outgoing=True, pattern=r"\.الجلسات"))
async def list_sessions(event):
    authorizations = await client(GetAuthorizationsRequest())
    msg = "**💻 الأجهزة المتصلة بحسابك:**\n\n"
    for i, auth in enumerate(authorizations.authorizations):
        msg += f"{i+1}. {auth.device_model} | {auth.country}\n"
    await event.edit(msg)

# أمر الانضمام
@client.on(events.NewMessage(outgoing=True, pattern=r"\.انضم (.+)"))
async def join_chat(event):
    link = event.pattern_match.group(1)
    try:
        if "+" in link or "joinchat" in link:
            hash_link = link.split('/')[-1].replace('+', '')
            await client(ImportChatInviteRequest(hash_link))
        else:
            await client(JoinChannelRequest(link))
        await event.edit(f"✅ تم الانضمام بنجاح إلى: {link}")
    except Exception as e:
        await event.edit(f"❌ خطأ: {e}")
# --- [ 1. أمر معلوماتي - معلومات الحساب ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.معلوماتي"))
async def my_info(event):
    me = await client.get_me()
    full_user = await client(GetFullUserRequest(me.id))
    bio = full_user.full_user.about or "لا يوجد"
    
    info = (
        f"🙋‍♂️ **معلومات حسابك الشخصي:**\n"
        f"─── • 💠 • ───\n"
        f"👤 **الاسم:** {me.first_name} {me.last_name or ''}\n"
        f"🆔 **الايدي:** `{me.id}`\n"
        f"🔗 **اليوزر:** @{me.username or 'لا يوجد'}\n"
        f"📝 **البايو:** {bio}\n"
        f"─── • 🦅 • ───"
    )
    await event.edit(info)

# --- [ 2. تغيير البايو واليوزر ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.بايو (.+)"))
async def set_bio(event):
    new_bio = event.pattern_match.group(1)
    await client(UpdateProfileRequest(about=new_bio))
    await event.edit(f"✅ تم تغيير البايو إلى: \n`{new_bio}`")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.يوزر (.+)"))
async def set_username(event):
    # تنظيف اليوزر من @ والمسافات
    new_un = event.pattern_match.group(1).strip().replace("@", "")
    
    # فحص الطول (تليجرام يتطلب 5 أحرف على الأقل)
    if len(new_un) < 5:
        return await event.edit("❌ **خطأ:** اليوزرنيم قصير جداً، يجب أن يكون 5 أحرف أو أكثر.")

    try:
        await client(UpdateUsernameRequest(new_un))
        await event.edit(f"✅ **تم تغيير اليوزرنيم بنجاح!**\n🔗 اليوزر الجديد: @{new_un}")
    
    except UsernameOccupiedError:
        await event.edit(f"❌ **للأسف:** اليوزر `@{new_un}` محجوز بالفعل، جرب يوزر ثاني.")
    
    except UsernameInvalidError:
        await event.edit("❌ **خطأ في التنسيق:** اليوزرنيم غير صالح (تأكد أنه يبدأ بحرف ولا يحتوي على رموز ممنوعة).")
    
    except Exception as e:
        # إذا كان هناك خطأ بسبب كثرة المحاولات (Flood)
        if "Wait" in str(e):
            await event.edit("⏳ **انتظر قليل:** لقد حاولت تغيير اليوزر كثيراً، تليجرام حظرك مؤقتاً.")
        else:
            await event.edit(f"❌ **حدث خطأ غير متوقع:**\n`{str(e)}`")

# --- [ 3. المغادرة وصنع القنوات/الكروبات ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.غادر (.+)"))
async def leave(event):
    target = event.pattern_match.group(1)
    await client(LeaveChannelRequest(target))
    await event.edit(f"🏃‍♂️ تم مغادرة: {target}")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.صنع (قناة|كروب) (.+)"))
async def create_chat(event):
    mode = event.pattern_match.group(1)
    title = event.pattern_match.group(2)
    is_group = True if mode == "كروب" else False
    try:
        await client(CreateChannelRequest(title=title, about="تم الصنع بواسطة السورس", megagroup=is_group))
        await event.edit(f"✅ تم إنشاء {mode} بنجاح باسم: **{title}**")
    except Exception as e:
        await event.edit(f"❌ فشل الإنشاء: {e}")

# --- [ 4. إرسال رسالة لشخص (عبر اليوزر أو الايدي) ] ---
# الاستخدام: .ارسل @username النص أو .ارسل 123456 النص
@client.on(events.NewMessage(outgoing=True, pattern=r"\.ارسل (\S+) (.+)"))
async def send_to(event):
    target = event.pattern_match.group(1)
    message = event.pattern_match.group(2)
    try:
        # تحويل النص إلى رقم إذا كان ايدي
        target_id = int(target) if target.isdigit() else target
        await client.send_message(target_id, message)
        await event.edit(f"✅ تم إرسال الرسالة إلى: {target}")
    except Exception as e:
        await event.edit(f"❌ لم أستطع الإرسال: {e}")

# --- [ 5. صنع بوت عبر BotFather ] ---
# الاستخدام: .صنع بوت (الاسم) - (اليوزر)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.صنع بوت (.+) - (.+)"))
async def make_bot(event):
    name = event.pattern_match.group(1).strip()
    username = event.pattern_match.group(2).strip()
    await event.edit("⏳ جاري التواصل مع BotFather...")
    
    async with client.conversation("@BotFather") as conv:
        await conv.send_message("/newbot")
        await conv.get_response()
        await conv.send_message(name)
        await conv.get_response()
        await conv.send_message(username)
        res = await conv.get_response()
        
        if "Done!" in res.text:
            await event.edit(f"🎉 تم إنشاء البوت بنجاح!\n\n{res.text}")
        else:
            await event.edit(f"❌ حدث خطأ من BotFather:\n`{res.text}`")

async def main():
    await client.start()
    print("✅ السورس يعمل الآن داخل حسابك الشخصي!")
    await client.run_until_disconnected()
from telethon.tl.functions.account import GetAuthorizationsRequest, ResetAuthorizationRequest

# --- [ 1. أمر عرض الجلسات النشطة ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.الجلسات"))
async def list_sessions(event):
    await event.edit("⏳ جاري جلب الجلسات النشطة...")
    try:
        authorizations = await client(GetAuthorizationsRequest())
        msg = "💻 **الأجهزة المتصلة بحسابك:**\n\n"
        
        for i, auth in enumerate(authorizations.authorizations):
            # تمييز الجلسة الحالية
            current = "👈 (هذه الجلسة)" if auth.current else ""
            msg += (
                f"{i+1}. **الجهاز:** `{auth.device_model}`\n"
                f"   **النظام:** `{auth.platform}`\n"
                f"   **الدولة:** `{auth.country}`\n"
                f"   **التاريخ:** `{auth.date_active.strftime('%Y-%m-%d')}` {current}\n"
                f"───\n"
            )
        
        msg += "\n💡 لإنهاء جلسة، أرسل: `.انهاء` + رقم الجلسة\nمثال: `.انهاء 2`"
        await event.edit(msg)
    except Exception as e:
        await event.edit(f"❌ فشل جلب الجلسات: {e}")

# --- [ 2. أمر إنهاء جلسة معينة ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.انهاء (\d+)"))
async def terminate_session(event):
    index = int(event.pattern_match.group(1)) - 1
    await event.edit(f"⏳ جاري محاولة إنهاء الجلسة رقم {index + 1}...")
    
    try:
        authorizations = await client(GetAuthorizationsRequest())
        
        if index < 0 or index >= len(authorizations.authorizations):
            return await event.edit("❌ رقم الجلسة غير صحيح، تأكد من القائمة باستخدام أمر `.الجلسات`")
        
        target_auth = authorizations.authorizations[index]
        
        if target_auth.current:
            return await event.edit("⚠️ لا يمكنك إنهاء الجلسة الحالية التي تستخدمها الآن!")

        # تنفيذ إنهاء الجلسة باستخدام الـ hash الخاص بها
        await client(ResetAuthorizationRequest(hash=target_auth.hash))
        await event.edit(f"✅ تم إنهاء الجلسة بنجاح:\n🖥 **الجهاز:** `{target_auth.device_model}`\n📍 **الدولة:** `{target_auth.country}`")
        
    except Exception as e:
        await event.edit(f"❌ حدث خطأ أثناء محاولة إنهاء الجلسة:\n`{str(e)}` \n\n*ملاحظة: تليجرام قد يتطلب أن تكون الجلسة الحالية نشطة لعدة أيام قبل السماح بإنهاء الجلسات الأخرى.*")
from telethon import events
from datetime import datetime
import requests
import re
import asyncio

# --- [ جلب التاريخ الهجري ] ---
def get_hijri_date():
    try:
        url = "https://www.sistani.org"
        headers = {'User-Agent': "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        res = re.search(r'style="margin-left:9px;">([^<]+)</span>', response.text)
        return res.group(1).strip() if res else "غير متوفر"
    except:
        return "غير متوفر"

# --- [ 1. أمر الخدمات الرئيسي ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.الخدمات الترفيهية"))
async def services_menu(event):
    now = datetime.now()
    hijri = get_hijri_date()

    msg = (
        f"<b>🌟 قائمة الخدمات الذكية</b>\n"
        f"─── • 💠 • ───\n"
        f"📅 <b>هجري:</b> {hijri}\n"
        f"📅 <b>ميلادي:</b> {now.strftime('%Y/%m/%d')}\n"
        f"⏰ <b>الوقت:</b> {now.strftime('%I:%M %p')}\n"
        f"─── • 💠 • ───\n\n"
        f"<b>📌 الأوامر المتاحة:</b>\n\n"
        f"📖 القرآن الكريم:\n"
        f"↳ <code>.ص رقم</code>\n"
        f"مثال: <code>.ص 100</code>\n\n"
        f"🎬 تحميل تيك توك:\n"
        f"↳ <code>.تيك رابط</code>\n\n"
        f"🤖 اسأل الذكاء الاصطناعي:\n"
        f"↳ <code>.سوال سؤالك</code>\n\n"
        f"📋 المهام:\n"
        f"↳ <code>.مهمة نص</code>\n"
        f"↳ <code>.مهامي</code>\n\n"
        f"👨‍💻 المطور:\n"
        f"↳ https://t.me/altaee_z"
    )

    await event.edit(msg, parse_mode="html")

# --- [ 2. خدمة ChatGPT ] ---

MEMORY_FILE = "gpt_memory.json"
STATE_FILE = "gpt_state.json"

# ======================
# حالة الذكاء
# ======================
def load_state():
    if not os.path.exists(STATE_FILE):
        return {"enabled": False}
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False)

# ======================
# الذاكرة
# ======================
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(mem):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(mem, f, ensure_ascii=False, indent=2)

def get_history(chat_id, limit=6):
    mem = load_memory()
    return mem.get(str(chat_id), [])[-limit:]

def add_history(chat_id, q, a):
    mem = load_memory()
    cid = str(chat_id)
    if cid not in mem:
        mem[cid] = []
    mem[cid].append({"q": q, "a": a})
    mem[cid] = mem[cid][-12:]
    save_memory(mem)

# ======================
# أوامر التشغيل (OWNER فقط)
# ======================
@client.on(events.NewMessage(pattern=r"\.ذكاء تشغيل"))
async def enable_ai(event):
    if event.sender_id != owner_id:
        await event.reply("❌ هذا الأمر للمالك فقط")
        return

    save_state({"enabled": True})
    await event.reply("🧠 تم تشغيل الذكاء")

@client.on(events.NewMessage(pattern=r"\.ذكاء ايقاف"))
async def disable_ai(event):
    if event.sender_id != owner_id:
        await event.reply("❌ هذا الأمر للمالك فقط")
        return

    save_state({"enabled": False})
    await event.reply("⛔ تم إيقاف الذكاء")

# ======================
# أمر الذكاء (.س)
# ======================
@client.on(events.NewMessage(pattern=r"\.س (.+)"))
async def ai_command(event):
    state = load_state()
    if not state.get("enabled"):
        return

    sender = await event.get_sender()
    if sender.bot:
        return

    question = event.pattern_match.group(1)
    chat_id = event.chat_id

    # رد فوري
    wait_msg = await event.reply("⏳ تم استلام سؤالك، انتظر شوي...")

    # مؤشر تفكير
    async with client.action(event.chat_id, "typing"):
        await asyncio.sleep(2)

        history = get_history(chat_id)
        memory_text = ""
        for h in history:
            memory_text += f"سؤال: {h['q']}\nجوابك: {h['a']}\n"

        prompt = (
            "إنت شخص عراقي تحچي طبيعي، "
            "جاوب بدون ذكر ذكاء اصطناعي أو بوت، "
            "وكمّل على السوالف السابقة إذا موجودة.\n\n"
            f"{memory_text}\n"
            f"السؤال الجديد:\n{question}"
        )

        try:
            r = requests.get(
                f"https://chatgpt.apinepdev.workers.dev/?question={requests.utils.quote(prompt)}",
                timeout=25
            ).json()

            answer = r.get("answer", "ما عندي جواب مضبوط هسه 😅")
            answer = answer.replace(
                "🔗 Join our community: [t.me/nepdevsz](https://t.me/nepdevsz)", ""
            )

            add_history(chat_id, question, answer)

            await wait_msg.delete()
            await event.reply(answer)

        except:
            await wait_msg.edit("❌ صار خطأ، جرّب مرة ثانية")

# ======================
print(" الذكاء العراقي شغال وبإدارة المالك...")

# --- [ 4. خدمة القرآن الكريم ] ---
@client.on(events.NewMessage(outgoing=True, pattern=r"\.ص (\d+)"))
async def quran_cmd(event):
    page = int(event.pattern_match.group(1))
    if 1 <= page <= 604:
        url = f"https://quran.ksu.edu.sa/png_big/{page}.png"
        await event.client.send_file(
            event.chat_id,
            url,
            caption=f"📖 الصفحة رقم {page}"
        )
        await event.delete()
    else:
        await event.edit("❌ رقم الصفحة يجب أن يكون بين 1 و 604.")
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تيك (.+)"))
async def tiktok_cmd(event):
    url = event.pattern_match.group(1)
    await event.edit("⏳ جاري تحميل فيديو تيك توك...")

    try:
        headers = {
            "referer": "https://lovetik.com/sa/video/",
            "origin": "https://lovetik.com",
            "user-agent": "Mozilla/5.0"
        }
        payload = {"query": url}
        r = requests.post(
            "https://lovetik.com/api/ajax/search",
            headers=headers,
            data=payload,
            timeout=10
        ).json()

        video_url = r["links"][2]["a"]

        await event.client.send_file(
            event.chat_id,
            video_url,
            caption="✅ تم تحميل الفيديو\n🤍 سورس الطائي"
        )
        await event.delete()

    except Exception as e:
        await event.edit("❌ فشل تحميل الفيديو، تأكد من الرابط.")   
DATA_FILE = "tasks_data.json"             
def load_tasks():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_tasks(user_id):
    data = load_tasks()
    return data.get(str(user_id), [])

def set_tasks(user_id, tasks):
    data = load_tasks()
    data[str(user_id)] = tasks
    save_tasks(data)
@client.on(events.NewMessage(outgoing=True, pattern=r"\.مهمة (.+)"))
async def add_task(event):
    text = event.pattern_match.group(1)
    uid = str(event.sender_id)

    tasks = get_tasks(uid)
    tasks.append({"text": text, "done": False})
    set_tasks(uid, tasks)

    await event.edit(f"✅ تمت إضافة المهمة:\n• {text}")
@client.on(events.NewMessage(outgoing=True, pattern=r"\.مهامي"))
async def list_tasks(event):
    uid = str(event.sender_id)
    tasks = get_tasks(uid)

    if not tasks:
        await event.edit("📋 لا توجد مهام حالياً.")
        return

    msg = "<b>📋 مهامك:</b>\n\n"
    for i, t in enumerate(tasks, 1):
        status = "✅" if t["done"] else "◻️"
        msg += f"{i}. {status} {t['text']}\n"

    msg += "\nاستخدم:\n.تم رقم\n.حذف رقم\n.مسح_الكل"
    await event.edit(msg, parse_mode="html")
@client.on(events.NewMessage(outgoing=True, pattern=r"\.تم (\d+)"))
async def done_task(event):
    idx = int(event.pattern_match.group(1)) - 1
    uid = str(event.sender_id)
    tasks = get_tasks(uid)

    if 0 <= idx < len(tasks):
        tasks[idx]["done"] = True
        set_tasks(uid, tasks)
        await event.edit("✅ تم إنجاز المهمة.")
    else:
        await event.edit("❌ رقم مهمة غير صحيح.")
@client.on(events.NewMessage(outgoing=True, pattern=r"\.حذف (\d+)"))
async def delete_task(event):
    idx = int(event.pattern_match.group(1)) - 1
    uid = str(event.sender_id)
    tasks = get_tasks(uid)

    if 0 <= idx < len(tasks):
        removed = tasks.pop(idx)
        set_tasks(uid, tasks)
        await event.edit(f"🗑️ تم حذف: {removed['text']}")
    else:
        await event.edit("❌ رقم مهمة غير صحيح.")
@client.on(events.NewMessage(outgoing=True, pattern=r"\.مسح_الكل"))
async def clear_tasks(event):
    set_tasks(str(event.sender_id), [])
    await event.edit("🧹 تم مسح جميع المهام.")     


client.start()
client.run_until_disconnected()                                   
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
