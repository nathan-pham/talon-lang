class Environment:
    def __init__(self):
        self.store = {}

    def get(self, name):
        return self.store.get(name, None)
    
    def set(self, name, value):
        self.store[name] = value
        return value