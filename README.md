# Nano Banana Pro

<p align="center">
  <img src="https://img.shields.io/badge/Claude%20Code-Plugin-blue" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Gemini-3%20Pro%20Image-green" alt="Gemini 3 Pro">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="MIT License">
</p>

Generate images via Gemini API with a single command.

## Quick Start

```bash
# 1. Clone
git clone https://github.com/ilyakorolev/nano-banana-ru ~/.claude/skills/nano-banana-ru

# 2. Add API key (https://aistudio.google.com/apikey)
echo "GEMINI_API_KEY=your_key" > ~/.claude/skills/nano-banana-ru/skills/.env

# 3. Use
/nano-banana-ru hero shot of product on marble, dramatic lighting
```

## Usage

### Via skill (recommended)
```bash
/nano-banana-ru SaaS dashboard, dark theme, charts and metrics
```

### Via script directly
```bash
python3 ~/.claude/skills/nano-banana-ru/skills/scripts/generate.py \
  --prompt "presentation slide, McKinsey style, growth metrics" \
  --output slide.png
```

### Options
```bash
-p, --prompt    Text prompt
-o, --output    Output path
-m, --model     flash (fast) | pro (quality) | imagen (photo)
```

## Prompt Examples

**Product:**
```
hero shot of energy drink can, ice and splashes, dramatic lighting, dark background
```

**UI mockup:**
```
analytics dashboard, dark theme, 4 metric cards, line chart, Inter font
```

**Slide (McKinsey):**
```
presentation slide, white background, 16:9, headline "Growth +47%", three metrics, bar chart
```

**Icons:**
```
fintech icon set: wallet, card, transfer, history, outlined, 24px, #374151
```

More examples: [examples/prompts.md](examples/prompts.md)

## Installation

### Option 1: As skill
```bash
git clone https://github.com/ilyakorolev/nano-banana-ru ~/.claude/skills/nano-banana-ru
```

### Option 2: As plugin
```bash
git clone https://github.com/ilyakorolev/nano-banana-ru ~/.claude/plugins/nano-banana-ru
```

### Option 3: With flag
```bash
claude --plugin-dir ./nano-banana-ru
```

## API Setup

1. Get key: [Google AI Studio](https://aistudio.google.com/apikey)
2. Create `.env`:
```bash
echo "GEMINI_API_KEY=AIzaSy..." > ~/.claude/skills/nano-banana-ru/skills/.env
```

Or via environment variable:
```bash
export GEMINI_API_KEY=AIzaSy...
```

## Models

| Model | Use case |
|-------|----------|
| `flash` | Quick iterations, drafts |
| `pro` | Final quality (default) |
| `imagen` | Photorealism, artistic styles |

## Structure

```
nano-banana-ru/
├── skills/
│   ├── SKILL.md              # Claude instructions
│   ├── .env                  # API key (create)
│   └── scripts/
│       └── generate.py       # Zero-dependency generator
├── examples/
│   ├── prompts.md            # Prompt examples
│   └── json/                 # JSON specs (Pro mode)
└── README.md
```

## Pro Mode (JSON)

For full control over generation (branding, batch generation):

```bash
python3 generate.py examples/json/marketing.json --output result.png
```

## Zero Dependencies

Script runs on pure Python 3 — stdlib only. No `pip install` needed.

## Credits

Inspired by:
- [kkoppenhaver/cc-nano-banana](https://github.com/kkoppenhaver/cc-nano-banana) — Gemini CLI integration
- [jawhnycooke/claude-code-nano-banana](https://github.com/jawhnycooke/claude-code-nano-banana) — Original JSON translator

API: [Gemini Image Generation](https://ai.google.dev/gemini-api/docs/image-generation)

## License

MIT — [LICENSE](LICENSE)
