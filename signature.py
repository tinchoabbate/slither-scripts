class Signature:
    def __init__(self, name, args, returns=[]):
        self.name = name
        self.args = args
        self.returns = returns
    
    def to_string(self, with_return):
        result = f"{self.name} ({', '.join(self.args)})"    
        if len(self.returns) and with_return:
            result = f"{result} -> ({', '.join(self.returns)})"    
        return result

    def __eq__(self, other):
        if isinstance(other, tuple):
            match = other[0] == self.name and other[1] == self.args
            return match and other[2] == self.returns if len(other) == 3 else match
        return NotImplemented
