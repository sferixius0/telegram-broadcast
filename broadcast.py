import asyncio
import os
import random
import base64
from telethon import TelegramClient, functions
from messages import MESSAGES

# ===== НАСТРОЙКИ =====
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
PHONE = os.environ["PHONE"]
SESSION_B64 = os.environ["SESSION_B64"]

FOLDER_NAME = "барахолки"  # Имя папки в Telegram
# =====================

async def main():
    # Восстанавливаем сессию
    with open("userbot_session.session", "wb") as f:
        f.write(base64.b64decode(SESSION_B64))

    client = TelegramClient("userbot_session", API_ID, API_HASH)
    await client.start(phone=PHONE)
    print("✅ Аккаунт подключён")

    # 1. Находим папку по имени
    print(f"🔍 Ищем папку '{FOLDER_NAME}'...")
    filters_result = await client(functions.messages.GetDialogFiltersRequest())

    # Отладка: выводим все папки
    print("📋 Список всех папок:")
    for f in filters_result.filters:
        if hasattr(f, 'title'):
            print(f"  - '{f.title}' (ID: {getattr(f, 'id', '?')})")

    target_folder_id = None
    for f in filters_result.filters:
        if hasattr(f, 'title'):
            # title может быть строкой или TextWithEntities
            title = f.title.text if hasattr(f.title, 'text') else str(f.title)
            if title == FOLDER_NAME:
                target_folder_id = f.id
                print(f"✅ Папка найдена! ID: {target_folder_id}")
                break

    if target_folder_id is None:
        print(f"❌ Папка '{FOLDER_NAME}' не найдена!")
        await client.disconnect()
        return

    # 2. Получаем чаты напрямую из объекта папки
    print(f"📂 Извлекаем чаты из папки...")
    
    groups = []
    # Ищем нашу папку в списке еще раз, чтобы получить её объект
    target_folder_obj = None
    for f in filters_result.filters:
        if hasattr(f, 'title'):
            title = f.title.text if hasattr(f.title, 'text') else str(f.title)
            if title == FOLDER_NAME:
                target_folder_obj = f
                break
    
    if target_folder_obj:
        # include_peers содержит список чатов, которые вручную добавлены в папку
        for peer in target_folder_obj.include_peers:
            try:
                # Преобразуем InputPeer в полный объект чата
                entity = await client.get_entity(peer)
                groups.append(entity)
            except Exception as e:
                print(f"  [ERR] Не удалось получить чат: {e}")
    
    print(f"📊 Найдено чатов: {len(groups)}")
    
    if not groups:
        print("❌ В папке нет чатов.")
        await client.disconnect()
        return

    # 3. Загружаем индекс
    try:
        with open("last_index.txt", "r") as f:
            index = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        index = 0

    # 4. Рассылаем
    message_text = MESSAGES[index % len(MESSAGES)]
    print(f"📨 Отправляем шаблон #{index % len(MESSAGES) + 1}")

    for i, group in enumerate(groups):
        try:
            await client.send_message(group, message_text)
            print(f"[{i+1}/{len(groups)}] ✅ {getattr(group, 'title', 'Без названия')}")
        except Exception as e:
            print(f"[{i+1}/{len(groups)}] ❌ {getattr(group, 'title', 'Без названия')} — {e}")
        await asyncio.sleep(random.randint(30, 90))

    # 5. Сохраняем следующий индекс
    with open("last_index.txt", "w") as f:
        f.write(str(index + 1))

    print("✅ Рассылка завершена!")
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
