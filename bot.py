import asyncio, json, re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

TOKEN = import asyncio, json, re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

TOKEN = "8780750723:AAGRAiRqInpw5Ywa4gAsU7FzcvGwMhRI6rk"
bot = Bot(token=TOKEN)
dp = Dispatcher()

PATTERN = re.compile(r"(?:ячейк\w*|yacheyk\w*)\s*[№#]?\s*(\d+)", re.I)

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
    with open("schedule.json", encoding="utf-8") as f:
        data = json.load(f)
    return [(role, p) for role in ("brigadir", "texnolog")
            for p in data[role] if in_cells(cell, p["cells"])]

@dp.message(Command("id"))
async def my_id(m: types.Message):
    if m.reply_to_message:
        u = m.reply_to_message.from_user
        await m.reply(f"{u.full_name}: {u.id}")
    else:
        await m.reply(f"Sizning ID: {m.from_user.id}")

@dp.message(lambda m: m.text)
async def handle(m: types.Message):
    cells = [int(x) for x in PATTERN.findall(m.text)]
    if not cells:
        return
    lines = []
    for cell in dict.fromkeys(cells):
        people = find_people(cell)
        if not people:
            lines.append(f"Ячейка {cell}: ⚠️ odam topilmadi")
            continue
        tags = []
        for role, p in people:
            tags.append(f'<a href="tg://user?id={p["id"]}">{p["name"]}</a>')
        lines.append(" ".join(tags))
    await m.reply("\n".join(lines), parse_mode=ParseMode.HTML)

asyncio.run(dp.start_polling(bot))""
bot = Bot(token=TOKEN)
dp = Dispatcher()

PATTERN = re.compile(r"(?:ячейк\w*|yacheyk\w*)\s*[№#]?\s*(\d+)", re.I)

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
    with open("schedule.json", encoding="utf-8") as f:
        data = json.load(f)
    return [(role, p) for role in ("brigadir", "texnolog")
            for p in data[role] if in_cells(cell, p["cells"])]

@dp.message(Command("id"))
async def my_id(m: types.Message):
    if m.reply_to_message:
        u = m.reply_to_message.from_user
        await m.reply(f"{u.full_name}: {u.id}")
    else:
        await m.reply(f"Sizning ID: {m.from_user.id}")

@dp.message(lambda m: m.text)
async def handle(m: types.Message):
    cells = [int(x) for x in PATTERN.findall(m.text)]
    if not cells:
        return
    lines = []
    for cell in dict.fromkeys(cells):
        people = find_people(cell)
        if not people:
            lines.append(f"Ячейка {cell}: ⚠️ odam topilmadi")
            continue
        tags = []
        for role, p in people:
            tags.append(f'<a href="tg://user?id={p["id"]}">{p["name"]}</a>')
        lines.append(" ".join(tags))
    await m.reply("\n".join(lines), parse_mode=ParseMode.HTML)

asyncio.run(dp.start_polling(bot))
