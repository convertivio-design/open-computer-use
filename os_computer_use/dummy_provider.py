
class DummyProvider:
    def __init__(self):
        pass

    def call(self, prompt, image_data):
        return (0, 0)
