import cv2

class game_state:
    def __init__(self,dino,game):
        self.dino = dino
        self.game = game

    def get(self,action,debug=True):
        score = self.game.getScore()
        reward = 0.1*score/10
        gameover = False

        if action == 1:
            self.dino.jump()
            reward = 0.1*score/11
        state = self.game.getScreen()

        if debug:
            cv2.imshow('game',state)
            cv2.waitKey(1)
        if self.dino.isCrashed():
            gameover = True
            reward = -10/score
        return state,reward,gameover