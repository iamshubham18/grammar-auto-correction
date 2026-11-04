# Training Notebooks

This folder contains the Google Colab notebooks used to train and evaluate the Grammar Auto-Correction model.

## Notebooks

### 1. `train_5k_gec_colab.ipynb`
- Base model: T5-small
- Training samples: 5,000
- Epochs: 1
- Learning rate: 3e-4
- Batch size: 32
- Training loss: 0.9281
- JFLEG GLEU score: 0.6010

### 2. `train_20k_gec_colab.ipynb`
- Base model: T5-small (fresh checkpoint)
- Training samples: 20,000
- Training samples after split: 19,000
- Validation samples: 1,000
- Epochs: 3
- Learning rate: 1e-4
- Batch size: 32
- Training loss: 0.7682
- JFLEG GLEU score: 0.6057

## Evaluation Results

| Model | JFLEG GLEU |
|---|---:|
| Original T5-small | 0.5092 |
| Fine-tuned on 5K samples | 0.6010 |
| Fine-tuned on 20K samples | 0.6057 |

The 20K experiment achieved the best GLEU score among these experiments.

## Notes
- Both notebooks use the C4_200M dataset.
- Training was performed using Google Colab.
- The 20K experiment started from a fresh T5-small checkpoint rather than continuing from the 5K model.
- Model checkpoints are not included in this repository.
