# class WeightManager:
#     def __init__(self, hole_w=40, height_w=10, bump_w=3, trans_w=2):
#         self.hole_weight = hole_w
#         self.height_weight = height_w
#         self.bumpiness_weight = bump_w
#         self.transition_weight = trans_w

#     def get_score(self, metrics, lines_removed):
#         # Line clears are now the priority!
#         score = (lines_removed ** 2) * 500 
        
#         # Penalties (Adjusted ratios)
#         score -= (metrics['holes'] * self.hole_weight)
#         score -= (metrics['blockades'] * 20)
#         score -= (metrics['bumpiness'] * self.bumpiness_weight)
#         score -= (metrics['max_height'] * self.height_weight)
#         score -= (metrics['total_height'] * 2)
#         return score