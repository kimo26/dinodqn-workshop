from model import q_model

class bot:
    def __init__(self,game,game_state):
        self.game = game
        self.game_state = game_state
        self.num_actions = 2
    
    def train(self,name=None):
        model = q_model(actions=self.num_actions)
        model_target = q_model(actions=self.num_actions)

        if name is not None:
            model.load_weights(name)
            model_target.load_weights(model)
        