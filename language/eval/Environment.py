# Environment class
class Environment:

    # constructor
    def __init__(self):
        self.store = {}
        self.outer = None

    # get value from store or outer store
    def get(self, name):
        return self.store.get(name, None) or (self.outer and self.outer.get(name))
    
    # set value
    def set(self, name, value):
        self.store[name] = value
        return value

    # create an encapsulated store
    def extend(self):
        env = Environment()
        env.outer = self
        return env