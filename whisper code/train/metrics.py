import re
from transformers.models.whisper.english_normalizer import BasicTextNormalizer
import evaluate

normalizer = BasicTextNormalizer()
wer_metric = evaluate.load("wer")

def compute_metrics(pred, processor):
    pred_ids = pred.predictions
    label_ids = pred.label_ids
    label_ids[label_ids == -100] = processor.tokenizer.pad_token_id

    pred_str = processor.tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
    label_str = processor.tokenizer.batch_decode(label_ids, skip_special_tokens=True)

    clean_preds = [re.sub(r'[\u200d\u200c]', '', normalizer(s)) for s in pred_str]
    clean_labels = [re.sub(r'[\u200d\u200c]', '', normalizer(s)) for s in label_str]

    return {"wer": 100 * wer_metric.compute(predictions=clean_preds, references=clean_labels)}
