from time import sleep

class dino:
    def __init__(self,game):
        self.game = game
        self.jump()
        sleep(0.2)

    def jump(self):
        self.game.jump()
    def isCrashed(self):
        return self.game.isCrashed()