# Grammar Auto-Correction using NLP and T5

An NLP-based grammar correction application built using a fine-tuned **T5-small Transformer model**. The application detects grammatical errors, generates corrected sentences, and highlights the changes between the original and corrected text using an interactive Gradio interface.

## Project Overview

This project explores the use of Transformer-based sequence-to-sequence models for Automatic Grammatical Error Correction (GEC).

The application accepts one or multiple sentences, processes them using a fine-tuned T5-small model, and generates grammatically improved versions. It also uses Python's `difflib` library to identify and highlight changes.

## Features

- Automatic grammar correction using a fine-tuned T5 model.
- Supports multiple sentences in a single input.
- Highlights deleted words in **red**.
- Highlights inserted words in **green**.
- Interactive web interface built with Gradio.
- Local model inference.
- Evaluation using the GLEU metric.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| NLP Architecture | T5-small Transformer |
| Deep Learning Framework | PyTorch |
| Model Library | Hugging Face Transformers |
| Training Dataset | C4_200M |
| Evaluation Dataset | JFLEG |
| Evaluation Metric | GLEU |
| Web Interface | Gradio |
| Text Difference | Python difflib |
| Training Environment | Google Colab (T4 GPU) |

## Model Training

Two fine-tuning experiments were conducted using the C4_200M grammar correction dataset.

### Experiment 1: Initial Fine-tuning

| Parameter | Configuration |
|---|---|
| Base Model | T5-small |
| Training Examples | 5,000 |
| Epochs | 1 |
| Batch Size | 32 |
| Learning Rate | 3e-4 |
| Maximum Sequence Length | 64 |
| Training Loss | 0.9281 |

### Experiment 2: Improved Fine-tuning

| Parameter | Configuration |
|---|---|
| Base Model | T5-small |
| Training Examples | 20,000 |
| Training Split | 19,000 |
| Validation Split | 1,000 |
| Epochs | 3 |
| Batch Size | 32 |
| Learning Rate | 1e-4 |
| Maximum Sequence Length | 64 |
| Final Training Loss | 0.7682 |

**Note:** Experiment 2 started from a fresh T5-small checkpoint rather than continuing from the 5K fine-tuned model.

## Model Evaluation

The models were evaluated using the validation split of the JFLEG dataset, containing 755 examples.

GLEU (Google-BLEU) was used to measure the similarity between generated corrections and reference corrections.

| Model | GLEU Score |
|---|---:|
| Original T5-small (Baseline) | 0.5092 |
| Fine-tuned T5-small (5K) | 0.6010 |
| Fine-tuned T5-small (20K) | **0.6057** |

The 20K fine-tuned model achieved the highest GLEU score among the three evaluated models.

It improved the GLEU score by 0.0965 points compared with the original baseline.

## Application Workflow

1. The user enters one or more sentences.
2. The application adds the `grammar:` task prefix.
3. The fine-tuned T5 model generates corrected sentences.
4. Python's `difflib` identifies differences between the original and corrected text.
5. Deleted and inserted words are highlighted.
6. Gradio displays the original text, corrected text, and highlighted changes.

## Project Structure

```text
grammar-auto-correction/
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
├── notebooks/
│   ├── README.md
│   └── train_5k_gec_colab.ipynb
│
└── models/                 # Excluded from Git
    ├── gec_t5/
    └── gec_t5_improved/
```

The trained model checkpoints are stored locally and excluded from Git because of their large file sizes.

## Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/iamshubham18/grammar-auto-correction.git

cd grammar-auto-correction
```

### 2. Create a virtual environment

For Windows PowerShell:

```powershell
python -m venv .venv

.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the trained model

The application requires the fine-tuned model checkpoint.

Download or obtain the trained checkpoint and extract it into the following directory:

```text
models/
└── gec_t5_improved/
    ├── config.json
    ├── generation_config.json
    ├── model.safetensors
    ├── tokenizer_config.json
    └── ...
```

Make sure the model directory contains the required model and tokenizer files.

**Note:** Model weights are not included in this GitHub repository.

### 5. Run the application

```bash
python app.py
```

Open the local Gradio URL displayed in the terminal:

```text
http://127.0.0.1:7860
```

## Limitations

- The model may not correct every grammatical error.
- Some corrections may be incomplete or inaccurate.
- The model may occasionally overcorrect sentences.
- Certain article, preposition, and pronoun errors remain challenging.
- The training experiments use a subset of the C4_200M dataset.
- The application primarily focuses on sentence-level grammar correction.

## Future Improvements

- Train with a larger and more diverse dataset.
- Improve article, preposition, and pronoun correction.
- Experiment with different Transformer architectures.
- Evaluate using additional grammar correction benchmarks.
- Optimize model inference and application performance.
- Deploy the application for public use.

## Author

**Shubham Kumar Verma**

- GitHub: [@iamshubham18](https://github.com/iamshubham18)
- Repository: [Grammar Auto-Correction](https://github.com/iamshubham18/grammar-auto-correction)

---

*This project was developed as a practical exploration of Natural Language Processing, Transformer models, and automatic grammatical error correction.*