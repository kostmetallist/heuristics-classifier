class Statement:
    @staticmethod
    def prune_float(x):
        return round(x, 6)

    def __init__(self, explanatory, *args):
        self.explanatory = explanatory
        self.args = args
        
    def to_string(self):
        prepared = [(str(self.prune_float(x)) if type(x) == float else str(x))
                    for x in self.args]
        return f'{self.explanatory}' \
               + (f' ({", ".join(prepared)})' if self.args else '')
