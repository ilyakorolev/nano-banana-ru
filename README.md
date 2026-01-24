# Nano Banana Pro (Russian Edition)

<p align="center">
  <img src="https://img.shields.io/badge/Claude%20Code-Plugin-blue" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Gemini-3%20Pro%20Image-green" alt="Gemini 3 Pro">
  <img src="https://img.shields.io/badge/Language-Russian-red" alt="Russian">
</p>

Генерация изображений через Gemini API одной командой.

## Quick Start

```bash
# 1. Клонировать
git clone https://github.com/ilyakorolev/nano-banana-ru ~/.claude/skills/nano-banana-ru

# 2. Добавить API ключ (https://aistudio.google.com/apikey)
echo "GEMINI_API_KEY=your_key" > ~/.claude/skills/nano-banana-ru/skills/.env

# 3. Использовать
/nano-banana-ru hero shot продукта на мраморе, драматическое освещение
```

## Использование

### Через skill (рекомендуется)
```bash
/nano-banana-ru дашборд SaaS, тёмная тема, графики и метрики
```

### Через скрипт напрямую
```bash
python ~/.claude/skills/nano-banana-ru/skills/scripts/generate.py \
  --prompt "слайд презентации, McKinsey style, метрики роста" \
  --output slide.png
```

### Опции
```bash
-p, --prompt    Текстовый промпт
-o, --output    Путь для сохранения
-m, --model     flash (быстро) | pro (качество) | imagen (фото)
```

## Примеры промптов

**Продукт:**
```
hero shot банки энергетика, лёд и брызги, драматическое освещение, тёмный фон
```

**UI мокап:**
```
dashboard аналитики, тёмная тема, 4 карточки метрик, line chart, Inter font
```

**Слайд (McKinsey):**
```
presentation slide, белый фон, 16:9, заголовок "Рост +47%", три метрики, bar chart
```

**Иконки:**
```
icon set финтех: wallet, card, transfer, history, outlined, 24px, #374151
```

Больше примеров: [examples/prompts.md](examples/prompts.md)

## Установка

### Вариант 1: Как skill
```bash
git clone https://github.com/ilyakorolev/nano-banana-ru ~/.claude/skills/nano-banana-ru
```

### Вариант 2: Как plugin
```bash
git clone https://github.com/ilyakorolev/nano-banana-ru ~/.claude/plugins/nano-banana-ru
```

### Вариант 3: С флагом
```bash
claude --plugin-dir ./nano-banana-ru
```

## Настройка API

1. Получить ключ: [Google AI Studio](https://aistudio.google.com/apikey)
2. Создать `.env`:
```bash
echo "GEMINI_API_KEY=AIzaSy..." > ~/.claude/skills/nano-banana-ru/skills/.env
```

Или через переменную окружения:
```bash
export GEMINI_API_KEY=AIzaSy...
```

## Модели

| Модель | Для чего |
|--------|----------|
| `flash` | Быстрые итерации, черновики |
| `pro` | Финальное качество (по умолчанию) |
| `imagen` | Фотореализм, художественные стили |

## Структура

```
nano-banana-ru/
├── skills/
│   ├── SKILL.md              # Инструкции для Claude
│   ├── .env                  # API ключ (создать)
│   └── scripts/
│       └── generate.py       # Zero-dependency генератор
├── examples/
│   ├── prompts.md            # Примеры промптов
│   └── json/                 # JSON спецификации (Pro mode)
└── README.md
```

## Pro Mode (JSON)

Для полного контроля над генерацией (брендинг, серийная генерация):

```bash
python generate.py examples/json/marketing.json --output result.png
```

## Zero Dependencies

Скрипт работает на чистом Python 3 — только стандартная библиотека. Никаких `pip install`.

## Credits

Вдохновлён:
- [kkoppenhaver/cc-nano-banana](https://github.com/kkoppenhaver/cc-nano-banana) — Gemini CLI интеграция
- [jawhnycooke/claude-code-nano-banana](https://github.com/jawhnycooke/claude-code-nano-banana) — оригинальный JSON translator

API: [Gemini Image Generation](https://ai.google.dev/gemini-api/docs/image-generation)

## License

MIT — [LICENSE](LICENSE)
