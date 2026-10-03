import asyncio
import os
from telethon import TelegramClient
from messages import MESSAGES

# ===== НАСТРОЙКИ (берутся из секретов GitHub) =====
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
PHONE = os.environ["PHONE"]

GROUPS = [
    "baraholkapnpn",
    "baraholkapolostknovopolotsk",
    "baraholkapnp",
    "baraholkapolostknp",
    "barakholka_polotsk",
    "SmokeHub_baraholka_Polotsk",
]

# =====================

async def main():
    client = TelegramClient("userbot_session", API_ID, API_HASH)
    await client.start(phone=PHONE)

    # Берём шаблон, который ещё не отправляли
    # Если файла с индексом нет — начинаем с 0
    try:
        with open("last_index.txt", "r") as f:
            index = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        index = 0

    message = MESSAGES[index % len(MESSAGES)]
    print(f"Отправляем шаблон #{index % len(MESSAGES) + 1}")

    for group in GROUPS:
        try:
            await client.send_message(group, message)
            print(f"[OK] {group}")
        except Exception as e:
            print(f"[ERR] {group}: {e}")
        await asyncio.sleep(30)

    # Сохраняем следующий индекс
    with open("last_index.txt", "w") as f:
        f.write(str(index + 1))

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
