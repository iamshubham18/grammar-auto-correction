# Grammar Auto-Correction using NLP and T5

An NLP-based grammar correction application powered by a fine-tuned T5-small Transformer model. It identifies grammatical errors, generates corrected sentences, and highlights the changes between the original and corrected text.

## Project Overview

This project explores how Transformer-based sequence-to-sequence models can be used for automatic grammatical error correction.

The application accepts one or more sentences, generates corrected versions using a fine-tuned T5-small model, and visually highlights deleted and inserted words.

## Features

- Automatic grammar correction.
- Supports multiple sentences in one input.
- Fine-tuned T5-small Transformer model.
- Red highlighting for deleted text.
- Green highlighting for inserted text.
- Interactive Gradio web interface.
- Local model inference.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| NLP Model | T5-small |
| Deep Learning | PyTorch |
| Model Framework | Hugging Face Transformers |
| Dataset | C4_200M |
| Evaluation Dataset | JFLEG |
| Evaluation Metric | GLEU |
| Interface | Gradio |
| Text Difference | Python difflib |
| Training Environment | Google Colab (T4 GPU) |

## Model Training Experiments

Two fine-tuning experiments were conducted using the C4_200M grammar correction dataset.

### Experiment 1: Initial Fine-tuning

- Base model: T5-small
- Training examples: 5,000
- Epochs: 1
- Batch size: 32
- Learning rate: 3e-4
- Maximum sequence length: 64
- Training loss: 0.9281

### Experiment 2: Improved Fine-tuning

- Base model: T5-small
- Training examples: 20,000
- Training split: 19,000 examples
- Validation split: 1,000 examples
- Epochs: 3
- Batch size: 32
- Learning rate: 1e-4
- Maximum sequence length: 64
- Final training loss: 0.7682

The second experiment used a fresh T5-small checkpoint rather than continuing training from Experiment 1.

## Model Evaluation

The models were evaluated using the JFLEG validation dataset containing 755 examples.

GLEU was used to measure the similarity between generated corrections and reference corrections.

| Model | GLEU Score |
|---|---:|
| Original T5-small baseline | 0.5092 |
| Fine-tuned T5-small (5K) | 0.6010 |
| Fine-tuned T5-small (20K) | **0.6057** |

The 20K model achieved the highest GLEU score among the three evaluated models.

The improvement over the original baseline was 0.0965 GLEU points.

## Application Workflow

1. User enters one or more sentences.
2. The application adds the grammar correction task prefix.
3. The fine-tuned T5 model generates corrected text.
4. Python's difflib identifies differences between the original and corrected sentences.
5. The application highlights deleted and inserted text.
6. Gradio displays the corrections.

## Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the trained model

Download the trained model checkpoint and extract it into:

```text
models/
└── gec_t5_improved/
    ├── config.json
    ├── model.safetensors
    ├── tokenizer_config.json
    └── ...
```

The model weights are not required to be committed directly to the Git repository.

### 5. Run the application

```bash
python app.py
```

Open the local Gradio URL displayed in the terminal, normally:

```text
http://127.0.0.1:7860
```

## Project Structure

```text
grammar-auto-correction/
│
├── app.py
├── requirements.txt
├── README.md
│
├── models/
│   ├──