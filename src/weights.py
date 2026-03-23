class WeightManager:
    """Handles AI parameters and INT8 quantization logic."""
    def __init__(self, hole_w=3, height_w=9, column_w=5, use_quantized=False):
        if use_quantized:
            from .optimize import optimize_ai_parameters
            q_w, s, z = optimize_ai_parameters(hole_w, height_w, column_w)
            # Dequantize for runtime use
            weights = (s * (q_w - z))
            self.hole_weight = weights[0]
            self.height_weight = weights[1]
            self.column_weight = weights[2]
        else:
            self.hole_weight = hole_w
            self.height_weight = height_w
            self.column_weight = column_w