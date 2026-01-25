#!/usr/bin/env python3
"""
Nano Banana Pro Image Generator (Zero Dependencies)

Generate images via Gemini API.
Works without installing additional packages — Python 3 stdlib only.

Usage:
    # Text prompt (recommended)
    python generate.py --prompt "hero shot of product on marble, dramatic lighting"

    # JSON specification (for full control)
    python generate.py spec.json [--output image.png] [--model flash]

API key is loaded automatically from (in order of priority):
    1. GEMINI_API_KEY environment variable
    2. .env in current directory
    3. .env in script directory
    4. ~/.env
    5. ~/.claude/.env

.env file format:
    GEMINI_API_KEY=AIzaSy...

Get key: https://aistudio.google.com/apikey
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
    """Parse .env file and return dict of variables."""
    env_vars = {}
    if not env_path.exists():
        return env_vars

    try:
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                # Parse KEY=VALUE
                if '=' in line:
                    key, _, value = line.partition('=')
                    key = key.strip()
                    value = value.strip()
                    # Remove quotes if present
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    env_vars[key] = value
    except Exception:
        pass

    return env_vars


def get_api_key() -> str | None:
    """Get API key from environment variables or .env files."""

    # 1. Check environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        return api_key

    # 2. Search in .env files (in order of priority)
    env_locations = [
        Path.cwd() / ".env",                          # Current directory
        Path(__file__).parent / ".env",               # Script directory
        Path(__file__).parent.parent / ".env",        # skills/
        Path.home() / ".env",                         # Home
        Path.home() / ".claude" / ".env",             # ~/.claude/
    ]

    for env_path in env_locations:
        env_vars = load_env_file(env_path)
        if "GEMINI_API_KEY" in env_vars:
            # Also set in environment for consistency
            os.environ["GEMINI_API_KEY"] = env_vars["GEMINI_API_KEY"]
            return env_vars["GEMINI_API_KEY"]

    return None


# API endpoint
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"

# Available models
MODELS = {
    "flash": "gemini-2.5-flash-preview-05-20",     # Nano Banana - fast
    "pro": "gemini-3-pro-image-preview",           # Nano Banana Pro - quality
    "imagen": "imagen-3.0-generate-002",           # Imagen 3
}

DEFAULT_MODEL = "pro"


def json_to_prompt(spec: dict) -> str:
    """Convert JSON specification to text prompt for Gemini."""

    schema_type = list(spec.keys())[0]
    data = spec[schema_type]

    prompt_parts = [
        "Generate a high-quality image based on this detailed specification.",
        f"Image type: {schema_type.replace('_', ' ').title()}",
    ]

    # Meta information
    if "meta" in data:
        meta = data["meta"]
        if "title" in meta:
            prompt_parts.append(f"Title: {meta['title']}")
        if "description" in meta:
            prompt_parts.append(f"Description: {meta['description']}")

    # Add key elements in readable form
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

    # Add full specification
    prompt_parts.append("\n--- FULL JSON SPECIFICATION (follow exactly) ---")
    prompt_parts.append(json.dumps(spec, indent=2, ensure_ascii=False))
    prompt_parts.append("--- END SPECIFICATION ---")

    prompt_parts.append("\nGenerate this image with professional quality. Follow all colors, positions, and styling from the specification.")

    return "\n".join(prompt_parts)


def generate_image(prompt: str, api_key: str, model_name: str = DEFAULT_MODEL) -> bytes:
    """Generate image via Gemini API."""

    model = MODELS.get(model_name, model_name)
    url = f"{GEMINI_API_URL}/{model}:generateContent?key={api_key}"

    # Request body for image generation
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

    print(f"Model: {model}")
    print("Generating image...")

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

    # Extract image from response
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
            # Gemini 2.0 may return text with description
            if "text" in part:
                print(f"Model response: {part['text'][:200]}...")

    # If image not found, output full response for debugging
    print("Full response:")
    print(json.dumps(result, indent=2, ensure_ascii=False)[:2000])
    raise RuntimeError("No image found in response. Model may not support image generation.")


def save_image(image_bytes: bytes, output_path: Path) -> None:
    """Save image to file."""

    # Detect format by magic bytes
    if image_bytes[:8] == b'\x89PNG\r\n\x1a\n':
        ext = ".png"
    elif image_bytes[:2] == b'\xff\xd8':
        ext = ".jpg"
    elif image_bytes[:4] == b'RIFF' and image_bytes[8:12] == b'WEBP':
        ext = ".webp"
    else:
        ext = ".png"  # default

    # Add extension if missing
    if not output_path.suffix:
        output_path = output_path.with_suffix(ext)

    output_path.write_bytes(image_bytes)
    print(f"Saved: {output_path}")
    print(f"Size: {len(image_bytes) / 1024:.1f} KB")


def main():
    parser = argparse.ArgumentParser(
        description="Generate images via Gemini API (zero dependencies)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text prompt (recommended)
  python generate.py -p "hero shot of product on marble, dramatic lighting"
  python generate.py --prompt "SaaS dashboard, dark theme, charts"

  # JSON specification (full control)
  python generate.py spec.json --model pro

  # Quick generation
  python generate.py -p "wallet icon, outlined, 24px" -m flash
        """
    )
    parser.add_argument(
        "spec_file",
        type=Path,
        nargs="?",
        help="JSON spec file (optional if using --prompt)"
    )
    parser.add_argument(
        "--prompt", "-p",
        type=str,
        default=None,
        help="Text prompt for generation (instead of JSON file)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Output path (default: generated_timestamp.png)"
    )
    parser.add_argument(
        "--model", "-m",
        choices=list(MODELS.keys()),
        default=DEFAULT_MODEL,
        help=f"Model (default: {DEFAULT_MODEL})"
    )
    parser.add_argument(
        "--show-prompt",
        action="store_true",
        help="Show final prompt before generation"
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read JSON from stdin"
    )

    args = parser.parse_args()

    # Get API key (from env or .env files)
    api_key = get_api_key()
    if not api_key:
        print("GEMINI_API_KEY not found!")
        print()
        print("Setup options:")
        print("  1. export GEMINI_API_KEY=your_key")
        print("  2. Create .env file with GEMINI_API_KEY=your_key")
        print("     Supported paths: ./.env, ~/.env, ~/.claude/.env")
        print()
        print("Get key: https://aistudio.google.com/apikey")
        sys.exit(1)

    # Determine prompt
    prompt = None

    # Option 1: Text prompt directly
    if args.prompt:
        prompt = args.prompt
        print(f"Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")

    # Option 2: JSON from stdin
    elif args.stdin:
        spec = json.load(sys.stdin)
        prompt = json_to_prompt(spec)

    # Option 3: JSON file
    elif args.spec_file:
        if not args.spec_file.exists():
            print(f"File not found: {args.spec_file}")
            sys.exit(1)
        with open(args.spec_file) as f:
            spec = json.load(f)
        prompt = json_to_prompt(spec)

    # No input data
    else:
        parser.print_help()
        sys.exit(1)

    if args.show_prompt:
        print("=" * 60)
        print("PROMPT:")
        print("=" * 60)
        print(prompt)
        print("=" * 60)

    # Generate
    try:
        image_bytes = generate_image(prompt, api_key, args.model)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Determine output path
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
