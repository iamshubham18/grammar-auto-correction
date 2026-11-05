
import difflib
import html
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# ==========================================
# MODEL CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "models" / "gec_t5_bea_final"

MAX_INPUT_LENGTH = 128
MAX_NEW_TOKENS = 128

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32


# ==========================================
# LOAD MODEL AND TOKENIZER
# ==========================================

if not (MODEL_DIR / "config.json").exists():
    raise FileNotFoundError(
        f"Trained model not found at: {MODEL_DIR}"
    )

print(f"Loading model from: {MODEL_DIR}")
print(f"Runtime device: {DEVICE}")

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
# PROCESS MULTIPLE LINES
# ==========================================

def correct_text(text: str) -> str:

    corrected_lines = []

    for line in text.splitlines():

        if not line.strip():
            corrected_lines.append("")
            continue

        corrected_lines.append(
            correct_sentence(line)
        )

    return "\n".join(corrected_lines)


# ==========================================
# HIGHLIGHT CHANGES
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
