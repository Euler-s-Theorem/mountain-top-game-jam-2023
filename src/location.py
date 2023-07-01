class Location:
    def __init__(self, image, map_x, map_y):
        self.image = image
        self.map_x = map_x
        self.map_y = map_y

    @classmethod
    def from_name(cls, name):
        pass

    def draw(self, window):
        pass
