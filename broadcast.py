import asyncio
import os
import random
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError, UsernameNotOccupiedError, ChannelPrivateError
from messages import MESSAGES
from groups import GROUPS

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_B64 = os.environ["SESSION_B64"]
PHONE = os.environ.get("PHONE", "")

PAUSE_MIN = 180
PAUSE_MAX = 600

async def main():
    client = TelegramClient(StringSession(SESSION_B64), API_ID, API_HASH)
    await client.start(phone=PHONE or None)
    me = await client.get_me()
    print(f"✅ Подключён как @{me.username or me.id}")

    try:
        with open("last_index.txt") as f:
            index = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        index = 0

    msg_num = index % len(MESSAGES)
    message_text = MESSAGES[msg_num]
    print(f"📨 Шаблон #{msg_num + 1} из {len(MESSAGES)}")

    sent = failed = 0
    for i, group in enumerate(GROUPS, start=1):
        try:
            await client.send_message(group, message_text)
            print(f"[{i}/{len(GROUPS)}] ✅ {group}")
            sent += 1
        except FloodWaitError as e:
            print(f"⏳ FLOOD WAIT {e.seconds} сек — прерываю прогон.")
            break
        except UsernameNotOccupiedError:
            print(f"[{i}/{len(GROUPS)}] ❌ {group} — нет такого username")
            failed += 1
        except ChannelPrivateError:
            print(f"[{i}/{len(GROUPS)}] ❌ {group} — нет доступа")
            failed += 1
        except Exception as e:
            print(f"[{i}/{len(GROUPS)}] ❌ {group} — {type(e).__name__}: {e}")
            failed += 1

        if i < len(GROUPS):
            d = random.randint(PAUSE_MIN, PAUSE_MAX)
            print(f"   ⏸ {d} сек...")
            await asyncio.sleep(d)

    with open("last_index.txt", "w") as f:
        f.write(str(index + 1))

    print(f"\n📊 Итог: отправлено {sent}, ошибок {failed}")
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
