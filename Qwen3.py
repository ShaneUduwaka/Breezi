!nvidia-smi

!pip install qwen-tts

# Install SoX
!apt-get install sox -y

# Install FlashAttention
#!pip install flash-attn --no-cache-dir

import qwen_tts
#import flash_attn
print("Qwen TTS ready")
#print("FlashAttention ready")

!git clone https://github.com/QwenLM/Qwen3-TTS.git

!ls Qwen3-TTS

!pip install qwen-tts transformers soundfile librosa numpy
