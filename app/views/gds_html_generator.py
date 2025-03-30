import os
import re
import base64
import requests
from pathlib import Path

# Folders
SOURCE_FOLDER = Path("./source_images")
OUTPUT_FOLDER = Path("./output_html")
SNIPPET_FOLDER = Path("./prompt_snippets")


def load_snippet(relative_path: str) -> str:
    snippet_path = SNIPPET_FOLDER / relative_path
    if not snippet_path.exists():
        raise FileNotFoundError(f"Missing snippet: {snippet_path}")
    with open(snippet_path, "r", encoding="utf-8") as f:
        return f.read()

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

def clean_ai_output(text: str) -> str:
    # Remove markdown syntax and explanations
    cleaned = re.sub(r"```(?:html)?", "", text)
    cleaned = re.sub(r"\*\*Step.*?\*\*", "", cleaned)
    cleaned = re.sub(r"\n{2,}", "\n", cleaned)
    # Extract only the last <div> block (if multiple snippets were generated)
    blocks = re.findall(r"(<div.*?</div>)", cleaned, re.DOTALL)
    if blocks:
        return blocks[-1]  # Use the last block assuming it's the final answer
    return cleaned.strip()

def main():
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    # Load prompt content
    prompt_path = Path("prompt_template.txt")
    if not prompt_path.exists():
        raise FileNotFoundError("Missing prompt_template.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read()

    # Load full layout wrapper (includes header + footer already)
    wrapper = load_snippet("layout/page-wrapper.txt")

    image_files = list(SOURCE_FOLDER.glob("*.png")) + list(SOURCE_FOLDER.glob("*.jpg")) + list(SOURCE_FOLDER.glob("*.jpeg"))

    if not image_files:
        print("No wireframe images found in ./source_images")
        return

    for image_path in image_files:
        print(f"\n📄 Processing: {image_path.name}")

        # Generate the HTML <body> section using your model
        raw_html = call_llama_vision(str(image_path), prompt)
        body_html = clean_ai_output(raw_html)

        # Assemble full HTML by replacing the body placeholder
        full_html = wrapper.replace("{{Body content goes here }}", body_html)

        # Save to output
        output_file = OUTPUT_FOLDER / (image_path.stem + ".html")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(full_html)

        print(f"✅ Saved: {output_file}")

if __name__ == "__main__":
    main()