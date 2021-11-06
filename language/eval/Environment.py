class Environment:
    def __init__(self):
        self.store = {}
        self.outer = None

    def get(self, name):
        return self.store.get(name, None) or (self.outer and self.outer.get(name))
    
    def set(self, name, value):
        self.store[name] = value
        return value

    def extend(self):
        env = Environment()
        env.outer = self
        return env