class CompressionParams:
    def __init__(self, samples, edge_strength, color_salience, sampling_linearity, seed):
        self.samples = samples
        self.edge_strength = edge_strength
        self.color_salience = color_salience
        self.sampling_linearity = sampling_linearity
        self.seed = seed

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(dict_obj):
        return CompressionParams(**dict_obj)
