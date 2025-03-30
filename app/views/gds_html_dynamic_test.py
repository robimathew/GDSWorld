import os
import re
import base64
import requests
from pathlib import Path

# Folders
SOURCE_FOLDER = Path("./source_images")
OUTPUT_FOLDER = Path("./output_html")
SNIPPET_FOLDER = Path("./prompt_snippets")
PROMPT_TEMPLATE = Path("./prompt_template.txt")


def load_snippet(relative_path: str) -> str:
    snippet_path = SNIPPET_FOLDER / relative_path
    if not snippet_path.exists():
        return ""
    with open(snippet_path, "r", encoding="utf-8") as f:
        return f.read()

def load_prompt_template() -> str:
    if not PROMPT_TEMPLATE.exists():
        raise FileNotFoundError("Missing prompt_template.txt. Please create one in the script folder.")
    with open(PROMPT_TEMPLATE, "r", encoding="utf-8") as f:
        return f.read()

def merge_prompt_with_snippets(base_prompt: str, filename: str) -> str:
    sections = []

    # Load all components
    components_path = SNIPPET_FOLDER / "components"
    for comp in components_path.glob("*.txt"):
        sections.append(comp.read_text(encoding="utf-8"))

    # Load all pages
    pages_path = SNIPPET_FOLDER / "pages"
    for page in pages_path.glob("*.txt"):
        sections.append(page.read_text(encoding="utf-8"))

    # Load all custom snippets
    custom_path = SNIPPET_FOLDER / "custom"
    for custom in custom_path.glob("*.txt"):
        sections.append(custom.read_text(encoding="utf-8"))

    # Always add date-input.txt if filename suggests it's needed
    if re.search(r"dob|birth|date", filename.lower()):
        date_input_path = SNIPPET_FOLDER / "components/date-input.txt"
        if date_input_path.exists():
            sections.append(date_input_path.read_text(encoding="utf-8"))

    full_prompt = base_prompt.strip() + "\n\n" + "\n\n".join(sections)
    return full_prompt.strip()

def call_llama_vision(image_path: str, prompt: str) -> str:
    with open(image_path, "rb") as img_file:
        image_data = base64.b64encode(img_file.read()).decode("utf-8")

    payload = {
        "model": "llama3.2-vision:latest",
        "prompt": prompt,
        "images": [image_data],
        "stream": False
    }

    response = requests.post("http://localhost:11434/api/generate", json=payload)
    response.raise_for_status()
    return response.json()["response"]

def main():
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    base_prompt = load_prompt_template()

    image_files = list(SOURCE_FOLDER.glob("*.png")) + list(SOURCE_FOLDER.glob("*.jpg")) + list(SOURCE_FOLDER.glob("*.jpeg"))

    if not image_files:
        print("No wireframe images found in ./source_images")
        return

    for image_path in image_files:
        print(f"\n📄 Processing: {image_path.name}")

        final_prompt = merge_prompt_with_snippets(base_prompt, image_path.name)
        raw_html = call_llama_vision(str(image_path), final_prompt)

        output_file = OUTPUT_FOLDER / (image_path.stem + "_dynamic.html")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(raw_html)

        print(f"✅ Saved dynamic output: {output_file}")

if __name__ == "__main__":
    main()
