class Settings(object):

    def __init__(self):
        self.colors = {
            'BLACK': (0, 0, 0),
            'WHITE': (255, 255, 255)
        }
        self._game_name = "Dino Run Game"
        self.size = self.width, self.height = 900, 270