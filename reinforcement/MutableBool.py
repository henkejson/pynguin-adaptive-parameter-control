class MutableBool:
    def __init__(self, value: bool):
        self.value = value

    def get(self) -> bool:
        return self.value

    def set(self, value: bool):
        self.value = value
