import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

print("--- Starting LLM Training Setup Check ---")

# Check CUDA
if torch.cuda.is_available():
    print(f"CUDA is available. Device count: {torch.cuda.device_count()}")
    print(f"Current device: {torch.cuda.get_device_name(0)}")
else:
    print("CUDA is NOT available. Running in CPU mode (slow).")

# Mock Model Loading (using a tiny model for demonstration speed)
model_name = "gpt2" # Small model for quick test
print(f"Loading model: {model_name}...")

try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

print("Ready for fine-tuning!")
print("--- Check Complete ---")
