import torch
import numpy as np
import os

def quantify_tensor(tensor, bits=8):
    """
    Performs Asymmetric Post-Training Quantization.
    Demonstrates Linear Algebra: Mapping a Float32 range to an Int8 range.
    """
    # Detach from graph and convert to numpy for manual math demonstration
    w = tensor.detach().cpu().numpy()
    
    qmin = 0
    qmax = 2**bits - 1
    
    # 1. Calculate Statistics
    w_min, w_max = w.min(), w.max()
    
    # 2. Calculate Scale (S) and Zero-point (Z)
    # Formula: S = (max - min) / (qmax - qmin)
    scale = (w_max - w_min) / (qmax - qmin)
    
    # Avoid division by zero for empty/static layers
    if scale == 0:
        scale = 1e-8
        
    initial_zero_point = qmin - w_min / scale
    
    # 3. Quantize: Mapping float to the [0, 255] integer space
    zero_point = np.clip(np.round(initial_zero_point), qmin, qmax).astype(np.uint8)
    w_quantized = np.clip(np.round(w / scale + zero_point), qmin, qmax).astype(np.uint8)
    
    return w_quantized, scale, zero_point

def run_model_optimization(model_path="tetris_brain.pth"):
    """
    Loads the trained Tetris brain and optimizes its weights.
    Returns a dictionary of optimization metrics for logging.
    """
    if not os.path.exists(model_path):
        print(f"Error: {model_path} not found. Train the AI first!")
        return None

    print(f"--- Optimizing Inference for: {model_path} ---")
    
    # Load the state dictionary (the weights)
    state_dict = torch.load(model_path, map_location=torch.device('cpu'))
    
    total_original_size = 0
    total_quantized_size = 0
    layer_count = 0

    for layer_name, weights in state_dict.items():
        # We only optimize weights and biases (tensors)
        if isinstance(weights, torch.Tensor) and weights.ndimension() > 0:
            layer_count += 1
            q_weights, scale, zp = quantify_tensor(weights)
            
            # Calculate sizes in bytes
            # FP32 = 4 bytes, INT8 = 1 byte
            original_size = weights.nelement() * 4
            quantized_size = weights.nelement() * 1
            
            total_original_size += original_size
            total_quantized_size += quantized_size
            
            print(f"Layer: {layer_name:25} | Size: {original_size:5} bytes -> {quantized_size:5} bytes | Scale: {scale:.6f}")

    # Final Technical Summary
    compression_ratio = (1 - (total_quantized_size / total_original_size)) * 100
    
    print("-" * 50)
    print(f"Optimization Strategy: Post-Training Quantization (PTQ)")
    print(f"Total Memory Reduction: {compression_ratio:.2f}%")
    print(f"Status: Inference ready for edge-deployment.")

    # Return the metrics so they can be logged to JSON
    return {
        "compression_ratio": round(compression_ratio, 2),
        "total_original_bytes": total_original_size,
        "total_optimized_bytes": total_quantized_size,
        "layers_optimized": layer_count
    }

if __name__ == "__main__":
    # This can be run independently to prove optimization logic
    stats = run_model_optimization()
    if stats:
        print(f"\nCaptured Metrics: {stats}")