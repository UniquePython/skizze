from skizze_errors import SkizzeRuntimeError


class SkizzeEnvironment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def assign(self, name, value):
        if name in self.vars:
            self.vars[name] = value
            return
        if self.parent:
            self.parent.assign(name, value)
            return
        raise SkizzeRuntimeError(f"Undefined variable '{name}'")

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise SkizzeRuntimeError(f"Undefined variable '{name}'")

    def set(self, name, value):
        self.vars[name] = value
