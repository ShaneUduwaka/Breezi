# scripts/env_check.py
import sys
import torch
import subprocess

def fail(msg):
    print(f"\n❌ ENV CHECK FAILED: {msg}\n")
    sys.exit(1)

def warn(msg):
    print(f"⚠️  WARNING: {msg}")

def ok(msg):
    print(f"✅ {msg}")

print("\n🔍 Running environment checks...\n")

# 1. CUDA availability
if not torch.cuda.is_available():
    fail("CUDA is not available. This training requires NVIDIA GPUs.")

ok("CUDA is available")

# 2. GPU info
device = torch.cuda.get_device_properties(0)
gpu_name = device.name
vram_gb = device.total_memory / (1024**3)

print(f"🖥️  GPU: {gpu_name}")
print(f"💾 VRAM: {vram_gb:.1f} GB")

if vram_gb < 40:
    warn("VRAM < 40GB. You MUST reduce batch size or use gradient accumulation.")

# 3. bf16 support
bf16_supported = torch.cuda.is_bf16_supported()
if not bf16_supported:
    warn("bf16 NOT supported on this GPU. Training must fall back to fp16.")
else:
    ok("bf16 is supported")

# 4. Flash Attention 2 check
flash_attn_ok = True
try:
    import flash_attn
    ok("flash-attn is installed")
except Exception as e:
    flash_attn_ok = False
    warn("flash-attn is NOT installed or incompatible")
    warn("Training must disable Flash Attention 2")

# 5. Torch / CUDA version sanity
torch_version = torch.__version__
cuda_version = torch.version.cuda

print(f"🔥 Torch version: {torch_version}")
print(f"🧩 CUDA version: {cuda_version}")

if cuda_version is None:
    fail("Torch was compiled without CUDA support.")

# 6. Summary
print("\n📋 ENVIRONMENT SUMMARY")
print("---------------------")
print(f"GPU            : {gpu_name}")
print(f"VRAM           : {vram_gb:.1f} GB")
print(f"bf16 supported : {bf16_supported}")
print(f"flash-attn     : {flash_attn_ok}")
print(f"torch          : {torch_version}")
print(f"cuda           : {cuda_version}")

print("\n✅ Environment check completed.\n")

# Exit code rules:
# - FAIL only if CUDA missing
# - Everything else is recoverable by config
