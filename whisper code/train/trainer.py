import os, json
from datasets import load_from_disk
import torch
from transformers import (
    WhisperForConditionalGeneration, 
    WhisperProcessor, 
    Seq2SeqTrainer, 
    Seq2SeqTrainingArguments
)
from transformers.trainer_utils import get_last_checkpoint
from train.data_collator import DataCollatorSpeechSeq2SeqWithPadding
from train.metrics import compute_metrics

def run_training(local_path, config_path="configs/training_args.json"):
    # Load training config from JSON
    with open(config_path, "r") as f:
        training_config = json.load(f)

    output_dir = training_config.get("output_dir", "./whisper-output")
    
    # Load processor and model
    processor = WhisperProcessor.from_pretrained("openai/whisper-large-v3")
    model = WhisperForConditionalGeneration.from_pretrained(
        "openai/whisper-large-v3",
        torch_dtype=torch.bfloat16,
        attn_implementation="flash_attention_2"
    )
    model.config.forced_decoder_ids = None
    model.config.use_cache = False

    # Load dataset
    dataset = load_from_disk(local_path)
    train_ds = dataset["train"]
    eval_ds = dataset["test"].shuffle(seed=42).select(range(1000))

    # Convert JSON config to Seq2SeqTrainingArguments
    training_args = Seq2SeqTrainingArguments(
        output_dir=output_dir,
        **training_config  # unpack all other fields from JSON
    )

    # Detect last checkpoint
    last_checkpoint = get_last_checkpoint(output_dir) if os.path.isdir(output_dir) else None

    # Trainer
    trainer = Seq2SeqTrainer(
        args=training_args,
        model=model,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        tokenizer=processor.tokenizer,
        data_collator=DataCollatorSpeechSeq2SeqWithPadding(processor),
        compute_metrics=lambda pred: compute_metrics(pred, processor),
    )

    trainer.train(resume_from_checkpoint=last_checkpoint)
