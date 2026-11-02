import os
from threading import Thread
from flask import Flask

# --- Render portini aldash uchun veb-server ---
app = Flask('')


@app.route('/')
def home():
  return 'Bot xatosiz ishlayapti!'


def run():
  port = int(os.environ.get('PORT', 8080))
  app.run(host='0.0.0.0', port=port)


# Veb-serverni alohida fonda ishga tushirish
Thread(target=run).start()
# ----------------------------------------------

# Shundan pastda O'ZINGIZNING BOTINGIZ KODI davom etadi:
import asyncio
import json
import os
import re

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject
from aiogram.enums import ParseMode

TOKEN = "8780750723:AAH5BLYo0bQ4ly4LCbZU-T9cCWadAs7Icoc"      
ADMINS = {8655854506, 6119869771}                        

BASE = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE, "schedule.json")

bot = Bot(token=TOKEN)
dp = Dispatcher()

PATTERN = re.compile(r"(?:ячейк\w*|yacheyk\w*)\s*[№#]?\s*(\d+)", re.I)


def load():
    with open(FILE, encoding="utf-8") as f:
        return json.load(f)


def save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


def is_admin(m: types.Message):
    return m.from_user.id in ADMINS


def in_cells(cell, rules):
    for r in rules:
        r = str(r)
        if "-" in r:
            a, b = r.split("-")
            if int(a) <= cell <= int(b):
                return True
        elif int(r) == cell:
            return True
    return False


def find_people(cell):
    data = load()
    return [
        (role, p)
        for role in ("brigadir", "texnolog")
        for p in data.get(role, [])
        if in_cells(cell, p["cells"])
    ]

@dp.message(Command("id"))
async def my_id(m: types.Message):
    if m.reply_to_message:
        u = m.reply_to_message.from_user
        await m.reply(f"{u.full_name}: {u.id}")
    else:
        await m.reply(f"Sizning ID: {m.from_user.id}")

@dp.message(Command("people"))
async def people(m: types.Message):
    if not is_admin(m):
        return
    data = load()
    text = ""
    for role in ("brigadir", "texnolog"):
        text += f"\n<b>{role}</b>\n"
        for p in data.get(role, []):
            text += f"{p['id']} | {p['name']} | {','.join(p['cells'])}\n"
    await m.answer(text[:4000], parse_mode=ParseMode.HTML)


@dp.message(Command("add"))
async def add(m: types.Message, command: CommandObject):
    if not is_admin(m):
        return
    try:
        role, uid, name, cells = [x.strip() for x in command.args.split("|")]
        assert role in ("brigadir", "texnolog")
        uid = int(uid)
        cells = [c.strip() for c in cells.split(",")]
    except Exception:
        await m.answer(
            "Format:\n/add brigadir | 123456 | Ali aka | 9421,9422,7000-7100"
        )
        return
    data = load()
    for r in data:
        data[r] = [p for p in data[r] if p["id"] != uid]
    data.setdefault(role, []).append({"id": uid, "name": name, "cells": cells})
    save(data)
    await m.answer(f"Saqlandi: {name} ({role})")


@dp.message(Command("del"))
async def delete(m: types.Message, command: CommandObject):
    if not is_admin(m):
        return
    try:
        uid = int(command.args)
    except Exception:
        await m.answer("Format: /del 123456")
        return
    data = load()
    for r in data:
        data[r] = [p for p in data[r] if p["id"] != uid]
    save(data)
    await m.answer("O'chirildi")
@dp.message(F.text | F.caption)
async def handle(m: types.Message):
    text = m.text or m.caption
    if not text:
        return
    cells = [int(x) for x in PATTERN.findall(text)]
    if not cells:
        return
    lines = []
    for cell in dict.fromkeys(cells):
        found = find_people(cell)
        if not found:
            lines.append(f"Ячейка {cell}: ⚠️ odam topilmadi")
            continue
        tags = []
        for role, p in found:
            tags.append(f'<a href="tg://user?id={p["id"]}">{p["name"]}</a>')
        lines.append(" ".join(tags))
    await m.reply("\n".join(lines), parse_mode=ParseMode.HTML)


async def main():
  await bot.delete_webhook(drop_pending_updates=True) 
  await dp.start_polling(bot)
if __name__ == "__main__": 
  asyncio.run(main())
