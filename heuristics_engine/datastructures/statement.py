class Statement:
    def __init__(self, explanatory, *args):
        self.explanatory = explanatory
        self.args = args
        
    def to_string(self):
        return f'{self.explanatory}' \
               + (f' ({", ".join([str(x) for x in self.args])})'
                  if self.args else '')
