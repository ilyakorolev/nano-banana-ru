#!/usr/bin/env python3
"""
Nano Banana Pro Image Generator (Zero Dependencies)

Генерирует изображения через Gemini API на основе JSON спецификаций.
Работает без установки дополнительных пакетов — только stdlib Python 3.

Использование:
    python generate.py spec.json [--output image.png] [--model flash]

API ключ загружается автоматически из (в порядке приоритета):
    1. Переменная окружения GEMINI_API_KEY
    2. .env в текущей директории
    3. .env в директории скрипта
    4. ~/.env
    5. ~/.claude/.env

Формат .env файла:
    GEMINI_API_KEY=AIzaSy...

Получить ключ: https://aistudio.google.com/apikey
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path


def load_env_file(env_path: Path) -> dict:
    """Парсит .env файл и возвращает dict переменных."""
    env_vars = {}
    if not env_path.exists():
        return env_vars

    try:
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                # Пропускаем пустые строки и комментарии
                if not line or line.startswith('#'):
                    continue
                # Парсим KEY=VALUE
                if '=' in line:
                    key, _, value = line.partition('=')
                    key = key.strip()
                    value = value.strip()
                    # Убираем кавычки если есть
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    env_vars[key] = value
    except Exception:
        pass

    return env_vars


def get_api_key() -> str | None:
    """Получает API ключ из переменных окружения или .env файлов."""

    # 1. Проверяем переменную окружения
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        return api_key

    # 2. Ищем в .env файлах (в порядке приоритета)
    env_locations = [
        Path.cwd() / ".env",                          # Текущая директория
        Path(__file__).parent / ".env",               # Директория скрипта
        Path(__file__).parent.parent / ".env",        # skills/
        Path.home() / ".env",                         # Домашняя
        Path.home() / ".claude" / ".env",             # ~/.claude/
    ]

    for env_path in env_locations:
        env_vars = load_env_file(env_path)
        if "GEMINI_API_KEY" in env_vars:
            # Также устанавливаем в окружение для консистентности
            os.environ["GEMINI_API_KEY"] = env_vars["GEMINI_API_KEY"]
            return env_vars["GEMINI_API_KEY"]

    return None


# API endpoint
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"

# Доступные модели
MODELS = {
    "flash": "gemini-2.5-flash-preview-05-20",     # Nano Banana - быстрый
    "pro": "gemini-3-pro-image-preview",           # Nano Banana Pro - качественный
    "imagen": "imagen-3.0-generate-002",           # Imagen 3
}

DEFAULT_MODEL = "pro"


def json_to_prompt(spec: dict) -> str:
    """Конвертирует JSON спецификацию в текстовый промпт для Gemini."""

    schema_type = list(spec.keys())[0]
    data = spec[schema_type]

    prompt_parts = [
        "Generate a high-quality image based on this detailed specification.",
        f"Image type: {schema_type.replace('_', ' ').title()}",
    ]

    # Meta информация
    if "meta" in data:
        meta = data["meta"]
        if "title" in meta:
            prompt_parts.append(f"Title: {meta['title']}")
        if "description" in meta:
            prompt_parts.append(f"Description: {meta['description']}")

    # Добавляем ключевые элементы в читаемом виде
    if schema_type == "marketing_image":
        if "subject" in data:
            prompt_parts.append(f"Subject: {data['subject'].get('name', '')} - {data['subject'].get('description', '')}")
        if "environment" in data:
            env = data["environment"]
            if "atmosphere" in env:
                prompt_parts.append(f"Mood: {env['atmosphere'].get('mood', '')}")
            if "background" in env:
                prompt_parts.append(f"Background color: {env['background'].get('color', '')}")
        if "lighting" in data:
            light = data["lighting"]
            prompt_parts.append(f"Lighting: {light.get('key_light_direction', '')} key light, {light.get('color_temperature', 'neutral')} temperature")
        if "brand" in data:
            brand = data["brand"]
            if "primary_colors" in brand:
                prompt_parts.append(f"Brand colors: {', '.join(brand['primary_colors'])}")

    elif schema_type == "presentation_slide":
        if "content" in data:
            content = data["content"]
            if "headline" in content:
                prompt_parts.append(f"Headline: {content['headline'].get('text', '')}")
        if "layout" in data:
            prompt_parts.append(f"Layout: {data['layout'].get('type', '')} ({data['layout'].get('aspect_ratio', '16:9')})")

    elif schema_type == "icon_set":
        if "specifications" in data:
            specs = data["specifications"]
            prompt_parts.append(f"Icon style: {specs.get('style', 'outlined')}, {specs.get('grid_size', 24)}px grid")
        if "icons" in data:
            icon_names = [i.get("name", "") for i in data["icons"][:5]]
            prompt_parts.append(f"Icons to create: {', '.join(icon_names)}")

    elif schema_type == "illustration":
        if "style" in data:
            prompt_parts.append(f"Style: {data['style'].get('type', '')}")
        if "scene" in data:
            prompt_parts.append(f"Scene: {data['scene'].get('description', '')}")
            prompt_parts.append(f"Mood: {data['scene'].get('mood', '')}")

    # Добавляем полную спецификацию
    prompt_parts.append("\n--- FULL JSON SPECIFICATION (follow exactly) ---")
    prompt_parts.append(json.dumps(spec, indent=2, ensure_ascii=False))
    prompt_parts.append("--- END SPECIFICATION ---")

    prompt_parts.append("\nGenerate this image with professional quality. Follow all colors, positions, and styling from the specification.")

    return "\n".join(prompt_parts)


def generate_image(prompt: str, api_key: str, model_name: str = DEFAULT_MODEL) -> bytes:
    """Генерирует изображение через Gemini API."""

    model = MODELS.get(model_name, model_name)
    url = f"{GEMINI_API_URL}/{model}:generateContent?key={api_key}"

    # Request body для image generation
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
        }
    }

    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
    }

    print(f"Модель: {model}")
    print("Генерация изображения...")

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            error_json = json.loads(error_body)
            error_msg = error_json.get("error", {}).get("message", error_body)
        except:
            error_msg = error_body
        raise RuntimeError(f"API Error ({e.code}): {error_msg}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network Error: {e.reason}")

    # Извлекаем изображение из ответа
    if "candidates" not in result:
        raise RuntimeError(f"Unexpected response: {json.dumps(result, indent=2)}")

    for candidate in result["candidates"]:
        if "content" not in candidate:
            continue
        for part in candidate["content"].get("parts", []):
            if "inlineData" in part:
                inline = part["inlineData"]
                if inline.get("mimeType", "").startswith("image/"):
                    return base64.b64decode(inline["data"])
            # Gemini 2.0 может вернуть text с описанием
            if "text" in part:
                print(f"Model response: {part['text'][:200]}...")

    # Если изображение не найдено, выводим полный ответ для отладки
    print("Full response:")
    print(json.dumps(result, indent=2, ensure_ascii=False)[:2000])
    raise RuntimeError("No image found in response. Model may not support image generation.")


def save_image(image_bytes: bytes, output_path: Path) -> None:
    """Сохраняет изображение."""

    # Определяем формат по magic bytes
    if image_bytes[:8] == b'\x89PNG\r\n\x1a\n':
        ext = ".png"
    elif image_bytes[:2] == b'\xff\xd8':
        ext = ".jpg"
    elif image_bytes[:4] == b'RIFF' and image_bytes[8:12] == b'WEBP':
        ext = ".webp"
    else:
        ext = ".png"  # default

    # Добавляем расширение если нет
    if not output_path.suffix:
        output_path = output_path.with_suffix(ext)

    output_path.write_bytes(image_bytes)
    print(f"Сохранено: {output_path}")
    print(f"Размер: {len(image_bytes) / 1024:.1f} KB")


def main():
    parser = argparse.ArgumentParser(
        description="Генерация изображений через Gemini API (без зависимостей)"
    )
    parser.add_argument(
        "spec_file",
        type=Path,
        nargs="?",
        help="JSON файл со спецификацией"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Путь для сохранения (по умолчанию: spec_file_timestamp.png)"
    )
    parser.add_argument(
        "--model", "-m",
        choices=list(MODELS.keys()),
        default=DEFAULT_MODEL,
        help=f"Модель (по умолчанию: {DEFAULT_MODEL})"
    )
    parser.add_argument(
        "--prompt-only",
        action="store_true",
        help="Только показать промпт, не генерировать"
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Читать JSON из stdin"
    )

    args = parser.parse_args()

    # Получаем API ключ (из env или .env файлов)
    api_key = get_api_key()
    if not api_key:
        print("GEMINI_API_KEY не найден!")
        print()
        print("Варианты настройки:")
        print("  1. export GEMINI_API_KEY=your_key")
        print("  2. Создать .env файл с GEMINI_API_KEY=your_key")
        print("     Поддерживаемые пути: ./.env, ~/.env, ~/.claude/.env")
        print()
        print("Получить ключ: https://aistudio.google.com/apikey")
        sys.exit(1)

    # Читаем спецификацию
    if args.stdin:
        spec = json.load(sys.stdin)
    elif args.spec_file:
        if not args.spec_file.exists():
            print(f"Файл не найден: {args.spec_file}")
            sys.exit(1)
        with open(args.spec_file) as f:
            spec = json.load(f)
    else:
        parser.print_help()
        sys.exit(1)

    # Конвертируем в промпт
    prompt = json_to_prompt(spec)

    if args.prompt_only:
        print("=" * 60)
        print("ПРОМПТ:")
        print("=" * 60)
        print(prompt)
        return

    # Генерируем
    try:
        image_bytes = generate_image(prompt, api_key, args.model)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

    # Сохраняем
    if args.output:
        output_path = args.output
    elif args.spec_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = args.spec_file.with_name(f"{args.spec_file.stem}_{timestamp}.png")
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Path(f"generated_{timestamp}.png")

    save_image(image_bytes, output_path)


if __name__ == "__main__":
    main()
