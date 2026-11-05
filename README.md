# Grammar Auto-Correction using NLP and T5

An NLP-based grammar correction application powered by a fine-tuned **T5-small Transformer model**. It detects grammatical errors in English sentences and generates corrected versions, with visual highlighting to show the changes.

## Overview

The project explores how Transformer-based sequence-to-sequence models can improve English grammar correction.

The application uses a fine-tuned T5-small model trained on the C4_200M grammar correction dataset. Two training experiments were conducted using 5,000 and 20,000 sentence pairs, and their performance was evaluated using the JFLEG dataset and GLEU metric.

## Features

- English grammar error detection and correction.
- Transformer-based text generation using T5-small.
- Fine-tuned models trained on different dataset sizes.
- Interactive web interface built with Gradio.
- Visual highlighting of deleted and inserted text.
- Support for multiple sentences.
- Local model inference.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| NLP / Deep Learning | PyTorch, Hugging Face Transformers |
| Model | T5-small |
| Dataset | C4_200M |
| Evaluation | JFLEG, GLEU |
| Interface | Gradio |
| Development | Google Colab, Jupyter Notebook |

## Model Training Experiments

Two independent fine-tuning experiments were conducted using T5-small.

### Experiment 1: 5K Training

| Parameter | Value |
|---|---|
| Base model | T5-small |
| Training samples | 5,000 |
| Epochs | 1 |
| Batch size | 32 |
| Learning rate | 3e-4 |
| Maximum sequence length | 64 |
| Training loss | 0.9281 |
| JFLEG GLEU | 0.6010 |

### Experiment 2: 20K Training

| Parameter | Value |
|---|---|
| Base model | T5-small (fresh checkpoint) |
| Dataset samples | 20,000 |
| Training samples | 19,000 |
| Validation samples | 1,000 |
| Epochs | 3 |
| Batch size | 32 |
| Learning rate | 1e-4 |
| Maximum sequence length | 64 |
| Training loss | 0.7682 |
| JFLEG GLEU | 0.6057 |

## Evaluation Results

The models were evaluated using the GLEU metric on the JFLEG validation dataset.

| Model | GLEU Score |
|---|---:|
| Original T5-small | 0.5092 |
| Fine-tuned T5-small (5K) | 0.6010 |
| Fine-tuned T5-small (20K) | **0.6057** |

The 20K experiment achieved the highest GLEU score among the three evaluated models.

The results show improvement over the original T5-small baseline. However, the model can still produce incomplete or incorrect corrections for some complex sentences.

## Application Workflow

1. User enters an English sentence.
2. The application adds the `grammar:` task prefix.
3. The fine-tuned T5-small model generates a corrected sentence.
4. The application compares the original and corrected text.
5. Deleted and inserted words are visually highlighted.

## Project Structure

```text
grammar-auto-correction/
│
├── models/
│   └── gec_t5_improved/       # Local trained model checkpoint
│
├── notebooks/
│   ├── README.md
│   ├── train_5k_gec_colab.ipynb
│   └── train_20k_gec_colab.ipynb
│
├── app.py                     # Gradio application
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

**Note:** Model checkpoints and virtual environments are excluded from Git.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/iamshubham18/grammar-auto-correction.git

cd grammar-auto-correction
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the trained model checkpoint

The trained model weights are not included in this repository.

Place the trained checkpoint in the following directory:

```text
models/gec_t5_improved/
```

Alternatively, set the `GEC_MODEL_DIR` environment variable to the location of your downloaded checkpoint.

The 20K training notebook is provided in `notebooks/` to reproduce the training process.

### 5. Run the application

```bash
python app.py
```

Open the local Gradio URL displayed in the terminal, usually:

```text
http://127.0.0.1:7860
```

## Limitations

- The model is trained specifically for English grammar correction.
- Some complex grammatical errors may not be corrected accurately.
- The model may occasionally generate incomplete or unintended corrections.
- Performance depends on the training data and model configuration.
- The application currently performs local inference.

## Future Improvements

- Train with a larger and more diverse grammar correction dataset.
- Improve article, preposition, and pronoun error correction.
- Experiment with larger Transformer models.
- Add more comprehensive evaluation metrics.
- Improve inference speed and application usability.
- Explore deployment through a cloud-based API.

## Author

**Shubham Kumar Verma**

- GitHub: [@iamshubham18](https://github.com/iamshubham18)
- LinkedIn: [Shubham Kumar Verma](https://www.linkedin.com/in/shubham-kumar-verma-18vk/)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.