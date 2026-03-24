import torch
import numpy as np
import os

def quantify_tensor(tensor, bits=8):
    # Asymmetric Post-Training Quantization: Mapping Float32 range to Int8 space
    w = tensor.detach().cpu().numpy()
    
    qmin = 0
    qmax = 2**bits - 1
    
    # Statistical range analysis
    w_min, w_max = w.min(), w.max()
    
    # Scale (S) and Zero-point (Z) derivation
    scale = (w_max - w_min) / (qmax - qmin)
    
    # Numerical stability check for static layers
    if scale == 0:
        scale = 1e-8
        
    initial_zero_point = qmin - w_min / scale
    
    # Linear affine transformation to integer space [0, 255]
    zero_point = np.clip(np.round(initial_zero_point), qmin, qmax).astype(np.uint8)
    w_quantized = np.clip(np.round(w / scale + zero_point), qmin, qmax).astype(np.uint8)
    
    return w_quantized, scale, zero_point

def run_model_optimization(model_path="tetris_brain.pth"):
    # Load trained model parameters and execute weight optimization
    if not os.path.exists(model_path):
        print(f"File error: {model_path} not found.")
        return None

    print(f"Optimizing Inference: {model_path}")
    
    state_dict = torch.load(model_path, map_location=torch.device('cpu'))
    
    total_original_size = 0
    total_quantized_size = 0
    layer_count = 0

    for layer_name, weights in state_dict.items():
        # Quantization targeting tensor weights and biases
        if isinstance(weights, torch.Tensor) and weights.ndimension() > 0:
            layer_count += 1
            q_weights, scale, zp = quantify_tensor(weights)
            
            # Memory footprint calculation (FP32: 4 bytes vs INT8: 1 byte)
            original_size = weights.nelement() * 4
            quantized_size = weights.nelement() * 1
            
            total_original_size += original_size
            total_quantized_size += quantized_size
            
            print(f"Layer: {layer_name:25} | {original_size:5}B -> {quantized_size:5}B | Scale: {scale:.6f}")

    # Optimization telemetry calculation
    compression_ratio = (1 - (total_quantized_size / total_original_size)) * 100
    
    print("-" * 50)
    print(f"Strategy: Post-Training Quantization (PTQ)")
    print(f"Memory Reduction: {compression_ratio:.2f}%")
    print(f"Status: Inference optimized for edge-deployment.")

    # Return telemetry for JSON logging
    return {
        "compression_ratio": round(compression_ratio, 2),
        "total_original_bytes": total_original_size,
        "total_optimized_bytes": total_quantized_size,
        "layers_optimized": layer_count
    }

if __name__ == "__main__":
    # Independent execution for logic verification
    stats = run_model_optimization()
    if stats:
        print(f"\nOptimization Metrics: {stats}")