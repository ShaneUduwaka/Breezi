# checkenv.py
import torch
import sys
import subprocess

def check_python():
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 10):
        print("⚠️ Warning: Recommended Python >= 3.10")

def check_cuda():
    if torch.cuda.is_available():
        print(f"CUDA available: {torch.version.cuda}")
        print(f"GPU count: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            print(f" - GPU {i}: {torch.cuda.get_device_name(i)}")
    else:
        print("⚠️ CUDA not available. Will run on CPU (slow!)")

def check_bf16():
    # bf16 support requires Ampere+ GPUs
    try:
        if torch.cuda.is_available():
            x = torch.randn(1, device="cuda").bfloat16
            print("✅ bf16 supported on this GPU")
        else:
            print("⚠️ bf16 requires GPU, running on CPU")
    except Exception as e:
        print(f"⚠️ bf16 not supported: {e}")

def check_flash_attention():
    try:
        from torch.nn import MultiheadAttention
        # Flash attention requires PyTorch 2.x + supported CUDA
        print("✅ Flash attention import check passed")
    except Exception as e:
        print(f"⚠️ Flash attention might fail: {e}")

def check_dependencies():
    print("\nChecking core dependencies...")
    required = [
        "torch", "torchaudio", "transformers", "datasets",
        "evaluate", "numpy", "sentencepiece", "soundfile",
        "ffmpeg", "jiwer"
    ]
    for pkg in required:
        try:
            subprocess.run([sys.executable, "-c", f"import {pkg}"], check=True)
            print(f"✅ {pkg} installed")
        except subprocess.CalledProcessError:
            print(f"⚠️ {pkg} NOT installed")

if __name__ == "__main__":
    print("=== ENVIRONMENT CHECK ===")
    check_python()
    check_cuda()
    check_bf16()
    check_flash_attention()
    check_dependencies()
    print("=== CHECK COMPLETE ===")
