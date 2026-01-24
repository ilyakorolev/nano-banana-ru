# Nano Banana Pro JSON Translator (Russian Edition)

<p align="center">
  <img src="https://img.shields.io/badge/Claude%20Code-Plugin-blue" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Gemini-3%20Pro%20Image-green" alt="Gemini 3 Pro">
  <img src="https://img.shields.io/badge/Language-Russian-red" alt="Russian">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="MIT License">
</p>

Плагин для Claude Code, который конвертирует описания на русском языке в структурированные JSON спецификации для [Nano Banana Pro](https://ai.google.dev/gemini-api/docs/image-generation) (Gemini 3 Pro Image).

**Основная идея:** Вместо расплывчатых промптов создаём точные спецификации, где каждый элемент — освещение, угол камеры, цвета, композиция — контролируется отдельно.

## Возможности

### 8 типов изображений

| Тип | Схема | Описание |
|-----|-------|----------|
| Маркетинг | `marketing_image` | Продуктовые шоты, hero-изображения, брендовая фотография |
| UI/UX | `ui_builder` | Экраны приложений, дашборды, веб-сайты |
| Диаграммы | `diagram_spec` | Флоучарты, архитектурные схемы, карты процессов |
| Данные | `data_viz` | Графики, чарты, визуализации статистики |
| Соцсети | `social_graphic` | Instagram, Telegram, VK, LinkedIn посты |
| Презентации | `presentation_slide` | Слайды для Keynote/PowerPoint/Google Slides |
| Иконки | `icon_set` | Согласованные наборы иконок |
| Иллюстрации | `illustration` | Художественные иллюстрации, концепт-арт |

### Особенности

- **Zero dependencies** — скрипт генерации работает на чистом Python 3
- **Автозагрузка API ключа** — из `.env` файла или переменной окружения
- **Русский язык** — все инструкции и примеры на русском
- **McKinsey-style слайды** — профессиональные презентации

## Установка

### Вариант 1: Через Claude Code Marketplace (рекомендуется)

```bash
# Добавить marketplace
/plugin marketplace add https://github.com/ilyakorolev/nano-banana-ru

# Установить плагин
/plugin
# → Выбрать "Browse and install plugins"
# → Выбрать marketplace "nano-banana-ru"
# → Нажать Space для выбора, затем i для установки
```

### Вариант 2: Клонировать локально

```bash
# Клонировать в папку плагинов Claude Code
git clone https://github.com/ilyakorolev/nano-banana-ru ~/.claude/plugins/nano-banana-ru

# Или в папку skills
git clone https://github.com/ilyakorolev/nano-banana-ru ~/.claude/skills/nano-banana-ru
```

### Вариант 3: Запуск с флагом

```bash
git clone https://github.com/ilyakorolev/nano-banana-ru
claude --plugin-dir ./nano-banana-ru
```

## Настройка API

### Шаг 1: Получить Gemini API ключ

1. Откройте [Google AI Studio](https://aistudio.google.com/apikey)
2. Нажмите "Create API Key"
3. Скопируйте ключ

### Шаг 2: Настроить ключ

**Вариант A: Через .env файл (рекомендуется)**

```bash
cd ~/.claude/skills/nano-banana-ru/skills
cp .env.example .env
nano .env  # Вставьте ваш ключ
```

```env
GEMINI_API_KEY=AIzaSy...ваш_ключ
```

**Вариант B: Через переменную окружения**

```bash
# Добавьте в ~/.zshrc или ~/.bashrc
export GEMINI_API_KEY=AIzaSy...ваш_ключ
```

## Использование

### Базовое использование

```bash
# Создать спецификацию через диалог
/nano-banana-ru

# С описанием
/nano-banana-ru hero shot продукта на мраморной поверхности, драматическое освещение

# Слайд презентации
/nano-banana-ru слайд для инвестор-дека, метрики роста, McKinsey style
```

### Генерация изображения

После создания JSON спецификации:

```bash
# Сохранить JSON в файл и сгенерировать
python skills/scripts/generate.py spec.json --output result.png

# С выбором модели
python skills/scripts/generate.py spec.json --model flash  # быстрее
python skills/scripts/generate.py spec.json --model pro    # качественнее (по умолчанию)
```

### Доступные модели

| Модель | ID | Описание |
|--------|-----|----------|
| `flash` | gemini-2.5-flash | Быстрый, хорош для итераций |
| `pro` | gemini-3-pro-image-preview | Nano Banana Pro — высокое качество |
| `imagen` | imagen-3.0 | Фотореализм, художественные стили |

## Примеры

### Маркетинговое изображение

```bash
/nano-banana-ru продуктовое фото банки энергетика, лёд, брызги воды, тёмный фон
```

### UI Мокап

```bash
/nano-banana-ru дашборд аналитики SaaS, тёмная тема, графики и метрики
```

### Слайд презентации (McKinsey style)

```bash
/nano-banana-ru слайд "Рост выручки +47%", три метрики, белый фон, синие акценты
```

### Набор иконок

```bash
/nano-banana-ru набор иконок для финтех приложения, outlined, 24px сетка
```

## Структура проекта

```
nano-banana-ru/
├── .claude-plugin/
│   ├── plugin.json          # Метаданные плагина
│   └── marketplace.json     # Конфигурация marketplace
├── skills/
│   ├── SKILL.md             # Основной skill (инструкции)
│   ├── .env.example         # Шаблон конфигурации
│   └── scripts/
│       └── generate.py      # Скрипт генерации (zero deps)
├── examples/
│   ├── marketing.json
│   ├── presentation.json
│   └── icons.json
├── .gitignore
├── LICENSE
└── README.md
```

## Отличия от оригинального nano-banana

| Feature | Оригинал | Russian Edition |
|---------|----------|-----------------|
| Язык | English | Русский |
| Типов схем | 5 | 8 (+презентации, иконки, иллюстрации) |
| Соцсети | Instagram, Twitter, LinkedIn | + Telegram, VK |
| API интеграция | Ручной copy-paste | Автоматическая генерация |
| Зависимости | google-genai | Zero dependencies |
| .env поддержка | Нет | Да |

## Troubleshooting

### API ключ не найден

```
GEMINI_API_KEY не найден!
```

**Решение:** Создайте `.env` файл или установите переменную окружения.

### Ошибка генерации

```
API Error (400): ...
```

**Решение:** Проверьте валидность API ключа на [Google AI Studio](https://aistudio.google.com/apikey).

### Модель не поддерживает генерацию изображений

Используйте модель `pro` (gemini-3-pro-image-preview) — она специально для генерации изображений.

## Contributing

Pull requests приветствуются! Особенно:

- Новые типы схем
- Улучшения промптов
- Примеры использования
- Переводы документации

## Credits

- Форк [jawhnycooke/claude-code-nano-banana](https://github.com/jawhnycooke/claude-code-nano-banana)
- Powered by [Gemini API](https://ai.google.dev/gemini-api/docs/image-generation)

## License

MIT License — см. [LICENSE](LICENSE)
