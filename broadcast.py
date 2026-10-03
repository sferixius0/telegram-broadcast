import asyncio
import os
import random
import base64
from telethon import TelegramClient
from messages import MESSAGES

# ===== НАСТРОЙКИ =====
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
PHONE = os.environ["PHONE"]
SESSION_B64 = os.environ["SESSION_B64"]

# ===== СПИСОК ГРУПП =====
GROUPS = [
    # Полоцк / Новополоцк
    "baraholkapnpn",
    "baraholkapolostknovopolotsk",
    "baraholkapnp",
    "baraholkapolostknp",
    "baraholkapolostknp0",
    "barakholka_polotsk",
    "SmokeHub_baraholka_Polotsk",
    # Минск / РБ
    "onlyvapebel",
    "minsk_vape7",
    # Другие
    "barakholka1",
    "baraholka_v_rb",
    "baraholka_ge",
]
# =====================

async def main():
    # Восстанавливаем сессию из base64
    with open("userbot_session.session", "wb") as f:
        f.write(base64.b64decode(SESSION_B64))

    client = TelegramClient("userbot_session", API_ID, API_HASH)
    await client.start(phone=PHONE)
    print("✅ Аккаунт подключён")

    # Загружаем индекс (какой шаблон отправить следующим)
    try:
        with open("last_index.txt", "r") as f:
            index = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        index = 0

    # Берём текст по индексу
    message_text = MESSAGES[index % len(MESSAGES)]
    print(f"📨 Отправляем шаблон #{index % len(MESSAGES) + 1} из {len(MESSAGES)}")

    # Рассылка по списку групп
    for i, group in enumerate(GROUPS):
        try:
            await client.send_message(group, message_text)
            print(f"[{i+1}/{len(GROUPS)}] ✅ {group}")
        except Exception as e:
            print(f"[{i+1}/{len(GROUPS)}] ❌ {group} — {e}")
        # Пауза между группами, чтобы не спалиться
        await asyncio.sleep(random.randint(30, 90))

    # Сохраняем следующий индекс
    with open("last_index.txt", "w") as f:
        f.write(str(index + 1))

    print("✅ Рассылка завершена!")
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
