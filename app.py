
import difflib
import html
import os
from pathlib import Path

import gradio as gr
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# ==========================================
# MODEL CONFIGURATION
# ==========================================

MODEL_DIR = Path(
    os.getenv("GEC_MODEL_DIR", "models/gec_t5_bea_final")
)

MAX_INPUT_LENGTH = 128
MAX_NEW_TOKENS = 128

if not (MODEL_DIR / "config.json").exists():
    raise FileNotFoundError(
        f"Model not found at: {MODEL_DIR}. "
        "Place the trained model inside this directory."
    )

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

print(f"Loading model from: {MODEL_DIR}")
print(f"Runtime device: {DEVICE}")


# ==========================================
# LOAD MODEL AND TOKENIZER
# ==========================================

tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR))

model = AutoModelForSeq2SeqLM.from_pretrained(
    str(MODEL_DIR),
    torch_dtype=DTYPE
).to(DEVICE)

model.eval()

print("Grammar correction model loaded successfully!")


# ==========================================
# GRAMMAR CORRECTION
# ==========================================

def correct_sentence(sentence: str) -> str:

    sentence = sentence.strip()

    if not sentence:
        return ""

    # Same prefix used during model training
    prompt = "grammar: " + sentence

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=MAX_INPUT_LENGTH
    ).to(DEVICE)

    with torch.inference_mode():

        output_ids = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=3
        )

    result = tokenizer.decode(
        output_ids[0],
        skip_special_tokens=True
    ).strip()

    return result if result else sentence


# ==========================================
# HIGHLIGHT TEXT CHANGES
# ==========================================

def highlight_changes(original: str, corrected: str) -> str:

    old_words = original.split()
    new_words = corrected.split()

    matcher = difflib.SequenceMatcher(
        a=old_words,
        b=new_words
    )

    pieces = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():

        if tag == "equal":

            pieces.extend(
                html.escape(word)
                for word in old_words[i1:i2]
            )

        elif tag == "delete":

            removed = html.escape(
                " ".join(old_words[i1:i2])
            )

            pieces.append(
                f'<del class="removed">{removed}</del>'
            )

        elif tag == "insert":

            added = html.escape(
                " ".join(new_words[j1:j2])
            )

            pieces.append(
                f'<ins class="added">{added}</ins>'
            )

        elif tag == "replace":

            removed = html.escape(
                " ".join(old_words[i1:i2])
            )

            added = html.escape(
                " ".join(new_words[j1:j2])
            )

            if removed:
                pieces.append(
                    f'<del class="removed">{removed}</del>'
                )

            if added:
                pieces.append(
                    f'<ins class="added">{added}</ins>'
                )

    return " ".join(pieces)


# ==========================================
# PROCESS INPUT TEXT
# ==========================================

def process_text(text: str):

    if not text or not text.strip():

        return (
            "",
            "<p class='empty'>Enter some text to get started.</p>",
            "Please enter text."
        )

    corrected_lines = []
    highlighted_lines = []

    try:

        for line in text.splitlines():

            if not line.strip():

                corrected_lines.append("")
                highlighted_lines.append("<br>")

                continue

            corrected = correct_sentence(line)

            corrected_lines.append(corrected)

            highlighted_lines.append(
                highlight_changes(line, corrected)
            )

        corrected_text = "\n".join(corrected_lines)

        highlighted_html = (
            "<div class='diff-output'>"
            + "<br>".join(highlighted_lines)
            + "</div>"
        )

        status = (
            "Correction complete. "
            "Review the highlighted changes before using the text."
        )

        return corrected_text, highlighted_html, status

    except Exception as error:

        print(f"Correction error: {error}")

        return (
            "",
            "<p class='empty'>Unable to process the text.</p>",
            "An error occurred while correcting the text."
        )


# ==========================================
# CUSTOM CSS
# ==========================================

CSS = """
.gradio-container {
    max-width: 1100px !important;
    margin: auto !important;
}

.hero {
    padding: 22px 24px;
    border-radius: 16px;
    background: linear-gradient(120deg,#102a43,#1d4e89);
    color: white;
    margin-bottom: 16px;
}

.hero h1 {
    margin: 0 0 8px 0;
    font-size: 28px;
}

.hero p {
    margin: 0;
    opacity: .9;
}

.diff-output {
    padding: 16px;
    min-height: 120px;
    line-height: 2;
    white-space: normal;
    overflow-wrap: anywhere;
    border: 1px solid var(--border-color-primary);
    border-radius: 10px;
    background: var(--background-fill-secondary);
}

.removed {
    background: #ffd9d9;
    color: #9b1c1c;
    text-decoration: line-through;
    padding: 2px 4px;
    border-radius: 4px;
}

.added {
    background: #d9fbe5;
    color: #166534;
    text-decoration: none;
    padding: 2px 4px;
    border-radius: 4px;
}

.legend {
    font-size: 13px;
    color: var(--body-text-color);
    margin: 8px 0 14px;
}

.empty {
    color: var(--body-text-color-subdued);
}

footer {
    visibility: hidden;
}
"""


# ==========================================
# GRADIO INTERFACE
# ==========================================

with gr.Blocks(
    theme=gr.themes.Soft(),
    css=CSS,
    title="Grammar Auto-Correction"
) as demo:

    gr.HTML("""
    <div class="hero">
        <h1>Grammar Auto-Correction</h1>
        <p>
            An NLP application powered by a fine-tuned T5 Transformer.
            Correct English text and inspect every change.
        </p>
    </div>
    """)

    with gr.Row():

        with gr.Column(scale=1):

            gr.Markdown("### Original text")

            input_text = gr.Textbox(
                lines=9,
                placeholder="Example: She go to school yesterday and buyed a book.",
                label="Enter one or more sentences"
            )

            with gr.Row():

                correct_btn = gr.Button(
                    "Correct grammar",
                    variant="primary"
                )

                clear_btn = gr.ClearButton(
                    [input_text],
                    value="Clear"
                )

        with gr.Column(scale=1):

            gr.Markdown("### Corrected text")

            corrected_text = gr.Textbox(
                lines=9,
                label="Generated correction",
                interactive=False,
                placeholder="Your corrected text will appear here."
            )

    gr.Markdown("### Changes highlighted")

    gr.HTML("""
    <div class="legend">
        <span style="background:#ffd9d9;color:#9b1c1c;padding:3px 7px;border-radius:4px;">
            Deleted text
        </span>
        &nbsp;
        <span style="background:#d9fbe5;color:#166534;padding:3px 7px;border-radius:4px;">
            Inserted text
        </span>
    </div>
    """)

    highlighted = gr.HTML(
        value="""
        <div class='diff-output'>
            <span class='empty'>
                Your highlighted changes will appear here.
            </span>
        </div>
        """
    )

    status = gr.Markdown("Ready.")

    correct_btn.click(
        fn=process_text,
        inputs=input_text,
        outputs=[
            corrected_text,
            highlighted,
            status
        ]
    )

    input_text.submit(
        fn=process_text,
        inputs=input_text,
        outputs=[
            corrected_text,
            highlighted,
            status
        ]
    )

    gr.Markdown(f"""
    ---
    **Model:** `{MODEL_DIR}`

    **Runtime device:** `{DEVICE}`

    **Note:** Transformer output is a suggestion.
    Review names, technical terms, and context-sensitive changes.
    """)


# ==========================================
# APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":

    demo.queue().launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("PORT", "7860"))
    )
