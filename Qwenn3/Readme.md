---

## Qwen Model

This project uses the **Qwen3-VL-8B-Instruct** large language model.

- Developed by **Alibaba Cloud – Qwen Team**
- Licensed under the **Apache License 2.0**

The full Apache 2.0 license text is included in this repository.

### Model Modifications

The original Qwen3-VL-8B-Instruct model has been **fine-tuned and adapted** as part of this project.  
All modifications and training procedures were performed by the project team for research purposes.

---
## 🧠 AI Brain: Qwen 3 8B Fine-Tuning (Sinhala)

This section of the repository contains the code and dataset samples used to fine-tune the **Qwen 3 8B** model to act as a conversational Sinhala food-ordering agent.

### Tech Stack
* **Base Model:** `Qwen/Qwen3-8B`
* **Fine-Tuning Framework:** Unsloth (QLoRA, 4-bit quantization)
* **Compute:** Google Colab (T4 GPU)
* **Dataset Format:** ChatML / ShareGPT

### File Structure
* `/Qwenn3/Training_Qwen3/qwen_colab_training.ipynb`: The exact Jupyter Notebook used to load the model, format the data, and run the SFTTrainer loop in Google Colab.
* `/Qwenn3/convert_data.py`: Script to convert raw JSON outputs into the optimized, tag-free ChatML `.jsonl` format required for low-latency voice generation.
* `/Qwenn3/sample_llm.json`: A safe, small sample of the Sinhala conversational data structure. 

### How to Train
1. Upload the `train.jsonl` dataset to a Google Colab instance (T4 GPU).
2. Run the `qwen_colab_training.ipynb` notebook from top to bottom.
3. The trained LoRA adapters will be saved in the `outputs/` directory.