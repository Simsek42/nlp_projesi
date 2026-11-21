---
library_name: transformers
license: mit
base_model: dbmdz/bert-base-turkish-cased
tags:
- generated_from_trainer
metrics:
- accuracy
model-index:
- name: watsons-sentiment-bert-tr
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# watsons-sentiment-bert-tr

This model is a fine-tuned version of [dbmdz/bert-base-turkish-cased](https://huggingface.co/dbmdz/bert-base-turkish-cased) on the None dataset.
It achieves the following results on the evaluation set:
- Loss: 0.1298
- Accuracy: 0.98

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 2e-05
- train_batch_size: 8
- eval_batch_size: 8
- seed: 42
- optimizer: Use OptimizerNames.ADAMW_TORCH_FUSED with betas=(0.9,0.999) and epsilon=1e-08 and optimizer_args=No additional optimizer arguments
- lr_scheduler_type: linear
- num_epochs: 3

### Training results

| Training Loss | Epoch | Step | Validation Loss | Accuracy |
|:-------------:|:-----:|:----:|:---------------:|:--------:|
| 0.2269        | 1.0   | 500  | 0.1304          | 0.974    |
| 0.0785        | 2.0   | 1000 | 0.1514          | 0.971    |
| 0.0367        | 3.0   | 1500 | 0.1298          | 0.98     |


### Framework versions

- Transformers 5.22.2
- Pytorch 2.15.0+cpu
- Datasets 5.2.0
- Tokenizers 0.23.3
