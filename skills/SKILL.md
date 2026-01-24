---
name: nano-banana-ru
description: Генерирует изображения через Gemini API. Маркетинг, UI мокапы, диаграммы, слайды, иконки, иллюстрации.
argument-hint: "[описание изображения]"
---

# Nano Banana Pro — Генератор изображений

Генерирует изображения через Gemini 3 Pro Image API по текстовому описанию.

## Входные данные
$ARGUMENTS

Если описание не предоставлено, спроси: "Что хочешь создать? (продукт, UI, диаграмму, слайд, иконки или иллюстрацию?)"

---

## Как работает

1. Получаешь описание от пользователя
2. Улучшаешь промпт (добавляешь детали)
3. Запускаешь генератор через Bash

```bash
python ~/.claude/skills/nano-banana-ru/skills/scripts/generate.py \
  --prompt "твой промпт" \
  --output ./output/image.png
```

---

## Промпт-инженерия

### Структура хорошего промпта

```
[ТИП ИЗОБРАЖЕНИЯ] + [ГЛАВНЫЙ ОБЪЕКТ] + [СТИЛЬ/АТМОСФЕРА] + [ДЕТАЛИ]
```

### Примеры по типам

**Продуктовое фото:**
```
hero shot банки энергетика Aurora Lime на глянцевой чёрной поверхности,
драматическое боковое освещение справа, лаймы и кубики льда на переднем плане,
брызги воды, тёмно-бирюзовый фон (#003b47), премиальная атмосфера
```

**UI/UX мокап:**
```
dashboard аналитики SaaS, тёмная тема (#1a1a2e),
левый сайдбар с навигацией, основная область с 4 карточками метрик,
большой line chart выручки за год, таблица транзакций внизу,
modern minimal style, Inter font
```

**Слайд презентации (McKinsey style):**
```
presentation slide, белый фон, 16:9,
заголовок "Рост выручки +47% YoY" синим (#1E3A8A) сверху слева,
три метрики в ряд: "$12.4M выручка", "340 клиентов", "94% retention",
bar chart справа сравнение Q4 2024 vs Q4 2025,
логотип в правом нижнем углу, McKinsey consulting style
```

**Набор иконок:**
```
icon set для финтех приложения, 8 иконок в ряд:
wallet, card, transfer, history, scan, security, support, settings,
outlined style, stroke 1.5px, 24px grid,
монохромные #1A1A1A, rounded corners
```

**Иллюстрация:**
```
isometric illustration команды из 4 человек работающих удаленно,
каждый за своим столом с ноутбуком,
соединены пунктирными линиями связи (#3B82F6),
разнообразные персонажи, современный flat style,
пастельные цвета, белый фон, дружелюбная атмосфера
```

**Диаграмма:**
```
flowchart процесса регистрации пользователя,
5 шагов: Email → Verification → Profile → Payment → Welcome,
горизонтальное направление слева направо,
rounded rectangles, стрелки между шагами,
синие (#3B82F6) ноды, серые (#6B7280) подписи
```

---

## Ключевые слова для улучшения промптов

### Стиль
- `premium`, `luxury`, `minimal`, `modern`, `corporate`
- `McKinsey style`, `Apple style`, `tech startup`

### Освещение
- `dramatic side lighting`, `soft diffused light`, `backlit`
- `studio lighting`, `natural daylight`

### Атмосфера
- `professional`, `friendly`, `energetic`, `calm`, `bold`

### Технические детали
- `16:9 aspect ratio`, `4K resolution`, `sharp focus`
- `depth of field`, `high contrast`

---

## Модели

| Флаг | Модель | Когда использовать |
|------|--------|-------------------|
| `flash` | gemini-2.5-flash | Быстрые итерации, черновики |
| `pro` | gemini-3-pro-image-preview | Финальное качество (по умолчанию) |
| `imagen` | imagen-3.0 | Фотореализм |

---

## Workflow

### Быстрая генерация
```bash
python ~/.claude/skills/nano-banana-ru/skills/scripts/generate.py \
  -p "hero shot продукта" -m flash -o ./draft.png
```

### Финальная версия
```bash
python ~/.claude/skills/nano-banana-ru/skills/scripts/generate.py \
  -p "детальный промпт со всеми деталями" -o ./final.png
```

---

## Pro Mode: JSON спецификации

Для **полного контроля** (брендинг, серийная генерация) используй JSON:

```bash
python ~/.claude/skills/nano-banana-ru/skills/scripts/generate.py spec.json
```

JSON примеры в `examples/` директории.

---

## Troubleshooting

**API ключ не найден:**
```bash
echo "GEMINI_API_KEY=your_key" > ~/.claude/skills/nano-banana-ru/skills/.env
```

**Модель не генерирует изображения:**
Используй `--model pro` (gemini-3-pro-image-preview).
