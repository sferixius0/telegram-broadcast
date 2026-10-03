import asyncio
import os
import base64
from telethon import TelegramClient
from messages import MESSAGES

# ===== НАСТРОЙКИ =====
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
PHONE = os.environ["PHONE"]
SESSION_B64 = os.environ["SESSION_B64"]

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
    # Восстанавливаем файл сессии из секрета
    with open("userbot_session.session", "wb") as f:
        f.write(base64.b64decode(SESSION_B64))

    client = TelegramClient("userbot_session", API_ID, API_HASH)
    await client.start(phone=PHONE)
    print("✅ Аккаунт подключён")

    # Берём шаблон по индексу
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
