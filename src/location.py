class Location:
    def __init__(self, image, map_x, map_y):
        self.image = image
        self.map_x = map_x
        self.map_y = map_y

    def get_position(self):
        return self.map_x, self.map_y

    def draw(self, window):
        pass

    def __str__(self):
        return f"Location with image {self.image} at ({self.map_x}, {self.map_y})"
