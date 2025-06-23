import numpy as np

class Aggregator:
    def __init__(self, weights_list):
        """
        weights_list: List of model weights. Each element is a list of numpy arrays (one per layer).
        """
        self.weights_list = weights_list

    # FedAvg
    def aggregate(self):
        """
        Returns the element-wise average of the weights across all models.
        """
        # Transpose the list to group weights by layer
        # Each element in 'layer_weights' is a list of arrays for that layer from all models
        layer_weights = list(zip(*self.weights_list))
        # Average each layer's weights
        aggregated = [np.mean(np.stack(w), axis=0) for w in layer_weights]
        return aggregated