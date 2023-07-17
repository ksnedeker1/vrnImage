class CompressionParams:
    def __init__(self, compression_level, edge_strength, color_salience, sampling_uniformity, seed):
        self.compression_level = compression_level
        self.edge_strength = edge_strength
        self.color_salience = color_salience
        self.sampling_uniformity = sampling_uniformity
        self.seed = seed

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(dict_obj):
        return CompressionParams(**dict_obj)
