import os
import time
import requests
from io import BytesIO
from PIL import Image

# ─────────── НАСТРОЙКИ ───────────
QUERY      = "cheese"    # поисковая фраза (в нашем случае «cheese»)
NUM_IMAGES = 30          # скольких файлов хотим сохранить
SAVE_DIR   = os.path.join(os.path.dirname(__file__), "cheese-folder")
os.makedirs(SAVE_DIR, exist_ok=True)

# User-Agent нужен, чтобы не получить 403 с Wikimedia:
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/113.0.0.0 Safari/537.36"
}


def fetch_commons_image_urls(search_term: str, limit: int) -> list:
    """
    Достаём прямые URL-ы файлов из Wikimedia Commons:
    - generator=search с gsrnamespace=6 (только файлы),
      gsrsearch=<search_term>, gsrlimit=<limit>
    - prop=imageinfo&iiprop=url
    Возвращает список до `limit` URL-ов (strings).
    """
    endpoint = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": search_term,
        "gsrnamespace": "6",   # 6 = File:
        "gsrlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }

    try:
        resp = requests.get(endpoint, params=params, headers=HEADERS, timeout=10)
    except Exception as e:
        raise RuntimeError(f"Не удалось запросить API Commons: {e}")

    if resp.status_code != 200:
        raise RuntimeError(f"Commons API вернул HTTP {resp.status_code}")

    data = resp.json()

    pages = data.get("query", {}).get("pages", {})
    urls = []
    for pageid, page in pages.items():
        info = page.get("imageinfo")
        if info and isinstance(info, list):
            # Берём первый элемент imageinfo (index 0) и поле 'url'
            url = info[0].get("url", "")
            if url:
                urls.append(url)
        if len(urls) >= limit:
            break

    return urls[:limit]


def download_and_save(image_url: str, count: int) -> bool:
    """
    Скачиваем картинку по image_url, пытаемся конвертировать через Pillow в JPEG
    и сохраняем как '{QUERY}_{count}.jpg'.
    Если Pillow не смог открыть (например, WEBP/PNG), просто пишем байты «как есть».
    Возвращаем True, если файл успешно попал в папку, иначе False.
    """
    try:
        resp = requests.get(image_url, headers=HEADERS, timeout=10)
    except Exception as e:
        print(f"    ❌ Ошибка запроса {image_url}: {e}")
        return False

    if resp.status_code != 200:
        print(f"    ❌ HTTP {resp.status_code} при скачивании {image_url}")
        return False

    filename = f"{QUERY}_{count}.jpg"
    path = os.path.join(SAVE_DIR, filename)

    # Пробуем через Pillow
    try:
        img = Image.open(BytesIO(resp.content)).convert("RGB")
        img.save(path, "JPEG", quality=90)
    except Exception as e:
        # Если Pillow не смог (WEBP, PNG), просто сохраняем байты как есть
        print(f"    ⚠️ PIL не смог открыть {image_url}. Сохраняем «как есть»: {e}")
        try:
            with open(path, "wb") as f:
                f.write(resp.content)
        except Exception as e2:
            print(f"    ❌ Не удалось записать файл {path}: {e2}")
            return False

    return True


if __name__ == "__main__":
    try:
        print(f"🔍 Запрашиваем из Wikimedia Commons первые {NUM_IMAGES} изображений по «{QUERY}»…")
        image_urls = fetch_commons_image_urls(QUERY, NUM_IMAGES)
        print(f"✅ Получено {len(image_urls)} URL-ов.")

        if not image_urls:
            print("⚠️ Не удалось получить ни одного URL-а из Commons. Возможно, изменился API.")
            exit(1)

        saved = 0
        for idx, url in enumerate(image_urls, start=1):
            print(f"   Скачиваем #{idx}: {url}")
            ok = download_and_save(url, idx)
            if ok:
                print(f"   ✅ Сохранили как {QUERY}_{idx}.jpg")
                saved += 1
            else:
                print(f"   ❌ Не удалось сохранить #{idx}")
            # Лёгкая пауза, чтобы не «прессовать» сервер
            time.sleep(0.2)

        print(f"\n🎉 ГОТОВО: сохранено {saved} файлов → {os.path.abspath(SAVE_DIR)}")
    except Exception as e:
        print("❗️Ошибка выполнения скрипта:", e)
