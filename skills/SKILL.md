---
name: nano-banana-ru
description: Generate images via Gemini API. Marketing shots, UI mockups, slides, icons, illustrations — from text prompts.
argument-hint: "[image description]"
---

# Nano Banana Pro — Image Generator

Generate images via Gemini 3 Pro Image API from text descriptions.

## Input
$ARGUMENTS

If no description provided, ask: "What do you want to create? (product shot, UI, diagram, slide, icons, or illustration?)"

---

## How it works

1. Get description from user
2. Enhance the prompt (add details)
3. Run generator via Bash

```bash
python3 ~/.claude/skills/nano-banana-ru/skills/scripts/generate.py \
  --prompt "your prompt" \
  --output ./output/image.png
```

---

## Prompt Engineering

### Good prompt structure

```
[IMAGE TYPE] + [MAIN SUBJECT] + [STYLE/MOOD] + [DETAILS]
```

### Examples by type

**Product photography:**
```
hero shot of Aurora Lime energy drink can on glossy black surface,
dramatic side lighting from right, limes and ice cubes in foreground,
water splashes, dark teal background (#003b47), premium atmosphere
```

**UI/UX mockup:**
```
SaaS analytics dashboard, dark theme (#1a1a2e),
left sidebar with navigation, main area with 4 metric cards,
large line chart showing yearly revenue, transactions table below,
modern minimal style, Inter font
```

**Presentation slide (McKinsey style):**
```
presentation slide, white background, 16:9,
headline "Revenue Growth +47% YoY" in blue (#1E3A8A) top left,
three metrics in row: "$12.4M revenue", "340 clients", "94% retention",
bar chart on right comparing Q4 2024 vs Q4 2025,
logo bottom right corner, McKinsey consulting style
```

**Icon set:**
```
fintech app icon set, 8 icons in a row:
wallet, card, transfer, history, scan, security, support, settings,
outlined style, stroke 1.5px, 24px grid,
monochrome #1A1A1A, rounded corners
```

**Illustration:**
```
isometric illustration of 4 people working remotely,
each at their own desk with laptop,
connected by dashed communication lines (#3B82F6),
diverse characters, modern flat style,
pastel colors, white background, friendly atmosphere
```

**Diagram:**
```
user registration flowchart,
5 steps: Email → Verification → Profile → Payment → Welcome,
horizontal direction left to right,
rounded rectangles, arrows between steps,
blue (#3B82F6) nodes, gray (#6B7280) labels
```

---

## Keywords for better prompts

### Style
- `premium`, `luxury`, `minimal`, `modern`, `corporate`
- `McKinsey style`, `Apple style`, `tech startup`

### Lighting
- `dramatic side lighting`, `soft diffused light`, `backlit`
- `studio lighting`, `natural daylight`

### Mood
- `professional`, `friendly`, `energetic`, `calm`, `bold`

### Technical details
- `16:9 aspect ratio`, `4K resolution`, `sharp focus`
- `depth of field`, `high contrast`

---

## Models

| Flag | Model | When to use |
|------|-------|-------------|
| `flash` | gemini-2.5-flash | Quick iterations, drafts |
| `pro` | gemini-3-pro-image-preview | Final quality (default) |
| `imagen` | imagen-3.0 | Photorealism |

---

## Workflow

### Quick draft
```bash
python3 ~/.claude/skills/nano-banana-ru/skills/scripts/generate.py \
  -p "product hero shot" -m flash -o ./draft.png
```

### Final version
```bash
python3 ~/.claude/skills/nano-banana-ru/skills/scripts/generate.py \
  -p "detailed prompt with all specifics" -o ./final.png
```

---

## Pro Mode: JSON specs

For **full control** (branding, batch generation) use JSON:

```bash
python3 ~/.claude/skills/nano-banana-ru/skills/scripts/generate.py spec.json
```

JSON examples in `examples/json/` directory.

---

## Troubleshooting

**API key not found:**
```bash
echo "GEMINI_API_KEY=your_key" > ~/.claude/skills/nano-banana-ru/skills/.env
```

**Model doesn't generate images:**
Use `--model pro` (gemini-3-pro-image-preview).
