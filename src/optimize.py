import torch
import numpy as np
import os

def quantify_weights(tensor, bits=8):
    """
    Manually quantize a weight tensor to 8-bit precision using NumPy.
    Demonstrates post-training quantization (PTQ) logic.
    """
    w = tensor.detach().numpy()
    
    qmin = 0
    qmax = 2**bits - 1
    
    # Calculate scale (S) and zero-point (Z)
    w_min, w_max = w.min(), w.max()
    scale = (w_max - w_min) / (qmax - qmin)
    initial_zero_point = qmin - w_min / scale
    
    # Clip zero_point to ensure it stays within [0, 255]
    zero_point = np.clip(np.round(initial_zero_point), qmin, qmax).astype(np.uint8)
    
    # Quantize: float32 -> uint8
    w_quantized = np.clip(np.round(w / scale + zero_point), qmin, qmax).astype(np.uint8)
    
    return w_quantized, scale, zero_point

def dequantize_weights(w_quantized, scale, zero_point):
    """Reconstruct float32 weights for validation."""
    return (scale * (w_quantized.astype(np.float32) - zero_point))

def optimize_ai_parameters(hole_w, height_w, col_w):
    """
    Converts Tetris AI weights into a quantized tensor format.
    """
    print("--- Tetris AI Weight Optimization ---")
    
    # 1. Convert local AI weights to a PyTorch Tensor
    raw_weights = torch.tensor([float(hole_w), float(height_w), float(col_w)])
    print(f"Original (FP32): {raw_weights.numpy()}")

    # 2. Apply 8-bit Quantization
    q_weights, scale, zp = quantify_weights(raw_weights)
    print(f"Quantized (INT8): {q_weights}")
    print(f"Scale: {scale:.6f}, Zero-Point: {zp}")

    # 3. Validation
    reconstructed = dequantize_weights(q_weights, scale, zp)
    error = np.mean((raw_weights.numpy() - reconstructed)**2)
    
    print(f"Reconstruction MSE: {error:.10f}")
    print(f"Compression: {((4-1)/4)*100}% memory reduction per parameter.")
    
    return q_weights, scale, zp

if __name__ == "__main__":
    # Example usage: Optimizing the default AI weights
    optimize_ai_parameters(hole_w=3, height_w=9, col_w=5)